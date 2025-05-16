"""Глобальные настройки бота."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from pydantic import SecretStr


class Config(BaseSettings):
    telegam_bot_token: SecretStr
    kinopoisk_api_key: SecretStr


config: Config = Config(_env_file=".env")
