import os
from dotenv import load_dotenv


env_loaded = False


def getenv(name, default=None):
    global env_loaded
    if not env_loaded:
        env_name = os.getenv("ENVIRONMENT", "")
        env_file_path = f".env.{env_name}" if env_name else ".env"
        print(f'Loading environment variables from "{env_file_path}"')
        load_dotenv(dotenv_path=env_file_path, verbose=True)
        env_loaded = True
    return os.getenv(name, default)
