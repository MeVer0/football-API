import json

from pydantic import BaseSettings

with open('config.json') as c:
    config = json.load(c)




class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    database_url: str = config.get('database_url')


settings = Settings(
    _env_file=".env",
    _env_file_encoding='utf-8',
)
