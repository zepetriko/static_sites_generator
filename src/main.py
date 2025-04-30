import os
import shutil
from functions import generate_pages_recursive
import sys 

def copy_static_files(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    copy_directory_contents(source_dir, dest_dir)

def copy_directory_contents(src_dir, dst_dir):
    for item in os.listdir(src_dir):
        src_item_path = os.path.join(src_dir, item)
        dst_item_path = os.path.join(dst_dir, item)

        if os.path.isfile(src_item_path):
            print(f"Copying file: {src_item_path} to {dst_item_path}")
            shutil.copy(src_item_path, dst_item_path)
        else:
            print(f"Creating directory: {dst_item_path}")
            os.mkdir(dst_item_path)

            copy_directory_contents(src_item_path, dst_item_path)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    copy_static_files("static", "docs")
    print("Static files copied successfully!")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    print("Page Generated")

if __name__ == "__main__":
    main()