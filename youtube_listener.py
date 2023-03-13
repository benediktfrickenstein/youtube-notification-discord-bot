import requests
import pickle
import json
import os


class YoutubeListener:
    def __init__(self, api_key: str, channel_id: str, logger) -> None:
        self.api_key = api_key
        self.channel_id = channel_id
        self.logger = logger
        self.file_path = f"{self.channel_id}.pickle"

    def load(self) -> list:
        videos = []
        if os.path.exists(self.file_path):
            if os.path.getsize(self.file_path) > 0:
                with open(self.file_path, "rb") as f:
                    videos = pickle.load(f)
        return videos

    def listen(self) -> str:
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date&maxResults=1"
        res = requests.get(url)
        data = json.loads(res.text)
        if "items" in data:
            video_id = data["items"][0]["id"]["videoId"]
            self.logger.info(f"YouTube Data API Request (Video ID: {video_id}).")
            return data["items"][0]["id"]["videoId"]
        self.logger.error(f"YouTube Data API Request: {data}")
        return ""

    def save(self, videos) -> None:
        with open(self.file_path, "wb") as f:
            pickle.dump(videos, f)
