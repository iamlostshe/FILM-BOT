"""Documentation for this module.

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


class API:
    """class for interacting with api."""

    def __init__(self) -> None:
        """Just init function."""
        self.session = ClientSession()

    async def _request(self, url: str, params: dict[str:any]) -> any:
        """Do a request."""
        async with self.session.get(URL + url, headers=HEADERS, params=params) as r:
            status_code = r.status
            if status_code == 200:  # noqa: PLR2004
                return json.loads(await r.text())
        logger.error("Сервер вернул неожиданный статус-код: {}", status_code)
        return None

    async def genre_search(self, message_text: str, film_type: str) -> str:
        """Func for search by genre.

        :param message: user's message
        :param type: anime or dorama
        :return: result (anime or dorama)
        """
        message = "".join(message_text.split())
        genres = message.split(",")

        params = {
            "notNullFields": ["name", "description"],
            "genres.name": genres,
        }

        if film_type == "аниме":
            params["type"] = ["anime"]
        else:
            params["type"] = ["tv-series"]
            params["countries.name"] = ["Корея Южная", "Япония", "Китай"]

        data = await self._request("movie", params)
        if data:
            docs = data["docs"]
            return "\n".join(
                [
                    f"{i + 1}. {film['name']}, {film['year']}\n\n{
                        textwrap.fill(film['description'], 100)
                    }"
                    for i, film in enumerate(docs)
                ],
            )

        return "Не удалось получить данные."

    async def title_search(self, message_text: str) -> str:
        """Func for searching by name.

        :param message: user's message
        :return: result (anime or dorama)
        """
        params = {
            "query": message_text,
        }
        data = await self._request("movie/search", params=params)
        if data:
            docs = data["docs"][0]
            return f"{docs['name']}, {docs['year']}\n\n{
                textwrap.fill(docs['description'], 100)
            }"

        return "Не удалось получить данные."

    async def actor_search(self, message_text: str) -> str:
        """Func for searching by actor.

        :param message: user's message
        :return: result (anime or dorama)
        """
        actor = message_text.replace(", ", ",").split(",")

        params = {
            "query": actor,
        }
        data = await self._request("person/search", params=params)
        if data:
            actor_id = data["docs"][0]["id"]

            params = {
                "notNullFields": ["description"],
                "type": ["tv-series"],
                "countries.name": ["Корея Южная", "Япония", "Китай"],
            }

            data = await self._request(
                f"movie?page=1&limit=10&persons.id={actor_id}",
                params=params,
            )

            if data:
                docs = data["docs"]
                return "\n".join(
                    [
                        f"{i + 1}. {film[i]['name']}, {film[i]['year']}\n\n{
                            textwrap.fill(film[i]['description'], 100)
                        }"
                        for i, film in enumerate(docs)
                    ],
                )
        return "Не удалось получить данные."

    async def year_search(self, message_text: str, film_type: str) -> str:
        """Func for searching by years.

        :param message: user's message
        :param type: anime or dorama
        :return: result (anime or dorama)
        """
        year = message_text.replace(" ", "")

        params = {
            "notNullFields": ["name", "description"],
            "year": year,
        }

        if film_type == "аниме":
            params["type"] = ["anime"]
        else:
            params["type"] = ["tv-series"]
            params["countries.name"] = ["Корея Южная", "Япония", "Китай"]

        data = await self._request("movie", params=params)
        if data:
            docs = data["docs"]
            return "\n".join(
                [
                    f"{i + 1}. {film['name']}, {film['year']}\n\n{
                        textwrap.fill(film['description'], 100)
                    }"
                    for i, film in enumerate(docs)
                ],
            )

        return "Не удалось получить данные."

    async def random_dorama(self, film_type: str) -> str:
        """Func for searching random dorama.

        :param type: anime or dorama
        :return: result (anime or dorama)
        """
        if film_type == "аниме":
            params = {
                "notNullFields": ["name", "description"],
                "type": ["anime"],
            }
        else:
            params = {
                "notNullFields": ["name", "description"],
                "type": ["tv-series"],
                "countries.name": ["Корея Южная", "Япония", "Китай"],
            }

        data = await self._request("movie/random", params=params)
        if data:
            return f"{data["name"]}, {data["year"]}\n\n{
                textwrap.fill(data["description"], 100)
            }"

        return "Не удалось получить данные."
