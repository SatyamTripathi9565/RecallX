import requests
import speech_recognition as sr
from moviepy import VideoFileClip
import tempfile
from pydub import AudioSegment
from django.shortcuts import render

BASE_URL = "http://127.0.0.1:8000"


# =========================
# 🏠 HOME VIEW
# =========================
def home(request):
    data = None

    if request.method == "POST":
        input_type = request.POST.get("input_type")
        text = ""

        # 🔹 TEXT INPUT
        if input_type == "text":
            text = request.POST.get("memory")

        # 🔹 AUDIO INPUT
        elif input_type == "audio":
            audio_file = request.FILES.get("audio_file")

            if audio_file:
                recognizer = sr.Recognizer()

                try:
                    # Save file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
                        for chunk in audio_file.chunks():
                            temp_audio.write(chunk)

                    # Convert to WAV
                    sound = AudioSegment.from_file(temp_audio.name)
                    wav_path = temp_audio.name + ".wav"
                    sound.export(wav_path, format="wav")

                    # Recognize speech
                    with sr.AudioFile(wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.record(source, duration=6)
                        text = recognizer.recognize_google(audio)

                except Exception:
                    text = "❌ Audio processing failed"

        # 🔹 VIDEO INPUT
        elif input_type == "video":
            video_file = request.FILES.get("video_file")

            if video_file:
                recognizer = sr.Recognizer()

                try:
                    # Save video
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_video:
                        for chunk in video_file.chunks():
                            temp_video.write(chunk)

                    clip = VideoFileClip(temp_video.name)

                    if clip.audio is None:
                        text = "❌ No audio in video"
                    else:
                        audio_path = temp_video.name + ".wav"
                        clip.audio.write_audiofile(audio_path)

                        # Convert
                        sound = AudioSegment.from_file(audio_path)
                        sound.export(audio_path, format="wav")

                        # Recognize
                        with sr.AudioFile(audio_path) as source:
                            recognizer.adjust_for_ambient_noise(source)
                            audio = recognizer.record(source, duration=8)
                            text = recognizer.recognize_google(audio)

                except Exception:
                    text = "❌ Video processing failed"

        # 🔥 SEND TO FASTAPI
        if text:
            try:
                res = requests.post(
                    f"{BASE_URL}/add",
                    json={"text": text}
                )
                data = res.json()
            except Exception:
                data = {"message": "Backend not reachable ❌"}

    return render(request, "index.html", {"data": data})


# =========================
# 💬 CHAT VIEW (RECOMMENDED)
# =========================
def chat(request):
    result = None

    query = request.GET.get("query")
    output_type = request.GET.get("output_type")

    if query:
        try:
            res = requests.post(
                f"{BASE_URL}/chat",
                params={
                    "query": query,
                    "output_type": output_type
                }
            )
            result = res.json()
        except Exception:
            result = {"answer": "Backend not reachable ❌"}

    return render(request, "chat.html", {"result": result})