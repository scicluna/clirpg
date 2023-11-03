import os
from ..classes.town.town import Town, Location

def parse_location(location_text, event_dict):
    parts = location_text.split(':')
    name = parts[0].strip()
    event_link = parts[1].strip()
    
    # Strip Obsidian link syntax if present
    if event_link.startswith('[[') and event_link.endswith(']]'):
        event_name = event_link[2:-2]
    else:
        event_name = event_link

    event = event_dict.get(event_name)
    if event is None:
        raise ValueError(f"Event '{event_name}' is not defined.")
    return Location(name, event)

def parse_town(file_path, event_dict):
    # Extract the town name from the file name, assuming it's the name before '.md'
    town_name = os.path.basename(file_path).replace('.md', '')
    
    with open(file_path, 'r') as file:
        # Skip the first line if it's the town name with '#'
        locations_text = file.readlines()[1:]  # This assumes the first line is not needed
        
    # Filter lines that are not locations (ignoring '## Locations' and empty lines)
    location_texts = [line.strip() for line in locations_text if line.strip() and not line.startswith('##')]

    visit_locations = [parse_location(location_text, event_dict) for location_text in location_texts if location_text.strip()]
    return Town(town_name, visit_locations)

def generate_town_dict(tier: int, event_dict):
    """Generate town dictionary for the given tier"""
    town_directory = f'vault/t{tier}/towns'
    town_dict = {}

    for filename in os.listdir(town_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(town_directory, filename)
            town = parse_town(file_path, event_dict)
            town_dict[town.name] = town
    
    return town_dict
