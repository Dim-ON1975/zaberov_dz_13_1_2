import os
from googleapiclient.discovery import build


class Getyoutube:
    """Класс, возвращающий объект для работы с YouTube API"""
    youtube = None  # объект для работы с API

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
