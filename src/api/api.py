from fastapi import FastAPI
from pydantic import BaseModel
from gpt4all import GPT4All
import argostranslate.translate
from tts import synthesize_to_wav
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

app = FastAPI()
model = GPT4All(model_name=config["gpt4all_model_file"], model_path=config["gpt4all_models_folder_path"])
installed_languages = argostranslate.translate.get_installed_languages()

MAX_HISTORY_MESSAGES = config["context_max_messages"]
chat_history = []

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(request: PromptRequest):
    input_prompt_pl = request.prompt.strip()
    input_prompt_en = translate_text(input_prompt_pl, "pl", "en")
    tiny_prompt  = build_prompt(input_prompt_en) # use this only for the tinyllama model (https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)

    # formatted_prompt = (
    #     input_prompt_en + "Answer in one short sentence."
    # )

    chat_history.append({"role": "user", "content": input_prompt_en})

    if len(chat_history) > MAX_HISTORY_MESSAGES:
        chat_history.pop(0)

    with model.chat_session():
        for message in chat_history:
            model.generate(message["content"], max_tokens=0)  # replay old content (no output)
        
        output_en = model.generate(tiny_prompt, max_tokens=100)

    chat_history.append({"role": "assistant", "content": output_en})

    output_pl = translate_text(output_en, "en", "pl")

    return {
        "response": output_pl
    }

@app.post("/reset")
def reset():
    chat_history.clear()
    return {"message": "Context reset"}

def translate_text(text: str, from_code: str, to_code: str) -> str:
    from_lang = next((l for l in installed_languages if l.code == from_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_code), None)
    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        if translation:
            return translation.translate(text)
    return text  # fallback

def build_prompt(prompt: str) -> str:
    return f"<|system|>\nYou are a helpful assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"

