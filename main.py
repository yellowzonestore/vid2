from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import os
import uuid
import requests

app = FastAPI()

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.get("/download")
def download_video(url: str = Query(...)):
    try:
        # فك أي رابط مختصر (مثل vm.tiktok، youtu.be، bit.ly، إلخ)
        response = requests.get(url, allow_redirects=True)
        full_url = response.url

        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOADS_DIR, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4',
        }

        # TikTok فقط: نحاول نزيل العلامة المائية
        if "tiktok.com" in full_url:
            ydl_opts['extractor_args'] = {
                'tiktok': {
                    'no_wm': 'True'
                }
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([full_url])

        return FileResponse(path=filepath, media_type="video/mp4", filename="video.mp4")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
