import os
import shutil
from converter_processor import process_files


def main():
    contents_folder = 'input'
    output_folder = 'output'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    process_files(contents_folder, output_folder)
    print("Processing complete!")


if __name__ == "__main__":
    main()
