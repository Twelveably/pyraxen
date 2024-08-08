import yaml
import os


def save_config(config, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        yaml.dump(config, file, sort_keys=False)


class FileHandler:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.ensure_folders()

    def ensure_folders(self):
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def load_config(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
