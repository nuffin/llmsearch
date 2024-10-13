#!/usr/bin/env python3

import os.path

from filetypes.mimetype import detect

from app import app


def main():
    dir = os.path.dirname(__file__)
    filepath = os.path.realpath(os.path.join(dir, "..", "requirements.txt"))
    print(f"filepath={filepath}")
    meme_type = detect(filepath)
    print(f"meme_type={meme_type}")

    app.run(debug=True)


if __name__ == "__main__":
    main()
