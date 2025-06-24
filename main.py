from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import os
import uuid

app = FastAPI()

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def get_ydl_options(url, filepath):
    if "tiktok.com" in url:
        return {
            'outtmpl': filepath,
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'extractor_args': {
                'tiktok': {
                    'no_wm': 'True',
                }
            },
        }
    else:
        return {
            'outtmpl': filepath,
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4',
        }

@app.get("/download")
def download_tiktok(url: str = Query(...)):
    try:
        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOADS_DIR, filename)

        ydl_opts = get_ydl_options(url, filepath)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return FileResponse(path=filepath, media_type="video/mp4", filename="video.mp4")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
