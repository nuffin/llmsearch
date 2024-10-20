import os

from .fileparser.mimetype import detect
from .schemas.fileinfo import FileInfo


def load_file_info(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist")

    # Get file information
    name = os.path.basename(filepath)
    path = os.path.abspath(filepath)
    originName = name
    size = os.path.getsize(filepath)
    file_type = os.path.splitext(filepath)[1][1:]  # File extension as type
    mimetype = detect(filepath)

    return FileInfo(
        fileId=str(
            os.path.getctime(filepath)
        ),  # Using creation time as fileId (or customize)
        name=name,
        path=path,
        originName=originName,
        size=size,
        type=file_type,
        mimetype=mimetype or "unknown",
    )


def main():
    import os
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(__file__)} <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    file_info = load_file_info(filepath)
    print(file_info)


if __name__ == "__main__":
    main()
