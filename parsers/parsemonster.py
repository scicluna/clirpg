import os
from ..classes.entities.monster import Monster

def parse_monster_file(file_path, item_dict):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    monster_data = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith('# '):  # Monster name
            monster_name = line[2:].strip()
            monster_data['name'] = monster_name
        elif line.startswith('## '):  # New section
            current_section = line[2:].strip().lower()
        else:
            if current_section and line:
                # Process based on current section
                if current_section in ['hp', 'damage', 'defense', 'gold', 'exp']:
                    monster_data[current_section] = int(line)
                elif current_section == 'loot' and line.startswith('[['):
                    # Parse the item by removing the Obsidian markdown link syntax
                    item_name = line.strip('[]')
                    if item_name in item_dict:
                        monster_data.setdefault('loot', []).append(item_dict[item_name])
                    else:
                        print(f"Item '{item_name}' not found in item dictionary, skipping...")

    # Create the Monster object with the extracted data
    monster = Monster(
        name=monster_data['name'],
        hp=monster_data['hp'],
        damage=monster_data['damage'],
        defense=monster_data['defense'],
        loot=monster_data.get('loot', []),
        gold=monster_data.get('gold', 0),
        exp=monster_data.get('exp', 0)
    )
    return monster

# Usage:
def generate_monster_dict(tier: int, item_dict):
    """Generate monster dictionary for the given tier using items from item_dict."""
    monster_directory = f'vault/t{tier}/monsters'
    monster_dict = {}

    for filename in os.listdir(monster_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(monster_directory, filename)
            monster = parse_monster_file(file_path, item_dict)
            monster_dict[monster.name] = monster
    return monster_dict

# Example usage
# item_dict = ... # this should be populated from your item parsing logic
# monster_dict = generate_monster_dict(tier=1, item_dict)
# print(monster_dict)  # This will print the dictionary of Monster objects with their loot as item objects
