import json

import isodate

from src.getyoutube import Getyoutube
from pytube import Playlist
import datetime

from src.video import Video


class PlayList(Getyoutube):
    """
    Класс плей-листа с ютуб-канала
    """

    def __init__(self, playlist_id: str) -> None:
        # информация о плейлисте
        self.__playlist_id = playlist_id  # id плей-листа
        playlist_videos = Playlist(f'https://www.youtube.com/playlist?list=' + self.__playlist_id)
        self.title = playlist_videos.title  # название плейлиста
        self.url = playlist_videos.playlist_url  # url плейлиста

    @property
    def total_duration(self) -> object:
        """
        Возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста.
        """
        youtube = self.get_service()

        # Получение данных по видеороликам в плейлисте.
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        # Получение всех id видеороликов в плейлисте.
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Получение длительности видеороликов плейлиста
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        # Получение общей длительности видеороликов плейлиста
        total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)

            # Получаем часы, минуты, секунды
            h, m, s = map(int, str(duration).split(':'))

            # Получаем общую продолжительность плейлиста (ч:м:с)
            total_time += datetime.timedelta(hours=h, minutes=m, seconds=s)

        return total_time

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        youtube = self.get_service()

        # Получение данных по видеороликам в плейлисте.
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        # Получение всех id видеороликов в плейлисте.
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Создаём экземпляры класса Video и проверяем количество лайков,
        # находим максимальное значение, выводим ссылку на видео.
        maximum = 0  # максимальное количество лайков
        max_link = ''  # ссылка на самое популярное видео
        for video_id in video_ids:
            video = Video(video_id)
            if int(video.like_count) > maximum:
                maximum = int(video.like_count)
                max_link = video.link

        return max_link

    # @staticmethod
    # def print_info(playlist_videos: object) -> None:
    #     """Выводит в консоль информацию о видео."""
    #     print(json.dumps(playlist_videos, indent=2, ensure_ascii=False))
