from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Akane Multi-Language Voice Server is Running! 💕"}

@app.get("/tts")
async def text_to_speech(text: str, lang: str = "ar"):
    if not text:
        return {"error": "No text provided"}

    # اختيار الصوت حسب لغة التطبيق (عربي أو إنجليزي)
    if lang == "en":
        voice = "en-US-AriaNeural"  # صوت إنجليزي كيوت وواضح
    else:
        voice = "ar-EG-SalmaNeural" # صوت عربي رقيق وطبيعي

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_path = temp_file.name
    temp_file.close()

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_path)

        with open(temp_path, "rb") as audio_file:
            audio_data = audio_file.read()

        os.remove(temp_path)

        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}
