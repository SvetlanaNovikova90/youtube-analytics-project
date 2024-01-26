import os

from googleapiclient.discovery import build

from helper.youtube_api_manual import youtube, printj


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = 'YT_API_KEY'

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self, ) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(channel)



