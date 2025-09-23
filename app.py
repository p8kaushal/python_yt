import yt_dlp

url = "https://www.youtube.com/watch?v=7ARBJQn6QkM"
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
