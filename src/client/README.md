# Client
This is the actual voice assistant. It listens to the inputs from the mic and communicates with the API to get the response from the LLM model.

# Usage
1. Edit `config.yml` and adjust all the settings to your configuration.
2. `python -m venv venv`
3. `venv/Scripts/activate` (Windows) or `source \venv\bin\activate` (Linux)
4. `pip install -r requirements.txt`
5. `python voice_assistant.py`
6. Speak to your microphone and listen to the chatbot answer.