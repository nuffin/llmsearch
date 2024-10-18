from . import tokenize


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: fileparser <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    tokenize(filepath)


if __name__ == "__main__":
    main()
