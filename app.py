from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import tempfile
import os

app = FastAPI()

# تفعيل الـ CORS عشان تطبيقك يقدر يكلم السيرفر بدون مشاكل أمنية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# صوت أكاني الكيوت (عربي)
VOICE = "ar-EG-SalmaNeural" 

@app.get("/")
def read_root():
    return {"status": "Akane Voice Server is Running! 💕"}

@app.get("/tts")
async def text_to_speech(text: str):
    if not text:
        return {"error": "No text provided"}

    # إنشاء ملف مؤقت لحفظ الصوت
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_path = temp_file.name
    temp_file.close()

    try:
        # تحويل النص لصوت كيوت
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(temp_path)

        # قراءة الصوت وإرساله للتطبيق
        with open(temp_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # مسح الملف المؤقت عشان السيرفر ما يتعبى
        os.remove(temp_path)

        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}
