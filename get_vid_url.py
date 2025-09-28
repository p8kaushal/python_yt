import scrapetube
import argparse

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
database_url = os.getenv('SUPABASE_URL')
api_secret = os.getenv('SUPABASE_ANON_KEY')

print(f"Database URL: {database_url}")
print(f"API Secret: {api_secret}")


from supabase import create_client, Client

supabase: Client = create_client(database_url, api_secret)


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


for video in videos:
    print("https://www.youtube.com/watch?v="+str(video['videoId']))
