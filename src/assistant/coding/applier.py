"""Adds docstrings suggested by the OpenAI model back to the source code."""
import ast
import textwrap
from typing import Any

from assistant.coding.model import StmtNodes


class DocstringTransformer(ast.NodeTransformer):
    def __init__(
        self,
        async_function_defs: dict[str, str | None],
        function_defs: dict[str, str | None],
        classes: dict[str, str | None],
        module_docstring: str | None,
    ):
        self.async_function_defs = async_function_defs
        self.function_defs = function_defs
        self.classes = classes
        self.module_docstring = module_docstring

    @staticmethod
    def _create_docstring_node(docstring: str) -> ast.stmt:
        return ast.Expr(value=ast.Str(s=docstring))

    def _add_docstring(self, node: StmtNodes, docstring: str | None) -> Any:
        if docstring:
            indented_docstring = textwrap.indent(
                docstring, (node.col_offset + 4) * " "
            ).strip()

            docstring_node = self._create_docstring_node(indented_docstring)
            node.body.insert(0, docstring_node)

        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        super().generic_visit(node)
        return self._add_docstring(node, self.async_function_defs.get(node.name, None))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        super().generic_visit(node)
        return self._add_docstring(node, self.function_defs.get(node.name, None))

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        super().generic_visit(node)
        return self._add_docstring(node, self.classes.get(node.name, None))

    def visit_Module(self, node: ast.Module) -> Any:
        super().generic_visit(node)
        return self._add_docstring(node, self.module_docstring)


class ReplacementDocstringExtractor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.async_function_defs: dict[str, str | None] = {}
        self.function_defs: dict[str, str | None] = {}
        self.classes: dict[str, str | None] = {}
        self.module_docstring: str | None = None

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.async_function_defs[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.function_defs[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.classes[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_Module(self, node: ast.Module) -> Any:
        self.module_docstring = ast.get_docstring(node)
        return super().generic_visit(node)


class DocstringApplier:
    def __init__(self, text: str):
        self.text = text

    def apply(self, replacement: str) -> str:
        original_ast = ast.parse(self.text)
        replacement_ast = ast.parse(replacement)

        docstring_extractor = ReplacementDocstringExtractor()
        docstring_extractor.visit(replacement_ast)

        docstring_transformer = DocstringTransformer(
            docstring_extractor.async_function_defs,
            docstring_extractor.function_defs,
            docstring_extractor.classes,
            docstring_extractor.module_docstring,
        )
        patched_ast = ast.fix_missing_locations(
            docstring_transformer.visit(original_ast)
        )
        return ast.unparse(patched_ast)
