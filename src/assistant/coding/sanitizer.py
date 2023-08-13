class ResponseSanitizer:
    """Sanitize the response from the OpenAI."""

    def __init__(self) -> None:
        """Initializes the ResponseSanitizer class."""
        self._extractors = [
            self._extract_code,
            self._extract_delimited,
        ]

    @staticmethod
    def _extract_code(content: str) -> str:
        """Extracts code from the content.

        Args:
            content (str): The text content from which to extract the code.

        Returns:
            str: Extracted code if present, else returns the content as is."""
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
        """Extracts text between delimiters from the content.

        Args:
            content (str): The text content from which to extract the delimited text.

        Returns:
            str: Extracted delimited text if present, else returns the content as is."""
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
        """Runs content through all the extractors defined in the class.

        Args:
            content (str): The text content to sanitize.

        Returns:
            str: The sanitized content."""
        for extractor in self._extractors:
            content = extractor(content)

        return content
