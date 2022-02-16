from typing import List, Any
from utils import save


def gen_row(acc: str, values: List[Any]) -> str:
    """
    Generates row from list of values with tail recursion.
    Ex., [1, 2, 3] -> "1 & 2 & 3".
    """
    if len(values) == 0:
        return acc
    if len(values) == 1:
        acc = f"{acc}{values[0]}"
        return gen_row(acc, values[1:])
    else:
        acc = f"{acc}{values[0]} & "
        return gen_row(acc, values[1:])


def gen_content(values: List[List[Any]]) -> str:
    """
    Generates content from values.
    Ex., [[1, 2, 3], [4, 5]] -> "1 & 2 & 3 \\ \hline \n 4 & 5 \\".
    """
    return " \\\ \\hline\n".join(map(lambda x: gen_row("", x), values))


def gen_table(values: List[List[Any]]) -> str:
    centering = 'c' * len(values[0])
    header = r"\begin{tabular}" + "{" + centering + "}"
    footer = r"\end{tabular}"
    content = gen_content(values)
    return "\n".join([header, content, footer])


if __name__ == "__main__":
    values = [
        [1, 2, 3],
        [4, 5],
        [6, 7, 8]
    ]

    table = gen_table(values)
    save(table, "artifacts/table.tex")
