import argparse
import ast
from collections import defaultdict
from typing import Optional
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import networkx as nx
import pydot


class ASTVisualizer(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.ast = nx.DiGraph()
        self.label_dict = {}
        self.color_dict = {}
        self.class_count = defaultdict(lambda: 0)

    def extend_ast(self, node: ast.AST, node_label: str, node_color: str):
        class_name = node.__class__.__name__
        node_name = f"{class_name}_{self.class_count[class_name]}"
        self.class_count[class_name] += 1

        if len(self.stack) > 0:
            parent_name = self.stack[-1]
            self.ast.add_edge(parent_name, node_name)

        self.stack.append(node_name)
        self.ast.add_node(node_name)
        self.label_dict[node_name] = node_label
        self.color_dict[node_name] = node_color

        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        label = (f"{node.__class__.__name__}\n"
                 f"name: {node.name}")
        self.extend_ast(node, label, "red")

    def visit_arg(self, node: ast.arg):
        label = (f"{node.__class__.__name__}\n"
                 f"name: {node.arg}")
        self.extend_ast(node, label, "grey")

    def visit_Name(self, node: ast.Name):
        label = (f"{node.__class__.__name__}\n"
                 f"id: {node.id}")
        self.extend_ast(node, label, "green")

    def visit_Constant(self, node: ast.Constant):
        label = (f"{node.__class__.__name__}\n"
                 f"value: {node.value}")
        self.extend_ast(node, label, "pink")

    def generic_visit(self, node: ast.AST):
        label = f"{node.__class__.__name__}"
        self.extend_ast(node, label, "orange")

    def visualize(self, save_path: Optional[str] = None):
        plt.figure(1, figsize=(30, 30))
        pos = graphviz_layout(self.ast, prog="dot")
        nx.draw(self.ast, pos,
                labels=self.label_dict, with_labels=True,
                node_size=[len(node) * 1000 for node in self.ast.nodes()],
                node_color=[self.color_dict[v] for v in self.ast.nodes()])
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()


def visualize(file_path: str, save_path: Optional[str] = None):
    with open(file_path, "r") as file:
        code = file.read()

    node = ast.parse(code)
    visualizer = ASTVisualizer()
    visualizer.visit(node)
    visualizer.visualize(save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default="fibonacci.py")
    parser.add_argument("--save_path", default="artifacts/fibonacci_ast.png")
    args = parser.parse_args()
    visualize(args.file_path, args.save_path)
