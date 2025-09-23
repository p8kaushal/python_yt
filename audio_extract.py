import yt_dlp

video_url = "https://www.youtube.com/watch?v=7ARBJQn6QkM"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',  # Or '0' for automatic best
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
