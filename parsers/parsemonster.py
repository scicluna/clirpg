import os
from ..classes.entities.monster import Monster

def parse_monster_file(file_path, item_dict):
    # Extract the monster's name from the file name, assuming the format is "monstername.md"
    monster_name = os.path.basename(file_path).replace('.md', '').replace('_', ' ').title()

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    monster_data = {'name': monster_name}  # Initialize with monster's name
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith('## '):  # New section
            current_section = line[2:].strip().lower().replace(':', '')  # remove colon if it's there
        elif line:  # Ignore empty lines
            # Process based on current section
            if current_section in ['hp', 'damage', 'defense', 'gold', 'exp']:
                # Assign the integer value of the line under the corresponding section
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
        hp=monster_data.get('hp'),
        damage=monster_data.get('damage'),
        defense=monster_data.get('defense'),
        loot=monster_data.get('loot', []),
        gold=monster_data.get('gold', 0),
        exp=monster_data.get('exp', 0)
    )
    return monster

# Usage:
def generate_monster_dict(tier: int, item_dict):
    """Generate monster dictionary for the given tier using items from item_dict."""
    monster_directory = os.path.join(os.path.dirname(__file__),'..', f'vault/t{tier}/monsters')
    monster_directory = os.path.normpath(monster_directory)  # Normalize the path
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
