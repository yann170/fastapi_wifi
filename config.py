from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MIKROTIK_HOST: str = "localhost"
    MIKROTIK_USERNAME: str = "admin"
    MIKROTIK_PASSWORD: str = "password"
    MIKROTIK_API_PORT: int = 8729
    MIKROTIK_USE_SSL: bool = True
    MIKROTIK_FRONTEND_IP: str = "127.0.0.1"
 
    JWT_SECRET_KEY: str = "your_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Permet de charger les variables depuis un fichier .env
    model_config = SettingsConfigDict(env_file='prod.env', env_file_encoding='utf-8')

settings = Settings()