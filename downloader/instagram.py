# downloader/instagram.py
from yt_dlp import YoutubeDL

def download_instagram(url):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {'url': info['url'], 'title': info.get('title', 'Instagram')}
    except Exception as e:
        return {'error': str(e)}
