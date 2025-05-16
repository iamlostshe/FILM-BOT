"""Глобальные настройки бота."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    telegam_bot_token: str
    kinopoisk_api_key: str


config: Config = Config(_env_file=".env")
