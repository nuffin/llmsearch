import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)


def main():
    from app import main as appmain
    appmain()

if __name__ == "__main__":
    main()
