"""Just models."""

from aiogram.fsm.state import State, StatesGroup


class FilmFromTitleForm(StatesGroup):
    """Форма для получения названия аниме/дорамы от пользователя."""

    film_type: str
    title = State()


class FilmFromGenreForm(StatesGroup):
    """Форма для получения жанра аниме/дорамы от пользователя."""

    film_type: str
    genre = State()


class FilmFromActorForm(StatesGroup):
    """Форма для получения актёра аниме/дорамы от пользователя."""

    film_type: str
    actor = State()


class FilmFromYearForm(StatesGroup):
    """Форма для получения года аниме/дорамы от пользователя."""

    film_type: str
    year = State()


class Dorama:
    def __init__(self, name: str, comments: str):
        self.name = name
        self.comments = comments

    def __str__(self):
        return f"{self.name} - {self.comments}"


class Anime:
    def __init__(self, name: str, comments: str):
        self.name = name
        self.comments = comments

    def __str__(self):
        return f"{self.name}- {self.comments}"
