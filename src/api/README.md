# API
A web API that uses a LLM to generate prompt responses.

## Methods

### POST /generate
Generate a response from the given prompt.

#### Request body
```
{
    "prompt": "Jaka jest stolica Polski?"
}
```

#### Response
```
{
        "response": "Stolicą Polski jest Warszawa.",
        "audio_file": "path/to/the/synthesized/answer/audio"
}
```

### POST /reset
Manually clear the model's conversation context.

#### Response
```
{
    "message": "Context reset"
}
```

# Usage
1. Edit `config.yml` and adjust all the settings to your configuration.
2. `python -m venv venv`
3. `venv/Scripts/activate` (Windows) or `source \venv\bin\activate` (Linux)
4. `pip install -r requirements.txt`
5. `uvicorn api:app --host 0.0.0.0 --port 8000`
OR
6. `docker compose up -d`