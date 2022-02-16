def save(content: str, file_name: str):
    with open(file_name, "w") as file:
        file.write(content)


def load(file_name: str) -> str:
    with open(file_name, "r") as file:
        return file.read()
