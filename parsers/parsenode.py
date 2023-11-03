import os
from ..classes.locations.node import Node
import re

def parse_node(file_path, node_text, event_dict, encounter_dict, town_dict):
    lines = node_text.strip().split('\n')
    header = os.path.basename(file_path).replace('.md', '')
    node_number, node_name = header.split('. ', 1)
    node_number = int(node_number.replace('#', '').strip())

    element_type = None
    linked_element_name = None
    connections_start_index = None

    # Loop to find the element type and linked element name
    for i, line in enumerate(lines):
        if line.startswith('## ') and element_type is None and line.strip('## '):
            element_type = line.strip('## ').lower()
        elif line.startswith('[[') and element_type is not None and linked_element_name is None:
            linked_element_name = re.search(r'\[\[([^\]]+)\]\]', line).group(1)
        elif line.strip('## ') == 'Connected Nodes:':
            connections_start_index = i  # Mark the start index for connections
            break  # Break the loop as we've found the header for connections

    if element_type is None or linked_element_name is None:
        raise ValueError(f"Element type or linked element name not found. ElementType={element_type} LinkedElementName={linked_element_name}")

    # Fetch the game element from the appropriate dictionary
    game_element = None
    if element_type == 'event':
        game_element = event_dict.get(linked_element_name)
    elif element_type == 'encounter':
        game_element = encounter_dict.get(linked_element_name)
    elif element_type == 'town':
        game_element = town_dict.get(linked_element_name)

    if game_element is None:
        raise ValueError(f"{element_type.title()} '{linked_element_name}' is not defined.")

    node = Node(node_number, node_name, game_element)

    # Parse the connection data, only if connections_start_index is set
    connection_data = []
    if connections_start_index is not None:
        connection_pattern = r'\-\s*\[\[\((\d+)\)\s*\.\s*([^]]+)\]\]\s*:\s*(\d+)'
        for line in lines[connections_start_index + 1:]:
            match = re.match(connection_pattern, line)
            if match:
                connected_node_number, connected_node_name, distance = match.groups()
                connection_data.append((int(connected_node_number), connected_node_name, int(distance)))

    return node, connection_data

def connect_nodes(nodes_dict, connections_data):
    for node, connection_lines in connections_data.items():
        for connected_node_number, connected_node_name, distance in connection_lines:
            # Here we use the node number and name to find the correct node
            # Assuming that the node name is unique enough or you could enhance this to make sure it matches the number as well
            connected_node = next((n for n in nodes_dict.values() if n.number == connected_node_number and n.name == connected_node_name), None)
            
            if connected_node:
                node.connect_nodes(connected_node, distance)
            else:
                raise ValueError(f"Node '{connected_node_number}. {connected_node_name}' is not defined.")


def parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict):
    nodes_dict = {}
    connections_data = {}

    # First pass: create nodes for each file's text
    for node_text in nodes_texts:
        file_path, content = node_text  # Unpack the tuple to get file path and content
        node, connection_data = parse_node(file_path, content, event_dict, encounter_dict, town_dict)
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
            nodes_texts.append((file_path, node_text))  # Append as a tuple (file_path, file_content)
    return parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict)

def generate_nodes_dict(tier: int, event_dict, encounter_dict, town_dict):
    """Generate nodes dictionary for the given tier"""
    nodes_directory = os.path.join(os.path.dirname(__file__),'..', f'vault/t{tier}/nodes')
    nodes_directory = os.path.normpath(nodes_directory)  # Normalize the path
    return parse_directory_nodes(nodes_directory, event_dict, encounter_dict, town_dict)