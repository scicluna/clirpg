import os
import re
from ..classes.actions.item import Item, ItemType

def parse_item_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expressions to match different parts of the template
    name_regex = re.compile(r'^# (.+)$', re.MULTILINE)
    description_regex = re.compile(r'## Description:\n(.+)', re.MULTILINE)
    type_regex = re.compile(r'## Type:\n(.+)', re.MULTILINE)
    stats_regex = re.compile(r'## Stats:\n((?:\(.*\)\n?)*)', re.MULTILINE)
    special_regex = re.compile(r'## Special:\n(.*)', re.MULTILINE)

    # Find matches
    name_match = name_regex.search(content)
    description_match = description_regex.search(content)
    type_match = type_regex.search(content)
    stats_match = stats_regex.search(content)
    special_match = special_regex.search(content)

    # Parse stats
    stats = {}
    if stats_match:
        stats_lines = stats_match.group(1).strip().split('\n')
        for line in stats_lines:
            key, value = line.strip('()').split(' = ')
            stats[key] = int(value) if value.isdigit() else value  # Assuming all stats are integers

    # Creating the item object
    item = Item(
        name=name_match.group(1).strip() if name_match else 'Unknown',
        description=description_match.group(1).strip() if description_match else 'No description',
        quantity=1,  # Default quantity to 1, adjust as needed
        item_type=ItemType[type_match.group(1).strip().upper()] if type_match else ItemType.SPECIAL,
        dmg=stats.get('dmg', 0),
        defense=stats.get('defense', 0),
        healing=stats.get('healing', 0),
        special=special_match.group(1).strip() if special_match else None
    )

    return item

# Usage:
# Assuming the directory structure is 'vault/t1/items'
def generate_item_dict(tier: int):
    """Generate item dictionary for the given tier"""
    item_directory = f'vault/t{tier}/items'
    item_dict = {}

    for filename in os.listdir(item_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(item_directory, filename)
            item = parse_item_file(file_path)
            item_dict[item.name] = item
    return item_dict
