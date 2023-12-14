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
    api_v1_prefix: str
    api_key: str
    base_url: str


@dataclass
class Config:
    tg: TgBotConfig
    redis: RedisConfig
    db: DbConfig
    api: ApiConfig
    debug: bool


def load_config(debug: bool = False, path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        tg=TgBotConfig(
            token=env.str("BOT_TOKEN_TEST") if debug else env.str("BOT_TOKEN"),
            provider_token=env.str("PROVIDER_TOKEN")
        ),

        redis=RedisConfig(url=env.str("REDIS_URL")),

        db=DbConfig(
            host=env.str("DB_HOST_TEST"),
            port=env.str("DB_PORT_TEST"),
            user=env.str("DB_USER_TEST"),
            password=env.str("DB_PASSWORD_TEST"),
            database_name=env.str("DB_NAME_TEST"),
            db_url=f"postgresql+asyncpg://{env.str('DB_USER_TEST')}:{env.str('DB_PASSWORD_TEST')}@{env.str('DB_HOST_TEST')}:{env.str('DB_PORT_TEST')}/{env.str('DB_NAME_TEST')}")
        if debug else DbConfig(
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database_name=env.str("DB_NAME"),
            db_url=f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"),

        api=ApiConfig(
            api_v1_prefix="/api/v1",
            api_key=env.str("API_KEY"),
            base_url=env.str("BASE_URL")
        ),
        debug=debug
    )


config = load_config(debug=False)
