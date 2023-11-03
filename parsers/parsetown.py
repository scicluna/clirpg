import os
from ..classes.town.town import Town, Location

def parse_location(location_text, event_dict):
    name, event_name = location_text.split(':')
    name = name.strip()
    event = event_dict.get(event_name.strip())
    if event is None:
        raise ValueError(f"Event '{event_name}' is not defined.")
    return Location(name, event)

def parse_town(town_text, event_dict):
    lines = town_text.strip().split('\n')
    town_name = lines[0].strip()
    location_texts = lines[2:]  # Skip the '## Locations' line
    visit_locations = [parse_location(location_text, event_dict) for location_text in location_texts if location_text.strip() and not location_text.strip() == '(Exit)']
    return Town(town_name, visit_locations)

def generate_town_dict(tier: int, event_dict):
    """Generate town dictionary for the given tier"""
    town_directory = f'vault/t{tier}/towns'
    town_dict = {}

    for filename in os.listdir(town_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(town_directory, filename)
            with open(file_path, 'r') as file:
                town_text = file.read()
                town = parse_town(town_text, event_dict)
                town_dict[town.name] = town
    return town_dict
