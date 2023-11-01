from ...classes.generators.node_creation import NodeBuilder
from ...classes.entities.player import Player
from .t1events import create_t1_events


def create_tier_1_nodes(player: Player):
    builder = NodeBuilder()
    events = create_t1_events(player)

    # Create nodes for Tier 1
    node1 = builder.create_node(
        1, "Starting Village", events["starting_town"], "Your journey begins here.")
    node2 = builder.create_node(
        2, "Haunted Woods", events["forest_encounter"], "Eerie woods filled with ghostly apparitions.")

    # Link nodes
    builder.link_nodes(node1, node2, 1)

    return builder.return_nodes()
