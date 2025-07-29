from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MIKROTIK_HOST: str
    MIKROTIK_USERNAME: str
    MIKROTIK_PASSWORD: str
    MIKROTIK_API_PORT: int = 8729
    MIKROTIK_USE_SSL: bool = True
    MIKROTIK_FRONTEND_IP: str # L'IP du MikroTik vue par le navigateur pour CORS

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Permet de charger les variables depuis un fichier .env
    #model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings