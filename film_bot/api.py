"""Модуль для взаимодейсктвия с API.

Телеграм бот реализован с помощью библиотеки telebot, позволяющей работать с
Telegram Bot API.
Для работы с базой данных используется библиотека sqlite3, позволяющая формировать
запросы к облегченной базе данных.

Работа бота осуществляется классом DoranimeBot и сопутствующими функциями для работы с
базой данных, для обращения к API Кинопоиска.
Для удобства использования добавлены кнопки в основное меню.
Запуск бота осуществляется с помощью файла "Main.py".
"""

# @section author_doxygen_example Author(s)
# Created by:
# * Pustovalova Sofya Alekseevna
# * Zavyalova Polina Igorevna
# * Peeva Olesya Romanovna
# * Kramarenko Yuri Andreevich
# on 16/06/2024.

import json
import textwrap

from aiohttp import ClientSession
from loguru import logger

from film_bot.config import config

URL = "https://api.kinopoisk.dev/v1.4/"
HEADERS = {"X-API-KEY": config.kinopoisk_api_key}


def get_params(film_type: str) -> dict[str:any]:
    """Func for get params by film type."""
    params = {
        "notNullFields": ["name", "description"],
    }

    if film_type == "аниме":
        params["type"] = ["anime"]

    elif film_type == "дорама":
        params["type"] = ["tv-series"]
        params["countries.name"] = ["Корея Южная", "Япония", "Китай"]

    return params


def normalize_user_input(user_input: str) -> list:
    """Func to normalize user input."""
    return user_input.replace(", ", ",").split(",")


class API:
    """Class for interacting with API."""

    async def init(self) -> None:
        """Just init function."""
        self.session = ClientSession(base_url=URL)

    async def _request(self, url: str, params: dict[str:any]) -> any:
        """Do a request."""
        async with self.session.get(url, headers=HEADERS, params=params) as r:
            status_code = r.status
            if status_code == 200:  # noqa: PLR2004
                text = await r.text()
                logger.debug(text)
                return json.loads(text)
        logger.error("Сервер вернул неожиданный статус-код: {}", status_code)
        return None

    async def from_genre(self, genres: str, film_type: str) -> str:
        """Func for search by genre.

        :param message: user's message
        :param film_type: anime or dorama
        :return: result (anime or dorama)
        """
        # Forming request parameters
        params = get_params(film_type)
        params["genres.name"] = normalize_user_input(genres)

        # Sending a request to the API
        data = await self._request("movie", params)
        if data:
            docs = data["docs"]
            # Forming a message
            return "\n".join(
                [
                    f"{i + 1}. {film['name']}, {film['year']}\n\n{
                        textwrap.fill(film['description'], 100)
                    }"
                    for i, film in enumerate(docs)
                ],
            )

        return "Не удалось получить данные."

    async def from_title(self, query: str, film_type: str) -> str:
        """Func for searching by name.

        :param query: user's query
        :param film_type: anime or dorama
        :return: result (anime or dorama)
        """
        # Forming request parameters
        params = get_params(film_type)
        params["query"] = query

        # Sending a request to the API
        data = await self._request("movie/search", params=params)
        if data:
            docs = data["docs"][0]
            # Forming a message
            return f"{docs['name']}, {docs['year']}\n\n{
                textwrap.fill(docs['description'], 100)
            }"

        return "Не удалось получить данные."

    async def from_actor(self, actor: str, film_type: str) -> str:
        """Func for searching by actor.

        :param message: user's message
        :param film_type: anime or dorama
        :return: result (anime or dorama)
        """
        # Forming request parameters
        params = {"query": normalize_user_input(actor)}

        # Sending a request to the API
        data = await self._request("person/search", params=params)
        if data:
            actor_id = data["docs"][0]["id"]

            # Forming request parameters
            params = get_params(film_type)
            params["persons.id"] = actor_id
            params["page"] = 1
            params["limit"] = 10

            # Sending a request to the API
            data = await self._request("movie", params=params)
            if data:
                docs = data["docs"]
                # Forming a message
                return "\n".join(
                    [
                        f"{i + 1}. {film[i]['name']}, {film[i]['year']}\n\n{
                            textwrap.fill(film[i]['description'], 100)
                        }"
                        for i, film in enumerate(docs)
                    ],
                )

        return "Не удалось получить данные."

    async def from_year(self, year: str, film_type: str) -> str:
        """Func for searching by years.

        :param message: user's message
        :param type: anime or dorama
        :return: result (anime or dorama)
        """
        # Forming request parameters
        params = get_params(film_type)
        params["year"] = year

        # Sending a request to the API
        data = await self._request("movie", params=params)
        if data:
            docs = data["docs"]
            # Forming a message
            return "\n".join(
                [
                    f"{i + 1}. {film['name']}, {film['year']}\n\n{
                        textwrap.fill(film['description'], 100)
                    }"
                    for i, film in enumerate(docs)
                ],
            )

        return "Не удалось получить данные."

    async def random(self, film_type: str) -> str:
        """Func for searching random dorama.

        :param type: anime or dorama
        :return: result (anime or dorama)
        """
        # Forming request parameters
        params = get_params(film_type)

        # Sending a request to the API
        data = await self._request("movie/random", params=params)
        if data:
            # Forming a message
            return f"{data['name']}, {data['year']}\n\n{
                textwrap.fill(data['description'], 100)
            }"

        return "Не удалось получить данные."
