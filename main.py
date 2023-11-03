from .classes.entities.player import Player
from .content.t1.t1nodes import create_tier_1_nodes
from .utils.playerchoice import handle_player_choice
from .classes.town.town import Town


def main():
    # Let's assume the player starts at node 1.
    player = Player(name='HERO', hp=40, mp=5, damage=2, defense=0)

    # Set up the game world.
    nodes = create_tier_1_nodes(player)
    current_node = nodes[0]

    # Main game loop.
    while player.is_alive():
        print(f"You are currently at {current_node.name}")

        if isinstance(current_node.event_or_encounter, Town):
            result = current_node.event_or_encounter.display_locations()
            if result == "exit_town":
                # Present travel options and let the player choose
                if current_node.connected_nodes:
                    current_node = handle_player_choice(
                        nodes, current_node, player)
                else:
                    print("There are no connected nodes from here. The journey ends.")
                    break

        # Check if current node event is completed and trigger if not
        while not current_node.event_or_encounter.completed:
            outcome = current_node.event_or_encounter.trigger()

            # Handle chained events
            while outcome.new_event:
                outcome = outcome.new_event.trigger()

            # Handle location changes
            if outcome.location_change:
                for node in nodes:
                    if node.name == outcome.location_change or node.number == outcome.location_change:
                        current_node = node
                        break

        # Check if player is still alive after the encounter
        if not player.is_alive():
            print("You have died!")
            exit()

        # Present travel options and let the player choose
        if current_node.connected_nodes:
            current_node = handle_player_choice(nodes, current_node, player)
        else:
            print("There are no connected nodes from here. The journey ends.")
            break

    # ... (rest of y


if __name__ == "__main__":
    main()
