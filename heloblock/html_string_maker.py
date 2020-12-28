from abc import ABCMeta, abstractmethod

from typing import List

LINE_FEED_CODE: str = "\r\n"

INDENT: str = "    "


# ##############################################
# インターフェース
class IMakeString(metaclass=ABCMeta):
    @abstractmethod
    def make_string(self) -> str:
        """
        出力する文字列の作成
        """
        pass


# ##############################################
# インデントを深くする
class Indent(object):
    """インデントを作る"""

    def __init__(self):
        self._indent_depth: int = 0

    def set_indent_depth(self, value: int) -> None:
        self._indent_depth = value

    def get_child_indent_depth(self) -> int:
        """子のインデントの深さを作成(自身のインデントの深さ+1)"""
        return self._indent_depth + 1

    def get_indent(self) -> str:
        """自身のインデント作成"""
        return INDENT * self._indent_depth


# ##############################################
# タグでテキストを挟む処理 の移譲先
class SandwichWithTags(object):
    """タグで挟む"""

    def __init__(self, tag: str):
        self._tag: str = tag

    def sandwich_with_tags(self, text: str) -> str:
        return f"<{self._tag}>{text}</{self._tag}>"


class SandwichWithTagsWithClass(SandwichWithTags):
    """class付き"""

    def __init__(self, tag: str, html_class_name: str):
        self.__html_class_name: str = html_class_name
        super(SandwichWithTagsWithClass, self).__init__(tag)

    def sandwich_with_tags(self, text: str) -> str:
        return f'<{self._tag} class="{self.__html_class_name}">{text}</{self._tag}>'


class SandwichWithTagsWithId(SandwichWithTags):
    """id付き"""

    def __init__(self, tag: str, html_id_name: str):
        self.__html_id_name: str = html_id_name
        super(SandwichWithTagsWithId, self).__init__(tag)

    def sandwich_with_tags(self, text: str) -> str:
        return f'<{self._tag} id="{self.__html_id_name}">{text}</{self._tag}>'


# ##############################################
# 基盤クラス
class BaseHtmlString(IMakeString, Indent):
    def __init__(self, tag: str):
        super(BaseHtmlString, self).__init__()
        self.__tag: str = tag
        self.children: List[BaseHtmlString] = []
        self.__sandwich: SandwichWithTags = SandwichWithTags(tag)  # デフォルトの処理

    def set_indent_depth_to_children(self) -> None:
        """このオブジェクトのインデントを下げる"""
        if len(self.children) == 0:
            return

        child_indent_depth: int = self.get_child_indent_depth()
        child: BaseHtmlString
        for child in self.children:
            child.set_indent_depth(child_indent_depth)

    def set_class(self, html_class_name) -> None:
        # 処理の切り替えを実行
        self.__sandwich = SandwichWithTagsWithClass(self.__tag, html_class_name)

    def set_id(self, html_id_name) -> None:
        # 処理の切り替えを実行
        self.__sandwich = SandwichWithTagsWithId(self.__tag, html_id_name)

    def make_string(self) -> str:
        """
        出力する文字列の作成
        """
        self.set_indent_depth_to_children()
        result = self.__make_string_for_children()
        return self.get_indent() + self._sandwich_with_tags(result)

    def __make_string_for_children(self):
        if len(self.children) == 0:
            return LINE_FEED_CODE
        else:
            children_texts = [child.make_string() for child in self.children]
            result_text = LINE_FEED_CODE.join(children_texts)
            return f"{LINE_FEED_CODE}{result_text}{LINE_FEED_CODE}"

    def append(self, children: list):
        """
        子の追加
        """
        self.children.extend(children)

    def _sandwich_with_tags(self, text):
        return self.__sandwich.sandwich_with_tags(text)


# ############################################################
# 各タグごとの動作
# ############################################################
# ############################################################
class Text(IMakeString, Indent):
    """テキスト(最小単位。子は持たない)"""

    def __init__(self, text: str):
        super(Text, self).__init__()
        self.__text: str = text

    def make_string(self) -> str:
        return self.get_indent() + self.__text


# ############################################################
class Heading(BaseHtmlString):
    """h"""

    def __init__(self, num: int, text: str):
        assert 0 < num < 7
        self.__text = text
        super(Heading, self).__init__(f"h{num}")

    def make_string(self) -> str:
        return self.get_indent() + self._sandwich_with_tags(self.__text)

    def append(self, children: list):
        raise Exception("can not use")


# ############################################################
class Body(BaseHtmlString):
    """body"""

    def __init__(self):
        super(Body, self).__init__("body")


# ############################################################
class Division(BaseHtmlString):
    """div"""

    def __init__(self):
        super(Division, self).__init__("div")

# ############################################################
# HTML FILE
# ############################################################
