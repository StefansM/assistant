class ResponseSanitizer:
    """Sanitize the response from the OpenAI."""

    def __init__(self) -> None:
        self._extractors = [
            self._extract_code,
            self._extract_delimited,
        ]

    @staticmethod
    def _extract_code(content: str) -> str:
        lines = content.split("\n")
        extracting = False
        code_lines: list[str] = []

        for line in lines:
            if line.startswith("```"):
                extracting = not extracting
                continue

            if extracting:
                code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines)

        return content

    @staticmethod
    def _extract_delimited(content: str) -> str:
        lines = content.split("\n")
        extracting = False
        delimiter = "✂"

        code_lines: list[str] = []
        for line in lines:
            if line.startswith(delimiter):
                extracting = True
                continue

            if extracting:
                code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines)

        return content

    def sanitize(self, content: str) -> str:
        for extractor in self._extractors:
            content = extractor(content)

        return content
