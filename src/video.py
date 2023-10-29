from src.getyoutube import Getyoutube


class Video(Getyoutube):
    def __init__(self, video_id):
        self.video_id = video_id  # id видео
        video_response = self.video_statistics(self.video_id)
        # self.print_info(video_response)
        self.video_title: str = video_response['items'][0]['snippet']['title']  # Название
        self.link: str = 'https://youtu.be/' + self.video_id  # ссылка на видео
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']  # Просмотры
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']  # Лайки

    def video_statistics(self, video_id: str) -> object:
        # Получение статистики видео по его id
        youtube = self.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        return video_response

    # def print_info(self, video_response: object) -> None:
    #     """Выводит в консоль информацию о видео."""
    #     print(json.dumps(video_response, indent=2, ensure_ascii=False))

    def __str__(self):
        return self.video_title

    def __repr__(self):
        return (f'{self.__class__.__name__}(video_id: {self.video_id}, video_title: {self.video_title},'
                f' link: {self.link}, view_count: {self.view_count}, like_count: {self.like_count})')


class PLVideo(Video):
    def __init__(self, video_id: str, play_list_id: str) -> None:
        super().__init__(video_id)
        self.play_list_id: str = play_list_id  # id плей-листа
