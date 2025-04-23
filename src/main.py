from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import split_nodes_bold, split_nodes_italic, split_nodes_code, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

def main():
    # test = TextNode("test text", TextType.LINK, "https://test.com")
    # test1 = HTMLNode(tag="<p>", value="valueee", children=[], props={"href": "https://www.google.com", "target": "_blank",})
    # node = TextNode("This is **text** with an _italic_ word and a ", TextType.NORMAL_TEXT, None)
    # new_nodes = split_nodes_bold([node])
    
    # node1 = TextNode(
    #     "",
    #     TextType.NORMAL_TEXT,
    # )
    # new_nodes1 = split_nodes_image([node1])
    
    # node2 = TextNode(
    # "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    # TextType.NORMAL_TEXT,
    # )
    # new_nodes2 = split_nodes_link([node2])

    # text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # final_text = text_to_textnodes(text)
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    blocks = markdown_to_blocks(md)
    print(blocks)

main()