from pydantic import BaseSettings

class Settings(BaseSettings):
    server_host: str = 'https://mrcool-finodays.herokuapp.com'
    server_port: int = 8000
    database_url: str = 'sqlite:///./database.sqlite3'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)