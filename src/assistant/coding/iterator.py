import ast
import collections.abc
import pathlib
import typing

from assistant.coding.model import DocstringNode
from assistant.coding.model import InterestingNode


class FileIterator:
    """Class to iterate over file contents and generate an abstract
    syntax tree (AST).

    Given a file, this class reads the contents and generates an AST divided
    into interesting nodes (functions, classes and modules) and also docstrings
    associated with the nodes.

    Attributes:
        file_path (pathlib.Path):
            The path to the python script file that needs to be parsed
        text (str):
            Content of the python script"""

    def __init__(self, file_path: pathlib.Path):
        """Instantiates the RepositoryIterator object with the given root directory.

        Args:
            root (pathlib.Path):
                The root directory that needs to be parsed"""
        assert file_path.is_file()
        self.file_path = file_path
        self.text = self.file_path.read_text()

    def _extract_ast(self, node: InterestingNode) -> typing.Iterable[DocstringNode]:
        """Extracts nodes from the AST.

        Args:
            node: Node for which sub-trees are created

        Returns:
            An iterable containing DocstringNode objects, which includes
            information about the node (AST), associated docstring,
            associated code snippet, and its child nodes"""
        interesting_nodes = (
            ast.AsyncFunctionDef,
            ast.FunctionDef,
            ast.ClassDef,
            ast.Module,
        )
        if not isinstance(node, interesting_nodes):
            return

        child_nodes = []
        for child in ast.iter_child_nodes(node):
            for transformed_child in self._extract_ast(child):
                if transformed_child:
                    child_nodes.append(transformed_child)

        src = ast.get_source_segment(self.text, node)

        if isinstance(node, ast.Module) and not src:
            src = self.text

        yield DocstringNode(
            ast=node,
            original_docstring=ast.get_docstring(node),
            code_snippet=src,
            children=child_nodes,
        )

    def iterate(self) -> collections.abc.Iterable[DocstringNode]:
        """Iterates over the directory to generate paths to Python script files.

        Returns:
            An iterable containing pathlib.Path objects, which are paths to
            Python script files in the directory"""
        syntax_tree = ast.parse(self.text, filename=self.file_path.name)
        yield from self._extract_ast(syntax_tree)


class RepositoryIterator:
    """Class to iterate over a repository of python script files.

    This class iterates over all Python files in the provided directory
    and its subdirectories.

    Attributes:
        root (pathlib.Path):
            The root directory that needs to be parsed"""

    def __init__(self, root: pathlib.Path):
        """Instantiates the RepositoryIterator object with the given root directory.

        Args:
            root (pathlib.Path):
                The root directory that needs to be parsed"""
        assert root.is_dir()
        self.root = root

    def iterate(self) -> collections.abc.Iterable[pathlib.Path]:
        """Iterates over the directory to generate paths to Python script files.

        Returns:
            An iterable containing pathlib.Path objects, which are paths to
            Python script files in the directory"""
        for path in self.root.glob("**/*.py"):
            if path.is_file():
                yield path
