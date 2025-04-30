
from textnode import TextType, TextNode
import re
import os


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
        if old_node.text_type != TextType.NORMAL_TEXT:
            final_list.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images: #no images found
            final_list.append(old_node)
        else:
            text_remaining = old_node.text
            for image in images:
                img_tag = f"![{image[0]}]({image[1]})"
                if img_tag in text_remaining:
                    parts = text_remaining.split(img_tag, 1)

                    if parts[0]:
                        final_list.append(TextNode(parts[0], TextType.NORMAL_TEXT))
                    
                    final_list.append(TextNode(image[0], TextType.IMAGE, image[1]))

                    text_remaining = parts[1]

            if text_remaining:
                final_list.append(TextNode(text_remaining, TextType.NORMAL_TEXT))

    return final_list

def split_nodes_link(old_nodes):
    final_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            final_list.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links: #no links found
            final_list.append(old_node)
        else:
            text_remaining = old_node.text
            for link in links:
                img_tag = f"[{link[0]}]({link[1]})"
                if img_tag in text_remaining:
                    parts = text_remaining.split(img_tag, 1)

                    if parts[0]:
                        final_list.append(TextNode(parts[0], TextType.NORMAL_TEXT))
                    
                    final_list.append(TextNode(link[0], TextType.LINK, link[1]))

                    text_remaining = parts[1]

            if text_remaining:
                final_list.append(TextNode(text_remaining, TextType.NORMAL_TEXT))
                
    return final_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL_TEXT)
    node1 = split_nodes_code([node])
    node2 = split_nodes_bold(node1)
    node3 = split_nodes_italic(node2)
    node4 = split_nodes_image(node3)
    node5 = split_nodes_link(node4)
    return node5


def extract_title(markdown):
    lines = markdown.split('\n')

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    from markdown_blocks import markdown_to_html_node

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    dir_entries = os.listdir(dir_path_content)

    for entry in dir_entries:
        entry_path = os.path.join(dir_path_content, entry)
        public_path = entry_path.replace(dir_path_content, dest_dir_path)
        public_path  = os.path.splitext(public_path)[0] + '.html'

        if os.path.isfile(entry_path) and entry_path.endswith('.md'):
            os.makedirs(os.path.dirname(public_path), exist_ok=True)

            generate_page(entry_path, template_path, public_path)
        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))