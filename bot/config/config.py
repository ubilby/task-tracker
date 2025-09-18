from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class LogSettings:
    level: str
    format: str
    style: str = "{"


@dataclass
class DBConfig:
    url: str
    echo: bool = True


@dataclass
class Config:
    bot: TgBot
    log: LogSettings
    db: DBConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    DATABASE_URL = f'postgresql+asyncpg://{env("POSTGRES_USER")}:{env("POSTGRES_PASSWORD")}@db:{env("POSTGRES_PORT")}/{env("POSTGRES_DB")}'

    return Config(
        bot=TgBot(token=env("BOT_TOKEN")),
        log=LogSettings(
            level=env("LOG_LEVEL"),
            format=env("LOG_FORMAT"),
            style=env("LOG_STYLE", "{")
        ),
        db=DBConfig(url = DATABASE_URL),
    )
