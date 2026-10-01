import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("Plain text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_explicit_none_url_equals_default(self):
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click me", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq_non_textnode(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, "This is a text node")

    def test_repr(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node), "TextNode(Click me, link, https://www.boot.dev)"
        )


if __name__ == "__main__":
    unittest.main()