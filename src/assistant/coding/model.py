import ast
import dataclasses
import typing

import libcst as cst


StmtNodes: typing.TypeAlias = cst.FunctionDef | cst.ClassDef | cst.Module

InterestingNode: typing.TypeAlias = StmtNodes | ast.AST


@dataclasses.dataclass
class DocstringNode:
    original_docstring: str | None
    code_snippet: str | None
    ast: ast.AST

    children: list[typing.Union["DocstringNode", "OtherNode"]] = dataclasses.field(
        default_factory=list
    )

    def combine_child_code(self) -> str:
        return "\n\n".join(
            child.code_snippet for child in self.children if child.code_snippet
        )


@dataclasses.dataclass
class OtherNode:
    ast: ast.AST
    code_snippet: str | None
