class Converter:
    def __init__(self):
        pass

    def convert_to_oraxen(self, itemsadder_config):
        oraxen_config = {}

        namespace = itemsadder_config.get('info', {}).get('namespace', '')
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
                    # TODO
                }
            }
            oraxen_config[item_name] = oraxen_item

        return oraxen_config
