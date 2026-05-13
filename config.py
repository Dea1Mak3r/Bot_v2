from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: str
    TELEGRAM_TOKEN: str
    API_URL: str
    login: str
    password: str
    LENTA_LOGIN_URL: str
    LENTA_INFO_URL: str
    MARS_LOGIN_URL: str
    MARS_INFO_URL: str
    ADMIN_CHAT_ID: str

    # Указываем, откуда брать данные, если их нет в системном окружении
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()