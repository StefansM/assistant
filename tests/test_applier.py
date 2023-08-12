import importlib.resources

from assistant.coding.applier import DocstringApplier


def load_request_and_response(test_case: str) -> tuple[str, str]:
    request_txt = importlib.resources.read_text(f"data.{test_case}", "input.txt")
    response_txt = importlib.resources.read_text(
        "data.update_inject_class", "sanitized_response.txt"
    )
    return request_txt, response_txt


def test_docstring_applier():
    req, res = load_request_and_response("update_inject_class")

    applier = DocstringApplier(req)
    print(applier.apply(res))
