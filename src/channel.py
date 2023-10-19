import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    youtube = None  # объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        # Вызываем функцию, создающую объект для работы с API
        youtube = self.get_service()
        self.__channel_id = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = self.__channel_id['items'][0]['id']  # id канала
        self.title = self.__channel_id['items'][0]['snippet']['title']  # название канала
        self.description = self.__channel_id['items'][0]['snippet']['description']  # описание канала
        self.url = 'https://www.youtube.com/channel/' + self.id  # ссылка на канал
        self.subscriber_count = self.__channel_id['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.__channel_id['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count = self.__channel_id['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel_id, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> object:
        """
        Возвращает объект для работы с YouTube API
        """
        # Ключ для работы с API с ютуба.
        api_key: str = os.getenv('YT_API_KEY')
        # Создаём специальный объект для работы с API
        cls.youtube = build('youtube', 'v3', developerKey=api_key)
        return cls.youtube

    @property
    def channel_id(self) -> dict:
        """Получение значения защищённого атрибута (getter),
        изменить channel_id нельзя"""
        return self.__channel_id

    def to_json(self, name_json: str) -> None:
        """
        Сохраняет данные в json файл
        """
        # Путь для хранения файла (полное имя файла).
        path_json = os.path.join('..', 'src', 'data', name_json)
        # Создаём словарь из данных атрибутов экземпляра класса
        content = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        # Открытие, очистка файла и запись в него новых данных
        with open(path_json, 'w', encoding='utf-8') as file:
            # ensure_ascii=False - решает проблему с русской кодировкой
            json.dump(content, file, ensure_ascii=False, indent=2)


