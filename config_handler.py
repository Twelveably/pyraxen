import os
import yaml

# Function to load YAML config
def load_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Function to save YAML config
def save_yaml_config(config, output_file_path):
    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, sort_keys=False)

# Function to convert ItemsAdder config to Oraxen format
def convert_to_oraxen(itemsadder_config, namespace):
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
