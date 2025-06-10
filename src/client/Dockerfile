FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    alsa-utils \
    portaudio19-dev \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "voice_assistant.py"]
