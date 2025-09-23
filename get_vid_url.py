import scrapetube

videos = scrapetube.get_channel(channel_id)
for video in videos:
    print("https://www.youtube.com/watch?v="+str(video['videoId']))
