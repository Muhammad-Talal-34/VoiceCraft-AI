# VoiceCraft AI — Neural Urdu Text-to-Speech

**Transform Urdu text into speech using locally hosted neural AI.**

VoiceCraft AI is an AI-powered Urdu Text-to-Speech (TTS) web application that converts written Urdu into spoken audio using Meta's MMS VITS speech synthesis model. Built with Python and Flask, it provides an intuitive interface for generating and playing Urdu speech directly in the browser.

The application runs inference locally using pre-downloaded model files, eliminating runtime dependency on external speech-generation APIs.

## Key Features

- **Urdu Text-to-Speech:** Convert written Urdu text into generated speech.
- **Neural Speech Synthesis:** Powered by Meta's MMS VITS multilingual TTS architecture.
- **Local Model Inference:** Run speech generation using locally stored model weights.
- **Interactive Web Interface:** Enter Urdu text and play generated audio directly in the browser.
- **REST API Integration:** Expose speech generation through a Flask-based JSON API.
- **WAV Audio Generation:** Save generated speech as WAV audio files.
- **Automatic File Cleanup:** Remove generated WAV files older than one hour during audio generation.
- **No External TTS API:** Generate speech without sending text to a third-party TTS service.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| Backend Framework | Flask |
| AI Model | Meta MMS VITS |
| Model Runtime | PyTorch / Transformers |
| Frontend | HTML, CSS, JavaScript |
| Audio Format | WAV |
| Model Storage | Local Filesystem |

## Requirements

- Python 3.10 or later
- Required Python dependencies
- Locally downloaded Meta MMS Urdu TTS model files

## Installation

Clone the repository and navigate to the project directory.

```powershell
git clone <your-repository-url>
cd VoiceCraft-AI
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Model Configuration

VoiceCraft AI uses the [Meta MMS Urdu TTS Model](https://huggingface.co/facebook/mms-tts-urd-script_arabic).

Download the model files and place them inside the `urdu_model/` directory.

Ensure the directory contains the required configuration, tokenizer, and model weight files, including:

- `config.json`
- Tokenizer and vocabulary files
- `pytorch_model.bin` or `model.safetensors`

The model weights are excluded from Git because of their large file size.

**Important — Model License:** The upstream Meta MMS Urdu TTS model is licensed under CC BY-NC 4.0. Review its licensing conditions before using or distributing the model, particularly for commercial applications.

## Running the Application

Start the Flask application:

```powershell
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

Enter your Urdu text and select **Generate Neural Audio** to generate and play the speech.

The model is loaded into memory when the server starts, allowing subsequent requests to use the loaded model.

## REST API

VoiceCraft AI also provides a JSON-based REST API for integrating Urdu speech generation into other applications.

**Endpoint**

```http
POST /api/tts
```

**Request Body**

```json
{
  "text": "آپ کیسے ہیں؟"
}
```

**Successful Response**

```json
{
  "audio_url": "/static/audio/voice_<id>.wav"
}
```

The API returns the URL of the generated WAV audio file.

Empty or invalid input returns a JSON error response.

## Project Structure

```text
VoiceCraft-AI/
│
├── app.py                  # Flask routes and model inference
├── requirements.txt        # Python dependencies
│
├── urdu_model/             # Local MMS Urdu TTS model files
│
├── static/
│   └── audio/              # Generated WAV audio files
│
└── templates/
    └── index.html          # Web application interface
```

## Architecture Overview

1. **Text Input:** The user enters Urdu text through the web interface.
2. **Request Processing:** Flask receives and validates the input.
3. **Model Inference:** The locally loaded MMS VITS model processes the Urdu text.
4. **Audio Generation:** The model generates speech and saves it as a WAV file.
5. **Audio Playback:** The application returns the audio URL for browser playback.
6. **File Management:** Old generated audio files are automatically cleaned up during audio generation.

## Development Notes

- Model weights must be downloaded and configured locally before running the application.
- The first startup requires loading the model into memory.
- Generated audio files are stored in `static/audio/`.
- The Flask development server is intended for local development and testing, not production deployment.

## License

The application source code and the upstream Meta MMS model have separate licensing considerations. Refer to the model's [CC BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/) before using or distributing the model.

---

**VoiceCraft AI — Making Urdu Speech Generation Accessible Through Local AI.**