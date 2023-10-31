from gameelement import GameElement


class Node:
    def __init__(self, number, name, event_or_encounter, travel_description):
        self.number = number
        self.name = name
        self.event_or_encounter = event_or_encounter
        self.connected_nodes = {}  # Dictionary to hold connected nodes and travel times
        self.travel_description = travel_description

    def connect_nodes(self, node, travel_time):
        """Connect another node to this one with a specified travel time."""
        if node not in self.connected_nodes:
            self.connected_nodes[node] = travel_time
            node.connected_nodes[self] = travel_time

    def get_travel_time(self, node):
        """Get the travel time to a specified node."""
        return self.connected_nodes.get(node, None)

    def display_travel_options(self):
        """Display connected nodes' names, numbers, and travel descriptions."""
        for node in self.connected_nodes:
            print(
                f"Node {node.number}: {node.name} - {node.travel_description} (Travel time: {node.travel_time} hours)")

    def set_game_element(self, game_element):
        """Set the game element for this node."""
        if isinstance(game_element, GameElement):
            self.game_element = game_element
        else:
            raise ValueError("Provided element is not a valid game element.")

    def __str__(self):
        return f"Node {self.number}: {self.name}"
