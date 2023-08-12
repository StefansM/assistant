"""Adds docstrings suggested by the OpenAI model back to the source code."""
import ast
import textwrap

from assistant.coding.model import InterestingNode


class DocstringTransformer(ast.NodeTransformer):
    def __init__(
        self,
        async_function_defs: dict[str, str],
        function_defs: dict[str, str],
        classes: dict[str, str],
        module_docstring: str | None,
    ):
        self.async_function_defs = async_function_defs
        self.function_defs = function_defs
        self.classes = classes
        self.module_docstring = module_docstring

    @staticmethod
    def _create_docstring_node(docstring: str) -> ast.stmt:
        return ast.Expr(value=ast.Str(s=docstring))

    def _add_docstring(self, node: InterestingNode, docstring: str | None):
        if docstring:
            indented_docstring = textwrap.indent(
                docstring, (node.col_offset + 4) * " "
            ).strip()

            docstring_node = self._create_docstring_node(indented_docstring)
            node.body.insert(0, docstring_node)

        return node

    def visit_AsyncFunctionDef(  # noqa: N802
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        super().generic_visit(node)
        return self._add_docstring(node, self.async_function_defs.get(node.name, None))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        super().generic_visit(node)
        return self._add_docstring(node, self.function_defs.get(node.name, None))

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        super().generic_visit(node)
        return self._add_docstring(node, self.classes.get(node.name, None))

    def visit_Module(self, node: ast.Module) -> ast.Module:
        super().generic_visit(node)
        return self._add_docstring(node, self.module_docstring)


class ReplacementDocstringExtractor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.async_function_defs: dict[str, str] = {}
        self.function_defs: dict[str, str] = {}
        self.classes: dict[str, str] = {}
        self.module_docstring: str | None = None

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        self.async_function_defs[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.function_defs[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.classes[node.name] = ast.get_docstring(node)
        return super().generic_visit(node)

    def visit_Module(self, node: ast.Module) -> ast.Module:
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
