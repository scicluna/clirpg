import os
from copy import deepcopy
from ..classes.locations.encounter import Encounter

def parse_monster_list(monster_section, monster_dict):
    """Helper function to parse the monster list and retrieve monster objects from a dictionary."""
    monsters = []
    monster_names = monster_section.strip().split('\n')
    for monster_name in monster_names:
        # Get the monster object from the dictionary, if it exists
        monster = monster_dict.get(monster_name.strip())
        if monster:
            # Deepcopy to prevent shared state if multiple encounters have the same monster type
            monsters.append(deepcopy(monster))
    return monsters

def parse_encounter_file(file_path, monster_dict, player):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by sections
    sections = content.split('##')
    name_section = sections[0].strip()
    monster_section = sections[1].strip() if len(sections) > 1 else ""

    # Parse name
    name = name_section.split('\n')[0].replace('#', '').strip()

    # Parse monster list
    monsters = parse_monster_list(monster_section, monster_dict)

    # Create the Encounter object
    encounter = Encounter(name=name, monsters=monsters, player=player)
    return encounter

# Usage:
# Assuming the directory structure is 'vault/t1/encounters'
def generate_encounter_dict(tier: int, monster_dict, player):
    """Generate a dictionary of encounters for the given tier"""
    encounter_directory = f'vault/t{tier}/encounters'
    encounter_dict = {}

    for filename in os.listdir(encounter_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(encounter_directory, filename)
            encounter = parse_encounter_file(file_path, monster_dict, player)
            encounter_name = filename.rstrip('.md')  # This assumes the filename without .md is the encounter's name
            encounter_dict[encounter_name] = encounter
    
    return encounter_dict

