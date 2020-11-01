class Heading(object):
    def __init__(self, num: int, text: str):
        assert 0 < num < 7
        self.__num = num
        self.__text = text

    def make_string(self) -> str:
        tag = f"h{self.__num}"
        return f"<{tag}>{self.__text}</{tag}>"
