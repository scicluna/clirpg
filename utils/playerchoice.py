def handle_player_choice(nodes, current_node, player):
    print("\nWhere would you like to go next?")
    for index, (destination, travel_time) in enumerate(current_node.connected_nodes.items()):
        print(f"{index + 1}. {destination.name} (Travel time: {travel_time} days)")

    # Get player's choice
    while True:
        choice = input(f"Where to next?")
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(current_node.connected_nodes):
                # Update current_node based on player's choice
                chosen_node = list(current_node.connected_nodes.keys())[
                    choice_num - 1]

                # Record the travel time for the player
                travel_time = current_node.get_travel_time(chosen_node)
                player.total_days_passed += travel_time

                return chosen_node
            else:
                print("Invalid choice. Please choose a valid destination.")
        except ValueError:
            print("Invalid input. Please enter a number.")
