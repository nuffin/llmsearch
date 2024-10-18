import common


def tokenize(filepath: str):
    with open(filepath, "r") as f:
        text = f.read()
    return text.split()
