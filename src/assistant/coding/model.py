import ast
import dataclasses
import typing

import libcst as cst


StmtNodes: typing.TypeAlias = cst.FunctionDef | cst.ClassDef | cst.Module

InterestingNode: typing.TypeAlias = StmtNodes | ast.AST


@dataclasses.dataclass
class DocstringNode:
    """A dataclass representing a node in a code syntax tree that has an associated docstring.

    Attributes:
        original_docstring (str | None): Original docstring associated with the node.
            None if the node had no docstring.
        code_snippet (str | None): A Python code snippet associated with the node.
            None if there's no associated code.
        ast (ast.AST): The AST node associated with this DocstringNode.
        children (list): A list of child nodes. These are also instances of DocstringNode.
    """

    original_docstring: str | None
    code_snippet: str | None
    ast: ast.AST

    children: list["DocstringNode"] = dataclasses.field(default_factory=list)

    def combine_child_code(self) -> str:
        """Combine code snippets from all child nodes into a single string.

        Returns:
            str: A string that combines the code snippets of all child nodes,
            separated by two newline characters. If a child node has no associated
            code snippet, it is not included in the returned string."""
        return "\n\n".join(
            child.code_snippet for child in self.children if child.code_snippet
        )


@dataclasses.dataclass
class OtherNode:
    """A dataclass representing a node in a code syntax tree that is not associated with a docstring.

    Attributes:
        ast (ast.AST): The AST node associated with this OtherNode.
        code_snippet (str | None): A Python code snippet associated with the node.
            None if there's no associated code."""

    ast: ast.AST
    code_snippet: str | None
