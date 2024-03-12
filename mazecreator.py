from main import *

if __name__ == "__main__":
    path = "maze.txt"

    def write_file():
        with open(path, "w") as file:
            file.write()

    def read_file():
        with open(path) as file:
            return file.read()

    print(read_file())