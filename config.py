from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    port: str
    user: str
    password: str
    database_name: str
    db_url: str


@dataclass
class RedisConfig:
    url: str


@dataclass
class TgBotConfig:
    token: str
    provider_token: str

@dataclass
class ApiConfig:
    api_key: str
    base_url: str


@dataclass
class Config:
    tg: TgBotConfig
    redis: RedisConfig
    db: DbConfig
    api: ApiConfig


def load_config(debug: bool = False, path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        tg=TgBotConfig(
            token=env.str("BOT_TOKEN_DEBUG") if debug else env.str("BOT_TOKEN"),
            provider_token=env.str("PROVIDER_TOKEN")
        ),

        redis=RedisConfig(url=env.str("REDIS_URL")),

        db=DbConfig(
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database_name=env.str("DB_NAME"),
            db_url=f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"),

        api=ApiConfig(
            api_key=env.str("API_KEY"),
            base_url=env.str("BASE_URL")
        )
    )
