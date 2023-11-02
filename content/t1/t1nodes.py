from ...classes.generators.node_creation import NodeBuilder
from ...classes.entities.player import Player
from .t1events import create_t1_events


def create_tier_1_nodes(player: Player):
    builder = NodeBuilder()
    events = create_t1_events(player)

    # Create nodes for Tier 1
    node1 = builder.create_node(
        1, "The Town of Loreva", events["loreva_town"], "You begin your journey towards Victoria Summit.")
    node3 = builder.create_node(
        3, "King's Road", events["kings_road"], "You begin your journey towards Victoria Summit.")

    # Link nodes
    builder.link_nodes(node1, node3, 1)

    return builder.return_nodes()
