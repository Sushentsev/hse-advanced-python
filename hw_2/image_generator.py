from typing import List

from homework_1.ast_builder import visualize
from utils import save


def gen_image(img_name: str, scale: float = 1.) -> str:
    return fr"\includegraphics[scale={scale}]" + "{" + img_name + "}"


def gen_content(items: List[str]) -> str:
    header = r"\documentclass{article}\n" \
             r"\begin{document}"
    footer = r"\end{document}"
    content = header + "\n".join(items) + footer
    return content


def gen_pdf(item_path: List[str]) -> str:
    items = []
    for path in item_path:
        with open(path, "r") as file:
            items.append(file.read())

    content = gen_content(items)
    return content


if __name__ == "__main__":
    file_path = "fibonacci.py"
    save_path = "artifacts/fibonacci_ast.png"
    visualize(file_path, save_path)
    image = gen_image("fibonacci_ast.png", 0.5)
    save(image, "artifacts/image.tex")
    content = gen_pdf(["artifacts/table.tex", "artifacts/image.tex"])
    save(content, "artifacts/content.tex")
