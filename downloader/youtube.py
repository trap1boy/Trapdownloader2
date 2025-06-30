from yt_dlp import YoutubeDL

def download_youtube(url):
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "url": info.get("url") or info.get("webpage_url")
            }
    except Exception as e:
        return {"error": str(e)}
