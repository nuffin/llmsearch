from . import LocalBackend


def main():
    import os
    import sys

    ## if len(sys.argv) < 2:
    ##     print(f"Usage: {os.path.basename(__file__)} <filepath>")
    ##     sys.exit(1)

    backend = LocalBackend()
    print(backend.embedding_text("gpt2", "Hello, world!"))


if __name__ == "__main__":
    main()
