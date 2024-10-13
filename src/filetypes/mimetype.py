import os
import magic

mime = magic.Magic(mime=True)


def detect(filepath: str):
    return mime.from_file(filepath) if os.path.isfile(filepath) else None
