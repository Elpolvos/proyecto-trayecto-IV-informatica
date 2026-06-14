import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class SecurityConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "pepetoño")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
    
    @classmethod
    def get_jwt_settings(cls):
        return {
            "secret_key": cls.SECRET_KEY,
            "algorithm": cls.ALGORITHM,
            "expires_delta": timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        }