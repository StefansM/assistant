import pathlib
import textwrap

from assistant.coding.applier import ApplierMode
from assistant.coding.applier import DocstringApplier


data_path = pathlib.Path(__file__).parent / "data"


def load_request_and_response(test_case: str) -> tuple[str, str]:  #
    request_txt = (data_path / test_case / "input.txt").read_text()
    response_txt = (data_path / test_case / "sanitized_response.txt").read_text()
    return request_txt, response_txt


def test_docstring_applier() -> None:
    req, res = load_request_and_response("update_inject_class")

    applier = DocstringApplier(req, ApplierMode.KEEP)
    print(applier.apply(res))


# Simple test cases to check whether we can either keep or replace docstrings.
input_text = textwrap.dedent(
    '''\
    def foo():
        """original"""
    '''
)


patched_text = textwrap.dedent(
    '''\
    def foo():
        """patched"""
    '''
)


def test_docstrings_are_kept_in_keep_mode() -> None:
    applier = DocstringApplier(input_text, ApplierMode.KEEP)
    result = applier.apply(patched_text)

    assert result.strip() == input_text.strip()


def test_docstrings_are_replaced_in_replace_mode() -> None:
    applier = DocstringApplier(input_text, ApplierMode.REPLACE)
    result = applier.apply(patched_text)

    assert result.strip() == patched_text.strip()
