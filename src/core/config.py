from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "API Ordem de Serviço"

    class Config:
        env_file = ".env"


settings = Settings()