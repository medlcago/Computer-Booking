from environs import Env

env = Env()
env.read_env(".env")

DB_HOST = env.str("host")
DB_PORT = env.str("port")
DB_USER = env.str("user")
DB_PASSWORD = env.str("password")
DB_NAME = env.str("db")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
