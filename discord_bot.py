from youtube_listener import YoutubeListener
import logging
import discord
import asyncio
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler("discord_bot.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

youtube_listener = YoutubeListener(
    api_key=config["youtube"]["api_key"],
    channel_id=config["youtube"]["channel_id"],
    logger=logger,
)
videos = youtube_listener.load()


class MyClient(discord.Client):
    async def on_ready(self):
        client.loop.create_task(self.youtube_listener_task())

    async def youtube_listener(self):
        youtube_channel = client.get_channel(config["youtube"]["channel_id"])
        video_id = youtube_listener.listen()
        if not video_id == "" and not video_id in videos:
            await youtube_channel.send(
                f'{config["messages"]["new_video"]}https://www.youtube.com/watch?v={video_id}'
            )
            videos.append(video_id)

    async def youtube_listener_task(self):
        await client.wait_until_ready()
        while not client.is_closed():
            await client.youtube_listener()
            await asyncio.sleep(int(config["youtube"]["interval"]))


intents = discord.Intents.default()

client = MyClient(intents=intents)
client.run(config["discord"]["token"])

youtube_listener.save(videos)
