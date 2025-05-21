"""launching the bot."""

import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from film_bot.api import API
from film_bot.config import config
from film_bot.db import create_tables, load_user_data
from film_bot.messages import HELP_MSG, START_MSG
from film_bot.models import (
    FilmFromActorForm,
    FilmFromGenreForm,
    FilmFromTitleForm,
    FilmFromYearForm,
)

api = API()
dp = Dispatcher()


@dp.message(CommandStart())
@dp.message(F.text.casefold() == "вернуться в главное меню 📌")
async def command_start_handler(message: Message) -> None:
    """Start command handler."""
    # TODO: Добавить запись в бд для списка избранного
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌸 Аниме"),
                KeyboardButton(text="📺 Дорамы"),
                KeyboardButton(text="❤️ Избранное"),
            ],
            [
                KeyboardButton(text="❓ Что я умею?"),
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer(START_MSG, reply_markup=markup)


@dp.message(Command("help"))
@dp.message(F.text.casefold() == "❓ что я умею?")
async def command_help_handler(message: Message) -> None:
    """Start command handler."""
    await message.answer(HELP_MSG)


@dp.message(F.text.casefold() == "🌸 аниме")
async def anime_button_handler(message: Message) -> None:
    """Anime button handler."""
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Поиск аниме по названию 🔎"),
                KeyboardButton(text="Поиск аниме по жанру 🎭"),
                KeyboardButton(text="Поиск аниме по году 🎯"),
            ],
            [
                KeyboardButton(text="Случайное аниме 💡"),
                KeyboardButton(text="Вернуться в главное меню 📌"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Вы в разделе 🌸 Аниме", reply_markup=markup)


@dp.message(F.text.casefold() == "📺 дорамы")
async def dorama_button_handler(message: Message) -> None:
    """Dorama button handler."""
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Поиск дорамы по названию 🔎"),
                KeyboardButton(text="Поиск дорамы по жанру 🎭"),
                KeyboardButton(text="Поиск дорамы по году 🎯"),
            ],
            [
                KeyboardButton(text="Случайная дорама 💡"),
                KeyboardButton(text="Поиск дорамы по актеру 💎"),
                KeyboardButton(text="Вернуться в главное меню 📌"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Вы в разделе 📺 Дорамы", reply_markup=markup)


@dp.message(F.text.casefold() == "❤️ избранное")
async def favorites_button_handler(message: Message) -> None:
    """Favorites button handler."""
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Мой список 📜"),
                KeyboardButton(text="Добавить в Избранное 📝"),
            ],
            [
                KeyboardButton(text="Удалить из Избранного 🚫"),
                KeyboardButton(text="Вернуться в главное меню 📌"),
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer("Вы в разделе ❤️ Избранное", reply_markup=markup)


@dp.message(F.text.casefold() == "поиск аниме по названию 🔎")
@dp.message(F.text.casefold() == "поиск дорамы по названию 🔎")
async def film_from_title_handler(message: Message, state: FSMContext) -> None:
    """Поиск аниме по названию."""
    # Set state
    await state.set_state(FilmFromTitleForm.title)

    # Add film type parameter
    film_type = message.text.split()[1]
    state.update_data(film_type=film_type)

    # Responding to the user
    await message.answer(
        f"Введи название {film_type}, которое (-ую) хочешь посмотреть",
    )


@dp.message(F.text.casefold() == "поиск аниме по жанру 🎭")
@dp.message(F.text.casefold() == "поиск дорамы по жанру 🎭")
async def film_from_genre_handler(message: Message, state: FSMContext) -> None:
    # Set state
    await state.set_state(FilmFromGenreForm.genre)

    # Add film type parameter
    film_type = message.text.split()[1]
    state.update_data(film_type=film_type)

    # Responding to the user
    await message.answer(
        "Введи нужные жанры (если их несколько, то укажи их через запятую).",
    )


@dp.message(F.text.casefold() == "поиск аниме по актеру 💎")
@dp.message(F.text.casefold() == "поиск дорамы по актеру 💎")
async def film_from_actor_handler(message: Message, state: FSMContext) -> None:
    # Set state
    await state.set_state(FilmFromActorForm.genre)

    # Add film type parameter
    film_type = message.text.split()[1]
    state.update_data(film_type=film_type)

    # Responding to the user
    await message.answer(
        "Введи нужных актеров (если их несколько, "
        "то укажи их через запятую, без пробелов)",
    )


@dp.message(F.text.casefold() == "поиск аниме по году 🎯")
@dp.message(F.text.casefold() == "поиск дорамы по году 🎯")
async def film_from_year_handler(message: Message, state: FSMContext) -> None:
    # Set state
    await state.set_state(FilmFromYearForm.genre)

    # Add film type parameter
    film_type = message.text.split()[1]
    state.update_data(film_type=film_type)

    # Responding to the user
    await message.answer(
        "Введи нужный год или диапазон годов (если вводишь "
        "диапазон, то вводи в формате год-год)",
    )


@dp.message(F.text.casefold() == "случайное аниме 💡")
@dp.message(F.text.casefold() == "случайная дорама 💡")
async def random_film_handler(message: Message) -> None:
    # Get the type of movie required by the user
    film_type = message.text.split()[1]

    # Responding to the user
    await message.answer(
        f"Случайное (-ая) {film_type}, надеюсь, что оно (-а) тебе понравится:",
    )
    await message.answer(
        await api.random(film_type),
    )


@dp.message(FilmFromTitleForm.title)
async def anime_from_title_state_handler(message: Message, state: FSMContext) -> None:
    """Поиск аниме/дорам по названию."""
    print(await state.get_data())
    await message.answer(await api.from_title(message.text, (await state.get_data())["film_type"]))


@dp.message(FilmFromGenreForm.genre)
async def anime_from_genre_state_handler(message: Message, state: FSMContext) -> None:
    """Поиск аниме/дорам по жанру."""
    await message.answer(await api.from_genre(message.text, (await state.get_data())["film_type"]))


@dp.message(FilmFromActorForm.actor)
async def anime_from_actor_state_handler(message: Message, state: FSMContext) -> None:
    """Поиск аниме/дорам по жанру."""
    await message.answer(await api.from_genre(message.text, (await state.get_data())["film_type"]))


@dp.message(FilmFromYearForm.year)
async def anime_from_year_state_handler(message: Message, state: FSMContext) -> None:
    """Поиск аниме/дорам по жанру."""
    await message.answer(await api.from_genre(message.text, (await state.get_data())["film_type"]))


# TODO: Dealing with the database and favorites list
"""
    elif message.text == "Добавить в Избранное 📝":
        message = self.bot.send_message(
            message.chat.id,
            "Введи, что ты хочешь добавить: аниме или дораму",
        )

    elif message.text == "Мой список 📜":
        message = self.bot.send_message(
            message.chat.id,
            "Введи, что ты хочешь увидеть: аниме или дорамы",
        )

    elif message.text == "Удалить из Избранного 🚫":
        message = self.bot.send_message(
            message.chat.id,
            "Введи, что ты хочешь удалить: аниме или дораму",
        )
"""


@dp.message()
async def any_messages_handler(message: Message) -> None:
    """Any messages handler."""
    await message.answer(
        (
            "⚙️ На такую команду я не запрограммирован... "
            "попробуйте другую или введите /help"
        ),
    )


async def main() -> None:
    """Bot startup."""
    # TODO: Подключаем файл для сбора логов
    # TODO: Подключаем базу данных для списка избранного
    await api.init()
    db_connection = sqlite3.connect("index.db", check_same_thread=False)

    # create_tables(db_connection)
    # user_data = load_user_data(db_connection)  # noqa: ERA001

    bot = Bot(token=config.telegam_bot_token, default=DefaultBotProperties())
    await dp.start_polling(bot)
