import subprocess
from pathlib import Path

#PIPER_MODEL_PATH = "/mnt/ssd/piper_models/darkman/pl_PL-darkman-medium.onnx"
PIPER_MODEL_PATH = "piper_models/darkman/pl_PL-darkman-medium.onnx"
PIPER_BINARY = "piper"  # or absolute path if not in $PATH
OUTPUT_DIR = Path("/models")
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def synthesize_to_wav(text: str) -> str:
    # output_filename = OUTPUT_DIR / f"{uuid.uuid4()}.wav"
    # output_filename = f"{uuid.uuid4()}.wav"
    output_filename = OUTPUT_DIR / "output.wav"

    try:
        result = subprocess.run(
            [
                PIPER_BINARY,
                "--model", PIPER_MODEL_PATH,
                "--output_file", str(output_filename),
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
