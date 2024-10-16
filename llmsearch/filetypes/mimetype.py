import os
import magic

mime = magic.Magic(mime=True)


def detect(filepath: str, follow_symlinks: bool = True) -> str:
    resolved_filepath = follow_symlinks and os.path.realpath(filepath) or filepath
    return mime.from_file(resolved_filepath) if os.path.isfile(filepath) else None


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
