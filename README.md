# Offline Python Voice Assistant

A local, Python-based voice assistant with custom wake-word activation. It uses `SpeechRecognition` and `pyttsx3` to handle tasks, system controls, and web navigation fully offline.

## Features

- Wake-word activation (`assistant`, `hey assistant`, `okay assistant`, `wake up`)
- Offline speech recognition with PocketSphinx
- Text-to-speech responses via `pyttsx3`
- Basic system controls: lock computer, volume up/down/mute, shutdown, restart
- Open common Windows apps: Notepad, Calculator, File Explorer
- Web navigation and search using the default browser
- Time and date responses

## Setup

1. Create and activate a Python virtual environment.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the assistant:

```powershell
python voice_assistant.py
```

## Notes

- This assistant relies on PocketSphinx for offline speech recognition.
- If `pocketsphinx` is not installed, the assistant will prompt you to install it.
- The script is designed for Windows and uses native Windows APIs for volume and locking.

## Usage

1. Run `python voice_assistant.py`.
2. Say the wake word, for example: "assistant".
3. Speak a command such as:
   - "open browser"
   - "search for weather"
   - "open notepad"
   - "lock computer"
   - "volume up"
   - "shutdown"

## License

This project is provided as-is for local offline voice automation.
