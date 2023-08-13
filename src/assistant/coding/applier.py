"""Adds docstrings suggested by the OpenAI model back to the source code."""
import ast
import enum
import textwrap
from typing import Any

import libcst as cst

from assistant.coding.model import StmtNodes


class ApplierMode(enum.Enum):
    REPLACE = enum.auto()
    KEEP = enum.auto()


class DocstringTransformer(cst.CSTTransformer):
    def __init__(
        self,
        async_function_defs: dict[str, str | None],
        function_defs: dict[str, str | None],
        classes: dict[str, str | None],
        module_docstring: str | None,
        mode: ApplierMode,
    ):
        super().__init__()
        self.async_function_defs = async_function_defs
        self.function_defs = function_defs
        self.classes = classes
        self.module_docstring = module_docstring
        self.mode = mode

    @staticmethod
    def _create_docstring_node(docstring: str) -> cst.SimpleStatementLine:
        return cst.SimpleStatementLine(
            body=[
                cst.Expr(
                    value=cst.SimpleString(value=f'"""{textwrap.dedent(docstring)}"""')
                )
            ]
        )

    def _add_docstring(self, node: StmtNodes, docstring: str | None) -> StmtNodes:
        has_docstring = node.get_docstring() is not None

        if not docstring:
            return node
        elif has_docstring and self.mode == ApplierMode.KEEP:
            return node

        docstring_node = self._create_docstring_node(docstring)
        if isinstance(node, cst.Module):
            body = node.body
            if has_docstring:
                return node.with_changes(body=(docstring_node, *body[1:]))
            else:
                node = node.with_changes(body=(docstring_node, cst.EmptyLine(), *body))
                return node

        body = node.body.body[1:] if has_docstring else node.body.body
        return node.with_changes(
            body=node.body.with_changes(body=(docstring_node, *body))
        )

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        return self._add_docstring(
            updated_node, self.function_defs.get(updated_node.name.value, None)
        )

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        return self._add_docstring(
            updated_node, self.classes.get(updated_node.name.value, None)
        )

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        return self._add_docstring(updated_node, self.module_docstring)


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
    def __init__(self, text: str, mode: ApplierMode):
        self.text = text
        self.mode = mode

    def apply(self, replacement: str) -> str:
        original_cst = cst.parse_module(self.text)
        replacement_ast = ast.parse(replacement)

        docstring_extractor = ReplacementDocstringExtractor()
        docstring_extractor.visit(replacement_ast)

        docstring_transformer = DocstringTransformer(
            docstring_extractor.async_function_defs,
            docstring_extractor.function_defs,
            docstring_extractor.classes,
            docstring_extractor.module_docstring,
            self.mode,
        )
        modified = original_cst.visit(docstring_transformer)
        return modified.code
