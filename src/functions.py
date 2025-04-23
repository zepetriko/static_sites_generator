
from textnode import TextType, TextNode
import re



def split_nodes_code(old_nodes):
    final_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            final_list.append(old_node)
        else:
            if "`" in old_node.text:
                old_text = ["", old_node.text]
                codes = re.findall("`([^`]*)`", old_node.text)
                split_list = old_node.text.split("`")
                
                if (len(split_list) % 2) == 0:
                    raise Exception("second ` not found, invalid Markdown syntax")
                for code in codes:
                    sections = old_text[1].split(f"`{code}`", 1)
                    final_list.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                    final_list.append(TextNode(code, TextType.CODE_TEXT))
                    old_text = sections
                if sections[1] != '':
                    final_list.append(TextNode(sections[1], TextType.NORMAL_TEXT))
            else:
                final_list.append(old_node)
    return final_list

def split_nodes_bold(old_nodes):
    final_list = []
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.NORMAL_TEXT:
            final_list.append(old_node)
        else:
            if "**" in old_node.text:
                old_text = ["", old_node.text]
                bolds = re.findall("\*\*(.*?)\*\*", old_node.text)
                split_list = old_node.text.split("**")
                if (len(split_list) % 2) == 0:
                    raise Exception("second ** not found, invalid Markdown syntax")
                for bold in bolds:
                    sections = old_text[1].split(f"**{bold}**", 1)
                    final_list.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                    final_list.append(TextNode(bold, TextType.BOLD_TEXT))
                    old_text = sections
                    
                if sections[1] != '':
                    final_list.append(TextNode(sections[1], TextType.NORMAL_TEXT))
            else:
                final_list.append(old_node)
    return final_list

def split_nodes_italic(old_nodes):
    final_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            final_list.append(old_node)
        else:
            if "_" in old_node.text:
                old_text = ["", old_node.text]
                italics = re.findall("_(.*?)_", old_node.text)
                split_list = old_node.text.split("_")
                
                if (len(split_list) % 2) == 0:
                    raise Exception("second _ not found, invalid Markdown syntax")
                for italic in italics:
                    sections = old_text[1].split(f"_{italic}_", 1)
                    final_list.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                    final_list.append(TextNode(italic, TextType.ITALIC_TEXT))
                    old_text = sections
                if sections[1] != '':
                    final_list.append(TextNode(sections[1], TextType.NORMAL_TEXT))
            else:
                final_list.append(old_node)
    return final_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    final_list = []
    for old_node in old_nodes:
        old_text = ["", old_node.text]
        images = extract_markdown_images(old_node.text)
        if len(images) < 1:
            if old_node.text == "":
                return Exception("No text in node")
            final_list.append(old_node)
        else:
            for image in images:
                sections = old_text[1].split(f"![{image[0]}]({image[1]})", 1)
                final_list.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                final_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                old_text = sections
            if sections[1] != '':
                final_list.append(TextNode(sections[1], TextType.NORMAL_TEXT))
    return final_list

def split_nodes_link(old_nodes):
    final_list = []
    for old_node in old_nodes:
        old_text = ["", old_node.text]
        links = extract_markdown_links(old_node.text)
        if len(links) < 1:
            if old_node.text == "":
                return Exception("No text in node")
            final_list.append(old_node)
        else:
            for link in links:
                sections = old_text[1].split(f"[{link[0]}]({link[1]})", 1)
                final_list.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                final_list.append(TextNode(link[0], TextType.LINK, link[1]))
                old_text = sections
            if sections[1] != '':
                final_list.append(TextNode(sections[1], TextType.NORMAL_TEXT))
    return final_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL_TEXT)
    node1 = split_nodes_code([node])
    node2 = split_nodes_bold(node1)
    node3 = split_nodes_italic(node2)
    node4 = split_nodes_image(node3)
    node5 = split_nodes_link(node4)
    return node5

