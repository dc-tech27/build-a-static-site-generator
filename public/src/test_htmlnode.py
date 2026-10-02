import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Google",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", props={"src": "cat.png"})
        self.assertEqual(node.props_to_html(), ' src="cat.png"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_values_stored(self):
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", None, [child], {"class": "wrapper"})
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"class": "wrapper"})

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "intro"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, children: None, {'class': 'intro'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_a_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hi')")
        self.assertEqual(node.to_html(), "<code>print('hi')</code>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            repr(node),
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})",
        )

if __name__ == "__main__":
    unittest.main()