import unittest

import heloblock.html_string_maker as hm


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


if __name__ == '__main__':
    unittest.main()
