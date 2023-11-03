from .parseitem import generate_item_dict
from .parsemonster import generate_monster_dict
from .parseevent import generate_event_dict
from .parseencounter import generate_encounter_dict
from .parsetown import generate_town_dict
from .parsenode import generate_nodes_dict

def allparse(tier, player):
    # Parse events, encounters, and towns first
    item_dict = generate_item_dict(tier)
    monster_dict = generate_monster_dict(tier, item_dict)
    event_dict = generate_event_dict(tier, player, item_dict, monster_dict)
    encounter_dict = generate_encounter_dict(tier, monster_dict, player)
    town_dict = generate_town_dict(tier, event_dict)
    
    # Parse nodes last since they depend on events, encounters, and towns
    nodes_dict = generate_nodes_dict(tier, event_dict, encounter_dict, town_dict)
    
    # Convert nodes_dict to a list of nodes
    nodes_list = list(nodes_dict.values())
    
    return nodes_list