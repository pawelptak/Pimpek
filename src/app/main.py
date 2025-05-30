from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import argostranslate.package
import argostranslate.translate
from tts import synthesize_to_wav

app = FastAPI()

llm = Llama(
    model_path="/models/phi3mini.gguf",
    #model_path="/mnt/ssd/phi_models/phi3mini.gguf",
    n_threads=4,
    # n_ctx=2048,
    verbose=False,
    # n_batch=64
)

class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate(request: PromptRequest):
    input_prompt_pl = request.prompt.strip()
    input_prompt_en = translate_text(input_prompt_pl, "pl", "en")
    # formatted_prompt = f"<|user|>\n{input_prompt_en}\n<|assistant|>\n"
    formatted_prompt = (
        "<|system|>\nYou are a helpful assistant that answers questions in short and friendly sentences.\n"
        "<|user|>\n" + input_prompt_en + "\n<|assistant|>\n"
    )

    response = llm(
        formatted_prompt,
        max_tokens=100,
        stop=["<|user|>", "<|assistant|>", "<|end|>"]
    )
    output_en = response['choices'][0]['text'].strip()
    # print(output_en)
    # print()

    output_pl = translate_text(output_en, "en", "pl")
    # print(output_pl)

    wav_path = synthesize_to_wav(output_pl)
    
    return {
        "response": output_pl,
        "audio_file": wav_path
    }

def ensure_package_installed(from_code: str, to_code: str):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    installed_languages = argostranslate.translate.get_installed_languages()
    installed_codes = [lang.code for lang in installed_languages]

    # Check if from_code->to_code package exists among installed
    from_lang = next((l for l in installed_languages if l.code == from_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_code), None)
    
    if from_lang and to_lang:
        if from_lang.get_translation(to_lang):
            # Already installed
            return

    # Install the package
    package_to_install = next(
        (p for p in available_packages if p.from_code == from_code and p.to_code == to_code),
        None,
    )
    if package_to_install:
        path = package_to_install.download()
        argostranslate.package.install_from_path(path)
    else:
        raise ValueError(f"No package available for {from_code} -> {to_code}")

ensure_package_installed("en", "pl")
ensure_package_installed("pl", "en")

def translate_text(text: str, from_code: str, to_code: str) -> str:
    return argostranslate.translate.translate(text, from_code, to_code)

if __name__ == "__main__":
    # polish_in = "Jak się dzisiaj czujesz?"
    # english_out = translate_text(polish_in, "pl", "en")
    # print("PL ➜ EN:", english_out)

    # english_in = "Where is this car?"
    # polish_out = translate_text(english_in, "en", "pl")
    # print("EN ➜ PL:", polish_out)

    result = generate(PromptRequest(prompt="Jak się masz?"))
    print("Bot response:", result["response"])
    print("Audio file saved to:", result["audio_file"])

