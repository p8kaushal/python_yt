import scrapetube
import argparse
import asyncio
from prisma import Prisma

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# # Access the variables
# database_url = os.getenv('SUPABASE_URL')
# api_secret = os.getenv('SUPABASE_ANON_KEY')

parser = argparse.ArgumentParser(description="A script that processes command-line arguments.")
parser.add_argument("-c", "--command", type=str, help="channel||playlist||search", default="channel")
parser.add_argument("-v", "--value", type=str, help="Channel ID||Playlist ID||Search Query", default="UCedIWVVm-tkgAoZYQiT7Fvw")

args = parser.parse_args()

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

    case _: # Wildcard pattern, acts as a default case
        print("Unknown command.")

async def store() -> None:
    prisma = Prisma()
    await prisma.connect()

    contentGroup = await prisma.contentgroup.create(
        data={
            'ref': args.value,
            'type': 'Channel' if args.command.strip().lower() == 'channel' else 'Playlist' if args.command.strip().lower() == 'playlist' else 'Search',
            'source': 'Youtube',
        },
    )

    for video in videos:
        print("https://www.youtube.com/watch?v="+str(video['videoId']))
        # write your queries here
        content = await prisma.content.create(
            data={
                'grpId': contentGroup.id,
                'title': video['title']['runs'][0]['text'] if 'runs' in video['title'] else video['title']['simpleText'],
                'description': '',
                'url': "https://www.youtube.com/watch?v="+str(video['videoId']),
                'thumbnail': '',
                'viewCount': 0,
                'length': 0,
                'type': 'video',
            },
        )

    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(store())