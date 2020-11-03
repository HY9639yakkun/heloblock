import unittest

import heloblock.html_string_maker as hm


class TextTest(unittest.TestCase):
    # タグ無しのテキスト
    def test_Heading1(self):
        obj = hm.Text("テスト")
        self.assertEqual("テスト", obj.make_string())


class HeadingTest(unittest.TestCase):
    def test_Heading1(self):
        obj = hm.Heading(1, "テスト")
        self.assertEqual("<h1>テスト</h1>", obj.make_string())

    def test_Heading2(self):
        obj = hm.Heading(2, "こんにちは")
        self.assertEqual("<h2>こんにちは</h2>", obj.make_string())

    def test_over_6(self):
        obj = hm.Heading(6, "6なら大丈夫")
        self.assertEqual("<h6>6なら大丈夫</h6>", obj.make_string())

        with self.assertRaises(AssertionError):
            hm.Heading(7, "7以上なら検証に引っかかる")

    def test_under_1(self):
        with self.assertRaises(AssertionError):
            hm.Heading(0, "0以下なら検証に引っかかる")

    def test_append(self):
        obj = hm.Heading(5, "appendが動作したらエラー")
        with self.assertRaises(Exception):
            obj.append([hm.Heading(5, "appendが動作したらエラー")])


class BodyTest(unittest.TestCase):
    def test_Body(self):
        obj = hm.Body()
        self.assertEqual("<body>\r\n</body>", obj.make_string())

    def test_append(self):
        obj = hm.Body()
        obj.append([hm.Heading(1, "テスト")])
        self.assertEqual("<body>\r\n<h1>テスト</h1>\r\n</body>", obj.make_string())

    def test_append2(self):
        obj = hm.Body()
        obj.append([hm.Heading(1, "テスト1"), hm.Heading(2, "テスト2")])
        obj.append([hm.Heading(3, "テスト3")])
        self.assertEqual(
            "<body>\r\n"
            "<h1>テスト1</h1>\r\n<h2>テスト2</h2>\r\n<h3>テスト3</h3>"
            "\r\n</body>",
            obj.make_string())


class Division(unittest.TestCase):
    def test_Body(self):
        obj = hm.Division()
        self.assertEqual("<div>\r\n</div>", obj.make_string())

    def test_set_class(self):
        obj = hm.Division()
        obj.set_class("test_class")
        obj.append([hm.Text("テスト")])
        self.assertEqual('<div class="test_class">\r\nテスト\r\n</div>', obj.make_string())


if __name__ == '__main__':
    unittest.main()
