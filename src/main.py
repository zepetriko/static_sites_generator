import os
import shutil

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
    copy_static_files("static", "public")
    print("Static files copied sucessfully!")

if __name__ == "__main__":
    main()