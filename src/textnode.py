from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and \
                    self.text_type == other.text_type and \
                    self.url == other.url
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    text_type_to_html = {
        TextType.NORMAL_TEXT: lambda node: LeafNode(None, node.text),
        TextType.BOLD_TEXT: lambda node: LeafNode("b", node.text),
        TextType.ITALIC_TEXT: lambda node: LeafNode("i", node.text),
        TextType.CODE_TEXT: lambda node: LeafNode("code", node.text),
        TextType.LINK: lambda node: LeafNode("a", node.text, {"href": node.url}),
        TextType.IMAGE: lambda node: LeafNode("img", "", {"src": node.url, "alt": node.text})
    }

    if text_node.text_type not in text_type_to_html:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    
    return text_type_to_html[text_node.text_type](text_node)