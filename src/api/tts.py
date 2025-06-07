import subprocess
from pathlib import Path
import yaml
import uuid

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

PIPER_MODEL_PATH = config["piper_model_path"]
PIPER_BINARY = "piper"  # or absolute path if not in $PATH
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def synthesize_to_wav(text: str) -> str:
    output_filename = f"{uuid.uuid4()}.wav"
    output_file = OUTPUT_DIR / output_filename

    for file in OUTPUT_DIR.glob("*"):
        if file.is_file():
            file.unlink()

    try:
        result = subprocess.run(
            [
                PIPER_BINARY,
                "--model", PIPER_MODEL_PATH,
                "--output_file", str(output_file),
            ],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Return code:", e.returncode)
        print("Command:", e.cmd)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        raise

    return str(output_filename)

if __name__ == "__main__":
    synthesize_to_wav("Dzień dobry")