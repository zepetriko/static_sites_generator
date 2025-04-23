import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from functions import split_nodes_bold, split_nodes_code, split_nodes_italic, extract_markdown_images, extract_markdown_links, split_nodes_image


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("First node", TextType.CODE_TEXT)
        node2 = TextNode("Second node", TextType.CODE_TEXT)
        self.assertNotEqual(node1, node2)

    def test_type_not_eq(self):
        node1 = TextNode("First node", TextType.CODE_TEXT)
        node2 = TextNode("First node", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("First node", TextType.CODE_TEXT, "https://example.com")
        node2 = TextNode("First node", TextType.CODE_TEXT, "https://example2.com")
        self.assertNotEqual(node1, node2)

    def test_url_none(self):
        node1 = TextNode("First node", TextType.CODE_TEXT)
        node2 = TextNode("First node", TextType.CODE_TEXT, None)
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_delimeter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_code([node])
        self.assertEqual(len(new_nodes), 3)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    

if __name__ == "__main__":
    unittest.main()