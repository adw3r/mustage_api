import os
import pathlib

import dotenv

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent
dotenv.load_dotenv(ROOT_DIR / '.env')


# Postgres config
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

DB_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

LOGGING_FORMAT = (
    "<level>{time:YYYY-MM-DD HH:mm:ss.SSS}</level> "
    "<level>{level}</level>: "
    "<level>{name}</level> - "
    "<level>{message}</level>"
)

APP_HOST = os.environ['APP_HOST']
APP_PORT = os.environ['APP_PORT']
