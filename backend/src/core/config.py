from pydantic_settings import BaseSettings

class Settings (BaseSettings):
    PROJECT_NAME: str = 'APP MOVIL DE GESTION DE DATOS MASIVOS EN LA U.E COLEGIO SIMÓN BOLÍVAR'
    PROJECT_VERSION:str = '0.0.1'
    DATABASE_URL: str
    EXPO_PUBLIC_API_URL: str

    class Config:
        env_file = '.env'

settings = Settings()