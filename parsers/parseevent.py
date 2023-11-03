import re
import os
from ..classes.locations.event import Event, Choice, Choices, EventOutcome

def parse_event_outcome(outcome_description, arguments, item_dict, monster_dict):
    """Create an EventOutcome object from the outcome description and arguments."""
    # Parse and create Items, Special Effects, Attacks, Spells, Monsters, etc. from arguments
    items = []
    special_effect = None
    attacks = []
    spells = []
    monsters = []
    incomplete = False
    location_change = None
    new_event = None
    stay_in_event = False
    lose_item = None

    for arg in arguments:
        key, value = arg.split('=')
        key = key.strip()
        value = value.strip()
        
        if key == 'items':
            # Assuming value is a comma-separated list of item names
            item_names = value.split(',')
            items = [item_dict[item_name.strip()] for item_name in item_names if item_name.strip() in item_dict]

        elif key == 'monsters':
            # Assuming value is a comma-separated list of monster names
            monster_names = value.split(',')
            monsters = [monster_dict[monster_name.strip()] for monster_name in monster_names if monster_name.strip() in monster_dict]


    # Create the EventOutcome object with all the gathered information
    return EventOutcome(outcome_description, items=items, special_effect=special_effect,
                        attacks=attacks, spells=spells, monsters=monsters,
                        incomplete=incomplete, location_change=location_change,
                        new_event=new_event, stay_in_event=stay_in_event,
                        lose_item=lose_item)

def parse_choice(choice_text, item_dict, monster_dict):
    lines = choice_text.strip().split('\n')
    description = lines[0].split(':')[1].strip()
    outcome_description = lines[1].split(':')[1].strip()
    arguments = lines[2:]
    
    outcome = parse_event_outcome(outcome_description, arguments, item_dict, monster_dict)
    return Choice(description, outcome)

def parse_event_file(file_path, player, item_dict, monster_dict):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by sections
    sections = content.split('##')
    name = sections[0].strip().replace('#', '').strip()
    description = sections[1].strip()
    choices_text = sections[2].strip().split('\n\n')  # Assuming double newlines separate choices

    choices = [parse_choice(choice_text, item_dict, monster_dict) for choice_text in choices_text if choice_text.strip() != '']
    choices_object = Choices(choices)

    # Create the Event object
    event = Event(name=name, description=description, choices=choices_object, player=player)
    return event

# Usage
def generate_event_dict(tier, player, item_dict, monster_dict):
    """Generate a dictionary of events for a given tier."""
    event_directory = f'vault/t{tier}/events'  # Construct the path with tier
    event_dict = {}

    for filename in os.listdir(event_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(event_directory, filename)
            event = parse_event_file(file_path, player, item_dict, monster_dict)
            event_name = filename.rstrip('.md')  # This assumes the filename without .md is the event's name
            event_dict[event_name] = event

    return event_dict

