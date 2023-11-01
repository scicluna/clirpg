from .classes.entities.player import Player
from .content.t1.t1nodes import create_tier_1_nodes


def main():
    # Let's assume the player starts at node 1.
    player = Player(name='HERO', hp=20, mp=5, damage=2, defense=0)

    # Set up the game world.
    nodes = create_tier_1_nodes(player)
    current_node = nodes[0]

    # Main game loop.
    while player.is_alive():
        print(f"You are currently at {current_node.name}")
        current_node.event_or_encounter.trigger()

        # Check if player is still alive after the encounter
        if not player.is_alive():
            break

        # Present travel options and let the player choose
        if current_node.connected_nodes:
            print("\nWhere would you like to go next?")
            for index, (destination, travel_time) in enumerate(current_node.connected_nodes.items()):
                print(
                    f"{index + 1}. {destination.name} (Travel time: {travel_time} days)")

            # Get player's choice
            while True:
                choice = input(
                    f"Where to next?")
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(current_node.connected_nodes):
                        # Update current_node based on player's choice
                        current_node = list(current_node.connected_nodes.keys())[
                            choice_num - 1]
                        break
                    else:
                        print("Invalid choice. Please choose a valid destination.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("There are no connected nodes from here. The journey ends.")
            break

    # ... (rest of y


if __name__ == "__main__":
    main()
