import scrapetube
import argparse
import asyncio
from prisma import Prisma
import yt_dlp
import whisper
from dotenv import load_dotenv
import os


async def store() -> None:
    print("Storing...")
    prisma = Prisma()
    await prisma.connect()

    contentGroup = await prisma.contentgroup.create(
        data={
            'ref': args.value,
            'type': 'Channel' if args.command.strip().lower() == 'channel' else 'Playlist' if args.command.strip().lower() == 'playlist' else 'Search' if args.command.strip().lower() == 'search' else 'Direct',
            'source': 'Youtube',
        },
    )

    for video in videos:
        if args.command.strip().lower() == "direct":
            video_url = video['videoId']
        else:
            video_url = "https://www.youtube.com/watch?v="+str(video['videoId'])
        print(video_url)
        # write your queries here
        title = ""
        if args.command.strip().lower() != "direct":
            title = video['title']['runs'][0]['text'] if 'runs' in video.get('title', {}) else video.get('title', {}).get('simpleText', '')
        else:
            title = video_url

        content = await prisma.content.create(
            data={
            'grpId': contentGroup.id,
            'title': title,
            'description': '',
            'url': video_url,
            'thumbnail': '',
            'viewCount': 0,
            'length': 0,
            'type': 'video',
            },
        )
        
        ydl_opts = {
            'format': 'bestaudio/best',
            # 'outtmpl': '%(title)s.%(ext)s',
            'outtmpl': '%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Or '0' for automatic best
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Transcribe the audio file (supports wav, mp3, m4a, and more)
        result = model.transcribe(f"{video['videoId']}.mp3")

        transcript_path = f"{video['videoId']}.txt"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result.get("text", ""))

        print(f"Saved transcript to {transcript_path}")

        # remove the downloaded audio file to save space
        # try:
        #     os.remove(f"{video['videoId']}.mp3")
        # except OSError:
        #     pass

    await prisma.disconnect()

if __name__ == '__main__':
    # Load a Whisper model: options are tiny, base, small, medium, large
    model = whisper.load_model("base")

    # Load environment variables from .env file
    load_dotenv()

    # # Access the variables
    # database_url = os.getenv('SUPABASE_URL')
    # api_secret = os.getenv('SUPABASE_ANON_KEY')

    parser = argparse.ArgumentParser(description="A script that downloads YouTube videos and stores metadata in a database.")
    parser.add_argument("-c", "--command", type=str, help="channel||playlist||search||direct", default="channel")
    parser.add_argument("-v", "--value", type=str, help="Channel ID||Playlist ID||Search Query||Direct URL", default="UCedIWVVm-tkgAoZYQiT7Fvw")

    args = parser.parse_args()
    print(f"Command: {args.command}")
    print(f"Value: {args.value}")

    match args.command.strip().lower():
        case "channel":
            print("Channel...")
            videos = scrapetube.get_channel(args.value)

        case "playlist":
            print("Playlist...")
            videos = scrapetube.get_playlist(args.value)

        case "search":
            print("Searching...")
            videos = scrapetube.get_search(args.value)

        case "direct":
            print("extracting...")
            videos = [{'videoId': args.value}]

        case _: # Wildcard pattern, acts as a default case
            print("Unknown command.")   

    asyncio.run(store())