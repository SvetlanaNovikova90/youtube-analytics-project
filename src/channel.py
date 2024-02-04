from googleapiclient.discovery import build

from helper.youtube_api_manual import youtube, printj, video_response


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = 'YT_API_KEY'

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.all_otr = []

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @classmethod
    def get_service(cls):
        '''класс-метод, возвращающий объект для работы с YouTube API'''
        return cls.youtube

    @property
    def channel_id(self):
        '''выводит приватный id'''
        return self.__channel_id
    def response(self):
        '''достает из списка атрибуты
        название канала
        описание канала
        ссылка на канал
        количество подписчиков
        количество видео
        общее количество просмотров'''
        channel_otrib = []
        channel_response = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_title: str = channel_response['items'][0]['snippet']['title']
        channel_otrib.append(channel_title)
        video_Count: str = channel_response['items'][0]['statistics']['videoCount']
        channel_otrib.append(video_Count)
        url_count: str = channel_response['items'][0]['snippet']['thumbnails']['default']['url']
        channel_otrib.append(url_count)
        channel_description: str = channel_response['items'][0]['snippet']['description']
        channel_otrib.append(channel_description)
        subscriber_count: str = channel_response['items'][0]['statistics']['subscriberCount']
        channel_otrib.append(subscriber_count)
        view_Count: str = channel_response['items'][0]['statistics']['viewCount']
        channel_otrib.append(view_Count)

        return channel_otrib
    @property
    def title(self):
        return self.response()[0]

    @property
    def video_count(self):
        return self.response()[1]

    @property
    def url(self):
        return self.response()[2]

    @property
    def subscriber_count(self):
        return self.response()[5]

    def print_info(self, ) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(channel)

    def to_json(self,file_new):
        '''Записыват атрибуты в файл'''
        self.all_otr.append(self.channel_id)
        self.all_otr.append(self.response())
        print(self.all_otr, file=open(file_new, 'a'))








