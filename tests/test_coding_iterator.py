import pathlib

from assistant.coding.iterator import FileIterator
from assistant.coding.iterator import RepositoryIterator


repo_root = pathlib.Path(__file__).parent / ".." / "code_examples" / "phyre_engine"


def test_path_iterator() -> None:
    iterator = RepositoryIterator(repo_root)

    for _ in iterator.iterate():
        return

    raise AssertionError("Should have iterated over at least one file")


def test_file_iterator() -> None:
    file_path = repo_root / "phyre_engine" / "component" / "strucaln.py"

    iterator = FileIterator(file_path)
    for clazz in iterator.iterate():
        print(clazz)
        return
