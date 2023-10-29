import os
import json

from src.getyoutube import Getyoutube


class Channel(Getyoutube):
    """Класс для ютуб-канала"""

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

    def __str__(self) -> str:
        """
        Возвращает удобочитаемое (или неформальное)
        строковое представление наименования канала и url-ссылки на него
        """
        return f'{self.title} {self.url}'

    def __add__(self, other) -> int:
        """
        Сложение количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        """
        Вычитание количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        """
        Сравнение (>) количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other) -> bool:
        """
        Сравнение (>=) количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other) -> bool:
        """
        Сравнение (<) количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other) -> bool:
        """
        Сравнение (<=) количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other) -> bool:
        """
        Сравнение (==) количества подписчиков двух каналов (экземпляров класса)
        """
        return int(self.subscriber_count) == int(other.subscriber_count)
