import pathlib

from assistant.coding.applier import DocstringApplier


data_path = pathlib.Path(__file__).parent / "data"


def load_request_and_response(test_case: str) -> tuple[str, str]:  #
    request_txt = (data_path / test_case / "input.txt").read_text()
    response_txt = (data_path / test_case / "sanitized_response.txt").read_text()
    return request_txt, response_txt


def test_docstring_applier() -> None:
    req, res = load_request_and_response("update_inject_class")

    applier = DocstringApplier(req)
    print(applier.apply(res))
