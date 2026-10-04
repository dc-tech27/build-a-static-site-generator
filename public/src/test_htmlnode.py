import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "wrapper", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="wrapper" id="main"><span>child</span></div>',
        )

    def test_to_html_child_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Visit "),
                LeafNode("a", "Boot.dev", {"href": "https://www.boot.dev"}),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p>Visit <a href="https://www.boot.dev">Boot.dev</a></p>',
        )

    def test_to_html_nested_siblings(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
                ParentNode("li", [LeafNode("i", "three")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>one</b></li><li>two</li><li><i>three</i></li></ul>",
        )

    def test_to_html_mixed_leaf_and_parent_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode(None, "Body "), LeafNode("b", "bold")]),
                LeafNode(None, "trailing text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Body <b>bold</b></p>trailing text</div>",
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "section",
            [ParentNode("div", [ParentNode("p", [ParentNode("span", [LeafNode("b", "deep")])])])],
        )
        self.assertEqual(
            node.to_html(),
            "<section><div><p><span><b>deep</b></span></p></div></section>",
        )

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_error_bubbles_from_child(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", None)])])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = ParentNode("div", [LeafNode("b", "hi")], {"class": "x"})
        self.assertEqual(
            repr(node),
            "ParentNode(div, children: [LeafNode(b, hi, None)], {'class': 'x'})",
        )

if __name__ == "__main__":
    unittest.main()