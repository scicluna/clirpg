import os
from ..classes.locations.node import Node

def parse_node(node_text, event_dict, encounter_dict, town_dict):
    lines = node_text.strip().split('\n')
    header = lines[0].strip()
    node_number, node_name = header.split('. ', 1)
    node_number = int(node_number)  # Assuming the node number is always an integer

    # Determine the type of game element this node holds (event, encounter, or town)
    element_type = lines[2].strip('## ').lower()  # This should get "Event", "Encounter", or "Town"
    element_name = lines[3].strip()
    
    # Fetch the game element from the appropriate dictionary
    game_element = None
    if element_type == 'event':
        game_element = event_dict.get(element_name)
    elif element_type == 'encounter':
        game_element = encounter_dict.get(element_name)
    elif element_type == 'town':
        game_element = town_dict.get(element_name)
    
    if game_element is None:
        raise ValueError(f"{element_type.title()} '{element_name}' is not defined.")

    # Create the node without connections initially
    node = Node(node_number, node_name, game_element)
    
    # Return the node and the connection data for processing in the second pass
    connection_data = lines[5:]  # The connections part of the text
    return node, connection_data

def connect_nodes(nodes_dict, connections_data):
    for node_name, connection_lines in connections_data.items():
        node = nodes_dict[node_name]
        for connection_text in connection_lines:
            if connection_text.strip():
                connected_node_name, distance = connection_text.split(' : ')
                distance = float(distance.strip())  # Assuming distance is a float
                connected_node = nodes_dict.get(connected_node_name.strip())

                if connected_node is None:
                    raise ValueError(f"Node '{connected_node_name}' is not defined.")

                # Connect the nodes
                node.connect_nodes(connected_node, distance)

def parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict):
    nodes_dict = {}
    connections_data = {}

    # First pass: create nodes
    for node_text in nodes_texts:
        node, connection_data = parse_node(node_text, event_dict, encounter_dict, town_dict)
        nodes_dict[node.name] = node
        connections_data[node.name] = connection_data

    # Second pass: connect nodes
    connect_nodes(nodes_dict, connections_data)

    return nodes_dict

def read_node_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_directory_nodes(directory_path, event_dict, encounter_dict, town_dict):
    nodes_texts = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            file_path = os.path.join(directory_path, filename)
            node_text = read_node_file(file_path)
            nodes_texts.append(node_text)
    return parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict)

def generate_nodes_dict(tier: int, event_dict, encounter_dict, town_dict):
    """Generate nodes dictionary for the given tier"""
    nodes_directory = f'vault/t{tier}/nodes'
    return parse_directory_nodes(nodes_directory, event_dict, encounter_dict, town_dict)