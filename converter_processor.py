import os
import shutil
import json
import yaml


def load_yaml_config(file_path):
    """Load a YAML configuration file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def save_yaml_config(data, output_file_path):
    """Save data to a YAML configuration file."""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, sort_keys=False)


def process_files(contents_folder, output_folder):
    """Process all relevant files and convert them to the desired format."""
    for root, dirs, files in os.walk(contents_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith('.yml') or file_name.endswith('.yaml'):
                process_yaml(file_path, output_folder, contents_folder)
            elif file_name.endswith('.json'):
                process_json(file_path, output_folder, contents_folder)
            elif file_name.endswith('.png'):
                process_texture(file_path, output_folder, contents_folder)


def process_yaml(file_path, output_folder, contents_folder):
    """Process YAML files and convert them to the desired format."""
    print(f"Processing YAML file '{file_path}'...")

    itemsadder_config = load_yaml_config(file_path)
    namespace = itemsadder_config.get('info', {}).get('namespace', '')

    if not namespace:
        print(f"Warning: No namespace found in YAML file '{file_path}'")
        return

    # Capture the base folder of the YAML item
    base_folder, folder_type = get_base_folder(file_path, ['models', 'textures'])

    # Process each item in the config
    items = itemsadder_config.get('items', {})
    for item_name, item_data in items.items():
        # Prepare the output path for the YAML config
        relative_path = os.path.basename(file_path)
        output_path = os.path.join(output_folder, 'items', namespace, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Convert and save the YAML config
        oraxen_config = convert_to_oraxen(itemsadder_config, namespace, folder_type)
        save_yaml_config(oraxen_config, output_path)

        process_model_textures(item_data, namespace, output_folder, base_folder)


def process_json(file_path, output_folder, contents_folder):
    """Process JSON model files."""
    print(f"Processing JSON file '{file_path}'...")

    # Read the JSON model file
    with open(file_path, 'r', encoding='utf-8') as file:
        model_data = json.load(file)

    # Extract the namespace and model path
    namespace = get_namespace_from_path(file_path)
    model_path = get_model_path_from_file(file_path)

    # Prepare the output path for models
    output_path = os.path.join(output_folder, 'pack', 'models', namespace)
    os.makedirs(output_path, exist_ok=True)

    # Replace texture paths in the JSON model data
    if 'textures' in model_data:
        for key, texture in model_data['textures'].items():
            model_data['textures'][key] = texture.replace(':', '/')

    # Save the updated model data
    relative_path = os.path.basename(file_path)
    with open(os.path.join(output_path, relative_path), 'w', encoding='utf-8') as file:
        json.dump(model_data, file, indent=4)


def process_texture(file_path, output_folder, contents_folder):
    """Process texture PNG files."""
    print(f"Processing texture file '{file_path}'...")

    # Extract the namespace and texture path from the file path
    namespace = get_namespace_from_path(file_path)
    texture_path = get_texture_path_from_file(file_path)

    # Prepare the output path for textures
    output_path = os.path.join(output_folder, 'pack', 'textures', namespace)
    os.makedirs(output_path, exist_ok=True)

    # Copy the texture file
    shutil.copy2(file_path, os.path.join(output_path, os.path.basename(file_path)))


def convert_to_oraxen(itemsadder_config, namespace, folder_type):
    """Convert ItemsAdder YAML config to the desired format."""
    oraxen_config = {}

    items = itemsadder_config.get('items', {})

    for item_name, item_data in items.items():
        oraxen_item = {
            'displayname': item_data.get('display_name', ''),
            'material': item_data.get('resource', {}).get('material', 'STONE'),
            'Pack': {
                'generate_model': item_data.get('resource', {}).get('generate', False),
                'model': f"{namespace}/{item_data.get('resource', {}).get('model_path', '')}",
                'custom_model_data': item_data.get('resource', {}).get('model_id', 0)
            },
            'Mechanics': {
            }
        }
        oraxen_config[item_name] = oraxen_item

    return oraxen_config


def get_base_folder(file_path, target_folders):
    parts = file_path.split(os.sep)
    for target_folder in target_folders:
        if target_folder in parts:
            target_index = parts.index(target_folder)
            base_folder = os.path.join(*parts[:target_index])
            return base_folder, target_folder
    return os.path.dirname(file_path), ''


def get_namespace_from_path(file_path):
    parts = file_path.split(os.sep)
    if 'configs' in parts:
        index = parts.index('configs') - 1
        return parts[index]
    if 'resourcepack' in parts:
        index = parts.index('resourcepack') - 1
        return parts[index]
    return ''


def get_model_path_from_file(file_path):
    parts = file_path.split(os.sep)
    if 'models' in parts:
        index = parts.index('models') + 1
        return os.path.join(*parts[index:])
    return ''


def get_texture_path_from_file(file_path):
    parts = file_path.split(os.sep)
    if 'textures' in parts:
        index = parts.index('textures') + 1
        return os.path.join(*parts[index:])
    return ''


def process_model_textures(item_data, namespace, output_folder, base_folder):
    model_path = item_data.get('resource', {}).get('model_path', '')

    textures = item_data.get('textures', [])
    for texture in textures:
        texture_file_path = os.path.join(base_folder, 'textures', namespace, texture)
        if os.path.isfile(texture_file_path):
            process_texture(texture_file_path, output_folder, contents_folder)
        else:
            print(f"Texture file '{texture_file_path}' not found.")


if __name__ == "__main__":

    contents_folder = 'input/contents'
    output_folder = 'output'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    process_files(contents_folder, output_folder)
    print("Processing complete!")
