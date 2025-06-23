from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from yt_dlp import YoutubeDL
from typing import Optional

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🎥 Video Downloader API is working!"}

@app.get("/download")
def download_video(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,
        }

        # تحايل لإزالة العلامة المائية من TikTok إن أمكن
        if 'tiktok.com' in url:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoRemuxer',
                'preferedformat': 'mp4',
            }]
            ydl_opts['force_generic_extractor'] = False

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for fmt in info.get('formats', []):
            if fmt.get('url') and fmt.get('ext') in ['mp4', 'webm']:
                formats.append({
                    'quality': fmt.get('format_note') or 
fmt.get('format'),
                    'resolution': f"{fmt.get('height', 'N/A')}p",
                    'ext': fmt.get('ext'),
                    'download_url': fmt.get('url')
                })

        result = {
            "title": info.get('title'),
            "thumbnail": info.get('thumbnail'),
            "duration": info.get('duration'),
            "available_formats": formats
        }
        return result

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": 
str(e)}, status_code=500)
