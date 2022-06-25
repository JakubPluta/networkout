import sys
import logging
from pydantic import BaseSettings, validator, AnyHttpUrl, EmailStr
from typing import List, Union, Optional, Type
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


module = sys.modules[__name__]


class Config(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str  = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int  = 30

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",  # type: ignore
    ]
    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = None

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = 'sqlite:///local.db'
    FIRST_SUPERUSER: EmailStr = "test@networkout.com"
    FIRST_SUPERUSER_PASSWORD: str = "test"

    class Config:
        case_sensitive = True


class ProdConfig(Config):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: str  = os.getenv('DB_URI')
    FIRST_SUPERUSER: EmailStr = os.getenv('DB_USERNAME')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('DB_PASSWORD')


class LocalConfig(Config):

    SECRET_KEY: str =  'this is amazing secret'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///networkout.db'
    FIRST_SUPERUSER: EmailStr = 'admin@app.com'
    FIRST_SUPERUSER_PASSWORD: str = 'admin'


def get_config(env='local') -> Type[Config]:
    assert env.lower() in ['local','prod'], "Env variable needs to be prod, local or test. By default: local"
    try:
        return getattr(sys.modules[__name__], f"{str(env).title()}Config")()
    except AttributeError as e:
        logger.info(f'could not find config: {env}')
    return LocalConfig.__call__()


def get_node():
    node = os.getenv('ENV_NODE', 'local')
    logger.info(f"Node {node}")
    return node


settings: Type[Config] = get_config(get_node())
