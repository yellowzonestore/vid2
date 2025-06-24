from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import os
import uuid
import requests  # ✅ مضافة لفك الروابط المختصرة

app = FastAPI()

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# ✅ دالة فك الروابط المختصرة
def resolve_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception:
        return url  # fallback إذا فشل التحويل

@app.get("/download")
def download_tiktok(url: str = Query(...)):
    try:
        url = resolve_url(url)  # ✅ فك الرابط المختصر أولًا

        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOADS_DIR, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [],
            'merge_output_format': 'mp4',
            'extractor_args': {
                'tiktok': {
                    'embed_missings': 'False',
                    'noprogress': 'True',
                    'no_wm': 'True',  # ❗️المهم لإزالة العلامة المائية
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return FileResponse(path=filepath, media_type="video/mp4", filename="video.mp4")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
