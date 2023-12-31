import re
import os
from ..classes.locations.event import Event, Choice, Choices, EventOutcome

def parse_event_outcome(outcome_description, arguments, item_dict, monster_dict):
    """Create an EventOutcome object from the outcome description and arguments."""
    # Parse and create Items, Special Effects, Attacks, Spells, Monsters, etc. from arguments
    effects = {
        "items" : [],
        "special_effect" : None,
        "attacks" : [],
        "spells" : [],
        "monsters" : [],
        "incomplete" : False,
        "location_change" : None,
        "new_event" : None,
        "stay_in_event" : False,
        "lose_item" : None,
        "gold_change" : 0,
        "hp" : 0
    }

    items_pattern = re.compile(r'\\\[\[\[(.*?)\]\]\]')
    monsters_pattern = re.compile(r'\\\[\[\[(.*?)\]\]\]')

    for arg in arguments:
        key, value = arg.split('=')
        key = key.replace('-', '').lower().strip()

        if key == 'items':
            item_matches = items_pattern.findall(value)
            items = [item_dict[item_name.strip().lower()] for item_name in item_matches if item_name.strip().lower() in item_dict]
            effects["items"] = items
        elif key == 'monsters':
            monster_matches = monsters_pattern.findall(value)
            monsters = [monster_dict[monster_name.strip().lower()] for monster_name in monster_matches if monster_name.strip().lower() in monster_dict]
            effects["monsters"] = monsters
        else:
            # Convert numeric values to integers
            if value.isdigit():
                effects[key] = int(value)
            else:
                effects[key] = value
        
    # Create the EventOutcome object with all the gathered information
    return EventOutcome(outcome_description, items=effects["items"], special_effect=effects["special_effect"],
                        attacks=effects["attacks"], spells=effects["spells"], monsters=effects["monsters"],
                        incomplete=effects["incomplete"], location_change=effects["location_change"],
                        new_event=effects["new_event"], stay_in_event=effects["stay_in_event"],
                        lose_item=effects["lose_item"], gold_change=effects["gold_change"], health_change=effects["hp"])

def parse_choice(choice_text, item_dict, monster_dict):
    lines = choice_text.strip().split('\n')
    description = lines[0].split(':')[1].strip()
    outcome_description = lines[1].split(':')[1].strip()
    arguments = lines[2:]
    
    outcome = parse_event_outcome(outcome_description, arguments, item_dict, monster_dict)
    return Choice(description, outcome)

def parse_event_file(file_path, player, item_dict, monster_dict):
    event_name = os.path.basename(file_path).replace('.md', '').replace('_', ' ').title()
    
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by sections and remove any empty lines or irrelevant headers
    sections = content.split('##')
    description = sections[1].strip()
   # First, split the entire choices section into lines
    choices_lines = sections[2].strip().split('\n')
    
    # Then, group lines into choices
    choices_text = []
    current_choice = []
    for line in choices_lines:
        if line.startswith('Description:') and current_choice:
            # When we hit a new 'Description:', we join the current choice's lines and reset for the next one
            choices_text.append('\n'.join(current_choice).strip())
            current_choice = [line]  # Start new choice with current line
        elif line.strip() and not line.startswith('Choices:'):
            # Otherwise, add line to current choice
            current_choice.append(line)
    
    # Don't forget to 
    # add the last choice if it exists
    if current_choice:
        choices_text.append('\n'.join(current_choice).strip())
    
    # Assuming that parse_choice function correctly processes each individual choice text
    choices = [parse_choice(choice, item_dict, monster_dict) for choice in choices_text]
    choices_object = Choices(choices)

    event = Event(name=event_name, description=description, choices=choices_object, player=player)
    return event

# Usage
def generate_event_dict(tier, player, item_dict, monster_dict):
    """Generate a dictionary of events for a given tier."""
    event_directory = os.path.join(os.path.dirname(__file__),'..', f'vault/t{tier}/events')
    event_directory = os.path.normpath(event_directory)
    event_dict = {}

    for filename in os.listdir(event_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(event_directory, filename)
            event = parse_event_file(file_path, player, item_dict, monster_dict)
            event_name = filename.rstrip('.md')  # This assumes the filename without .md is the event's name
            event_dict[event_name] = event

    return event_dict

