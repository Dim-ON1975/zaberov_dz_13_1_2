import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        # Ключ для работы с API с ютуба.
        api_key: str = os.getenv('YT_API_KEY')
        # Создаём специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_id = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
