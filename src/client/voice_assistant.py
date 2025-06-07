import sys
import queue
import sounddevice as sd
import vosk
import json
import requests
import subprocess
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

API_URL = config["api_url"]
DEVICE_ID = config["mic_device_id"]
MODEL_PATH = config["vosk_model_path"]

q = queue.Queue()

print(sd.query_devices())
print("Default input device:", sd.default.device[0])
print("Default output device:", sd.default.device[1])

def callback(indata, frames, time, status):
    if status:
        print("SoundDevice status:", status, file=sys.stderr)
    q.put(bytes(indata))

model = vosk.Model(MODEL_PATH)

device_info = sd.query_devices(kind='input')
samplerate = int(device_info["default_samplerate"])
sd.default.device = (DEVICE_ID, -1) # -1 means system default output device

with sd.RawInputStream(samplerate=samplerate, blocksize=0, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    print("🎙️ Speak now (Ctrl+C to stop)...")
    
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if text.strip():
                print(f"📝 Recognized: {text}")

                try:
                    response = requests.post(f"{API_URL}/generate", json={"prompt": text}, timeout=60)
                    response.raise_for_status()
                    json_response = response.json()
                    
                    print(f"🤖 Response: {json_response['response']}")

                    # wav_path = json_response["audio_file"]
                    wav_path = "/mnt/ssd/phi_models/output.wav"
                    print(f"🔊 Playing {wav_path}")
                    subprocess.run(["aplay", wav_path])
                except Exception as e:
                    print(f"❌ Request error {e}")
        else:
            pass
