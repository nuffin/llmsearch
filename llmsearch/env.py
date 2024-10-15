import os
from dotenv import load_dotenv


__env_loaded = False


__default_values = {
    "SERVER_NAME": "LLM Search Server",
    "HOST": "0.0.0.0",
    "PORT": 58000,
    "DATABASE_URI": "postgresql+psycopg2://postgres:postgres@localhost:35432/llmsearch",
    "PUBLIC_PATH": "public",
    "UPLOADS_PATH": "data/uploads",
    "SQLALCHEMY_ENGINE_POOL_SIZE": 10,  # Pool size (number of connections to keep in the pool)
    "SQLALCHEMY_ENGINE_MAX_OVERFLOW": 5,  # Allow up to 5 additional connections beyond pool_size
    "SQLALCHEMY_ENGINE_POOL_TIMEOUT": 30,  # Wait 30 seconds for a connection before giving up
    "SQLALCHEMY_ENGINE_POOL_RECYCLE": 1800,  # Recycle connections after 30 minutes (1800 seconds)
    "SQLALCHEMY_ENGINE_POOL_PRE_PING": True,  # Enable pre-ping to ensure connections are valid"
    "LOG_LEVEL": "INFO",
}


def getenv(name):
    global __env_loaded
    if not __env_loaded:
        env_name = os.getenv("ENVIRONMENT", None)
        env_file_path = f".env.{env_name}" if env_name else ".env"
        print(f'>>> Loading environment variables from "{env_file_path}"')
        load_dotenv(dotenv_path=env_file_path, verbose=True)
        __env_loaded = True
    value = os.getenv(name, str(__default_values[name]))
    return value
