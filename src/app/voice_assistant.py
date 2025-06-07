import sys
import queue
import sounddevice as sd
import vosk
import json
import requests
# from playsound import playsound
import subprocess

# API_URL = "http://localhost:8000/generate"
API_URL = "http://192.168.1.29:8000/generate"

DEVICE_ID = 1  # Mic ID
MODEL_PATH = "/mnt/ssd/vosk_models/vosk-model-small-pl"
# BLOCKSIZE = 8000
BLOCKSIZE = 0
# SAMPLERATE = 16000

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
sd.default.device = (DEVICE_ID, -1)

with sd.RawInputStream(samplerate=samplerate, blocksize=BLOCKSIZE, dtype='int16',
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
                    response = requests.post(API_URL, json={"prompt": text}, timeout=60)
                    response.raise_for_status()
                    json_response = response.json()
                    
                    print(f"🤖 Response: {json_response['response']}")

                    # wav_path = json_response["audio_file"]
                    wav_path = "/mnt/ssd/phi_models/output.wav"
                    print(f"🔊 Playing {wav_path}")
                    # playsound(wav_path)
                    subprocess.run(["aplay", wav_path])
                except Exception as e:
                    print(f"❌ Request error {e}")
        else:
            pass
