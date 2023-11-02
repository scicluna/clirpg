from ..locations.event import Event


class Town:
    def __init__(self, visit_locations: list["Location"]) -> None:
        self.visit_locations = visit_locations
        pass

    def display_locations(self):
        """Display all locations and handle user choice"""
        while True:
            for index, location in enumerate(self.visit_locations):
                print(f"{index+1}: {location['name']}")
            print(f"{len(self.visit_locations) + 1}: Exit Town")

            choice = input("Which location would you like to visit? ")

            try:
                choice_num = int(choice)

                if choice_num == len(self.visit_locations) + 1:
                    print("Leaving town...")
                    return "exit_town"

                if choice_num not in range(1, len(self.visit_locations) + 1):
                    print(
                        f"Invalid choice. Please choose between 1 and {len(self.visit_locations)}.")
                else:
                    self.visit_locations[choice_num - 1]["event"].trigger()

            except ValueError:
                # This block will execute if the conversion to int fails
                print("Invalid input. Please enter a number.")


class Location:
    def __init__(self, name: str, event: Event) -> None:
        self.name = name
        self.event = event
        pass
