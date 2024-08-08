import os
from file_handler import FileHandler, save_config
from converter import Converter


def process_folder(input_folder, output_folder):
    file_handler = FileHandler(input_folder, output_folder)
    converter = Converter()

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.yml') or file_name.endswith('.yaml'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            print(f"Processing {input_path}...")

            itemsadder_config = file_handler.load_config(input_path)
            oraxen_config = converter.convert_to_oraxen(itemsadder_config)
            save_config(oraxen_config, output_path)

            print(f"Saved to {output_path}")


def main():
    input_folder = 'input'
    output_folder = 'output'

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_folder(input_folder, output_folder)
    print("Conversion complete!")


if __name__ == "__main__":
    main()
