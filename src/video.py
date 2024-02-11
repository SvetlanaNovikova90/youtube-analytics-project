from googleapiclient.discovery import build
import os


class Video:
    # Класс для видеоролика
    api_key: str = os.getenv('YT_API_KEY')
    _video: dict = None
    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title: str = self.video_response()['items'][0]['snippet']['title']
        self.view_count: int = self.video_response()['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response()['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.video_response()['items'][0]['statistics']['commentCount']

    def video_response(self) -> dict:
        '''проверяет информацию в славаре, если нет, возвращает информацию о видеоролике.'''
        if self._video is None:
            self._video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=self.video_id).execute()
        return self._video

    def __str__(self):
        return f'{self.video_title}'

    def __repr__(self):
        return f'{self.video_title, self.view_count, self.like_count, self.comment_count}'


class PLVideo(Video):
    _playlist_videos: dict = None

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def playlist_response(self) -> dict:
        """проверяет информацию в славаре, если нет, возвращает информацию о плейлисте."""
        if self._playlist_videos is None:
            self._playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50,
                                                                      ).execute()
        return self._playlist_videos


