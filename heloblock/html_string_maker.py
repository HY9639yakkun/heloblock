from abc import ABCMeta, abstractmethod

LINE_FEED_CODE = "\r\n"


# インターフェース
class BaseHtmlString(metaclass=ABCMeta):
    def __init__(self, tag):
        self.__tag = tag
        self.children = []  # BaseHtmlString into list

    @abstractmethod
    def make_string(self) -> str:
        """
        出力する文字列の作成
        """
        pass

    def append(self, children: list):
        """
        子の追加
        """
        self.children.extend(children)

    def _sandwich_with_tags(self, text):
        return f"<{self.__tag }>{text}</{self.__tag }>"


# ############################################################
class Heading(BaseHtmlString):
    def __init__(self, num: int, text: str):
        assert 0 < num < 7
        self.__text = text
        super(Heading, self).__init__(f"h{num}")

    def make_string(self) -> str:
        return self._sandwich_with_tags(self.__text)

    def append(self, children: list):
        raise Exception("can not use")


# ############################################################
class Body(BaseHtmlString):
    def __init__(self):
        super(Body, self).__init__("body")

    def make_string(self) -> str:
        return self._sandwich_with_tags(self.__make_string_for_children())

    def __make_string_for_children(self):
        if len(self.children) == 0:
            return LINE_FEED_CODE
        else:
            children_texts = [child.make_string() for child in self.children]
            result_text = LINE_FEED_CODE.join(children_texts)
            return f"{LINE_FEED_CODE}{result_text}{LINE_FEED_CODE}"
