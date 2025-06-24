from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from starlette.responses import Response
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
        # فك الرابط المختصر (مثل vt.tiktok.com أو youtu.be)
        response = requests.get(url, allow_redirects=True)
        final_url = response.url

        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOADS_DIR, filename)

        # إعدادات التحميل العادية
        ydl_opts = {
            'outtmpl': filepath,
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4',
        }

        # شرط خاص لإزالة العلامة المائية فقط لتيك توك
        if "tiktok.com" in final_url:
            ydl_opts['extractor_args'] = {
                'tiktok': {
                    'no_wm': 'True',
                }
            }

        try:
            # المحاولة الأساسية
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([final_url])
        except Exception:
            # لو فشل، نجرب باستخدام force_generic_extractor
            ydl_opts['force_generic_extractor'] = True
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([final_url])

        # إرسال الفيديو مباشرة للتحميل
        return Response(
            content=open(filepath, 'rb').read(),
            media_type='video/mp4',
            headers={
                "Content-Disposition": f"attachment; filename=downloaded_video.mp4"
            }
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
