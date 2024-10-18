import os
import magic

mime = magic.Magic(mime=True)

supported_mimetypes = [
    "text/plain",
    "text/csv",
    "text/html",
    "text/xml",
    "text/x-c",  ## c, go ## XXX: add file extension checking
    "text/x-c++",  ## cpp
    "text/x-java-source",  ## java
    "text/x-go",  ## FAKE: not support by python-magic, but checking file extension
    "text/x-matlab",  ## matlab
    "text/x-perl",  ## perl
    "text/x-php",  ## php
    "text/x-python",  ## python, /etc/mime.types
    "text/x-script.python",  ## python, by magic
    "application/javascript",  ## js
    "application/json",
    # "application/x-python-code",  ## python, /etc/mime.types, pyc pyo
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  ## pptx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  ## xlsx
    "audio/mpeg",  ## mp3
    "audio/x-wav",  ## wav
    "image/gif",  ## gif
    "image/jpeg",  ## jpg
    "image/png",  ## png
    "image/svg+xml",  ## svg
    "video/mp4",  ## mp4
    "video/quicktime",  ## mov
    "video/x-msvideo",  ## avi
]


def detect(filepath: str, follow_symlinks: bool = True) -> str:
    resolved_filepath = follow_symlinks and os.path.realpath(filepath) or filepath
    mimetype = mime.from_file(resolved_filepath) if os.path.isfile(filepath) else None
    if mimetype in supported_mimetypes:
        if mimetype == "text/x-c" and filepath.endswith(".go"):
            return "text/x-go"
        return mimetype
    return None


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: mimetype.py <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    meme_type = detect(filepath)
    print(f"{filepath}: {meme_type}")


if __name__ == "__main__":
    main()
