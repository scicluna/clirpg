import os
from copy import deepcopy
from ..classes.locations.encounter import Encounter

def parse_monster_list(monster_section, monster_dict):
    """Helper function to parse the monster list and retrieve monster objects from a dictionary."""
    monsters = []
    monster_lines = monster_section.strip().split('\n')
    for line in monster_lines:
        if line.startswith('[[') and line.endswith(']]'):
            # Get the monster name from the Obsidian markdown link
            monster_name = line.strip('[]')
            # Get the monster object from the dictionary, if it exists
            monster = monster_dict.get(monster_name.strip())
            if monster:
                # Deepcopy to prevent shared state if multiple encounters have the same monster type
                monsters.append(deepcopy(monster))
            else:
                print(f"Monster '{monster_name}' not found in monster dictionary, skipping...")
    return monsters

def parse_encounter_file(file_path, monster_dict, player):
    # Use the filename (without the extension) as the encounter name
    encounter_name = os.path.basename(file_path).replace('.md', '').replace('_', ' ').title()

    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by sections
    sections = content.split('##')
    monster_section = sections[1].strip() if len(sections) > 1 else ""

    # Parse monster list
    monsters = parse_monster_list(monster_section, monster_dict)

    # Create the Encounter object with the name from the filename
    encounter = Encounter(name=encounter_name, monsters=monsters, player=player)
    return encounter

# Usage:
# Assuming the directory structure is 'vault/t1/encounters'
def generate_encounter_dict(tier: int, monster_dict, player):
    """Generate a dictionary of encounters for the given tier"""
    encounter_directory = os.path.join(os.path.dirname(__file__),'..', f'vault/t{tier}/encounters')
    encounter_directory = os.path.normpath(encounter_directory)
    encounter_dict = {}

    for filename in os.listdir(encounter_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(encounter_directory, filename)
            encounter = parse_encounter_file(file_path, monster_dict, player)
            encounter_name = filename.rstrip('.md')  # This assumes the filename without .md is the encounter's name
            encounter_dict[encounter_name] = encounter
    
    return encounter_dict

