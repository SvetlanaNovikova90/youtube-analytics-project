from googleapiclient.discovery import build
import os
import isodate
import datetime

class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    _playlist_data = None
    _video_response = None

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id
        self.playlist_title = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.title = self.playlist_title['items'][0]['snippet']['title']
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_response()['items']]
        self.right_id = ''

    def video_response(self) -> dict:
        """Возвращает информацию о видео."""
        if self._video_response is None:
             self._video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                                id=','.join(self.video_ids)
                                                                ).execute()
        return self._video_response
    @property
    def total_duration(self) -> datetime.timedelta:
        """Длительносить плейлиста"""
        playlist_duration = datetime.timedelta()
        for video in self.video_response()['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            playlist_duration += datetime.timedelta(seconds=duration.total_seconds())
        return playlist_duration

    def playlist_response(self) -> dict:
        """Возвращает информацию о плейлисте."""
        if self._playlist_data is None:
            self._playlist_data = (self.youtube.playlistItems().list(
                playlistId=self.playlist_id, part='contentDetails,snippet').execute())
        return self._playlist_data

    def show_best_video(self) -> str:
        """Показывает видео с наибольшим количеством лайков из плейлиста."""
        more_likes = 0
        for video in self.video_response()['items']:
            like_count= video['statistics']['likeCount']
            video_id = video['id']
            if int(like_count) > int(more_likes):
                more_likes = like_count
                self.right_id = video_id
        return f"https://youtu.be/{self.right_id}"

