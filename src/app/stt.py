import sys
import queue
import sounddevice as sd
import vosk
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

base_path = "/mnt/ssd/vosk_models/"
model = vosk.Model(base_path + "vosk-model-small-pl")

samplerate = 16000
device_info = sd.query_devices(kind='input')
# print(sd.query_devices())
# print("Default input device:", sd.default.device[0])
# print("Default output device:", sd.default.device[1])

# sd.default.device = (1, 0)

if device_info:
    samplerate = int(device_info['default_samplerate'])

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    print("Mów teraz...")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            print("Rozpoznano:", text)
            # tu możesz wysłać 'text' do endpointu chatbota /generate i odczytać odpowiedź
        else:
            partial = rec.PartialResult()
            # można tu obsługiwać częściowy tekst, ale nie jest konieczne
