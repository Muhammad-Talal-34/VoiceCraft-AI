from flask import Flask, request, render_template, jsonify
import torch
import scipy.io.wavfile as wavfile
from transformers import VitsModel, AutoTokenizer
import os
import uuid
import glob
import time

app = Flask(__name__)

# 1. Load Local Model
MODEL_PATH = "./urdu_model"
print("Offline Urdu model load ho raha hai...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = VitsModel.from_pretrained(MODEL_PATH, local_files_only=True)
print("Model successfully memory me load ho gaya!")

# Create static/audio directory if it doesn't exist
os.makedirs('static/audio', exist_ok=True)

def cleanup_old_audio():
    """Deletes audio files older than 1 hour to prevent hard drive bloat."""
    folder = 'static/audio'
    now = time.time()
    for f in glob.glob(os.path.join(folder, "*.wav")):
        if os.stat(f).st_mtime < now - 3600:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Cleanup error: {e}")

# 2. Render Frontend Route
@app.route('/')
def index():
    return render_template('index.html')

# 3. Text to Speech API Route
@app.route('/api/tts', methods=['POST'])
def tts_generate():
    try:
        # SAFELY parse the JSON. force=True ignores missing headers. silent=True prevents crashes.
        data = request.get_json(force=True, silent=True)
        
        # Safety check: if data is still None, return a clean JSON error
        if data is None:
            return jsonify({"error": "Invalid or missing JSON data."}), 400
            
        text = data.get('text', '')

        if not text.strip():
            return jsonify({"error": "Text cannot be empty."}), 400
        
        # Run cleanup before generating new audio
        cleanup_old_audio()

        # Tokenize text
        inputs = tokenizer(text, return_tensors="pt")
        
        # Generate speech waveform
        with torch.no_grad():
            output = model(**inputs).waveform

        # Save audio with a unique filename
        filename = f"voice_{uuid.uuid4().hex[:8]}.wav"
        filepath = os.path.join('static', 'audio', filename)
        
        sampling_rate = model.config.sampling_rate
        audio_data = output.squeeze().cpu().numpy()
        wavfile.write(filepath, rate=sampling_rate, data=audio_data)
        
        # Use forward slashes for the web URL so it works perfectly on Windows
        audio_url = f"/static/audio/{filename}"
        
        return jsonify({"audio_url": audio_url})
        
    except Exception as e:
        # If anything else fails, return the actual error as JSON so the frontend can read it
        print(f"Server Error: {str(e)}") 
        return jsonify({"error": f"Server crash: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)