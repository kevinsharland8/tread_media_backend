from dotenv import load_dotenv
import os

# dotenv_path = ".env.dev"
dotenv_path = '.env.prod'

load_dotenv(dotenv_path)


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


pg_pool_max_size = 10
pg_pool_min_size = 2
