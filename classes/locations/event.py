from .gameelement import GameElement
from ..entities.player import Player
from ..entities.monster import Monster
from ..actions.item import Item
from ..locations.encounter import Encounter


class Event(GameElement):
    def __init__(self, name: str, description: str, choices: "Choices", player: Player):
        self.name = name
        self.description = description
        self.choices = choices
        self.player = player
        self.completed = False

    def trigger(self):
        # Present the event to the player
        print(self.description)
        return self.resolve_choice()

    def resolve_choice(self):
        """Resolves the player's choice."""
        while True:
            self.choices.display_choices()
            choice = input("Which choice do you make?")

            if choice == "inventory":
                self.player.display_inventory()
                continue
            if choice == "status":
                self.player.display_status()
                continue

            try:
                choice_num = int(choice)

                if choice_num not in range(1, len(self.choices.choices) + 1) or self.choices.choices[choice_num - 1].complete:
                    print(
                        f"Invalid choice.")
                else:
                    outcome = self.choices.choose(choice_num, self.player)
                    if not outcome.stay_in_event:
                        if not outcome.incomplete:
                            self.completed = True
                        return outcome

            except ValueError:
                # This block will execute if the conversion to int fails
                print("Invalid input. Please enter a number.")


class EventOutcome:
    def __init__(self,
                 description: str,
                 health_change: int = 0,
                 gold_change: int = 0,
                 items: list[Item] = None,
                 special_effect=None,
                 attacks: list[str] = None,
                 spells: list[str] = None,
                 monsters: list[Monster] = None,
                 incomplete: bool = False,
                 location_change: str = None,
                 new_event: Event = None,
                 stay_in_event: bool = False,
                 lose_item: Item = None):
        self.description = description
        self.health_change = health_change
        self.gold_change = gold_change
        self.items = items if items is not None else []
        self.special_effect = special_effect
        self.attacks = attacks if attacks is not None else []
        self.spells = spells if spells is not None else []
        self.monsters = monsters
        self.incomplete = incomplete
        self.location_change = location_change
        self.new_event = new_event
        self.stay_in_event = stay_in_event
        self.lose_item = lose_item

    def apply(self, player: Player):
        """Apply the outcome to a player."""
        print(self.description)
        player.hp += self.health_change
        player.gold += int(self.gold_change)
        player.special_status = self.special_effect
        for item in self.items:
            player.add_items(item)
        for attack in self.attacks:
            player.add_attack(attack)
        for spell in self.spells:
            player.add_magic(spell)

        if self.lose_item:
            player.remove_from_inventory(self.lose_item)

        if self.monsters:
            encounter = Encounter(self.monsters, player)
            encounter.trigger()

        return self

    def can_apply(self, player: Player) -> bool:
        """Check if this outcome can be applied to the player."""
        if int(self.gold_change) < 0 and player.gold < abs(self.gold_change):
            print("You don't have enough gold!")
            return False
        if self.lose_item and self.lose_item not in player.inventory:
            print("You don't have that item!")
            return False
        # Add other constraints here if needed
        return True


class Choice:
    def __init__(self, description: str, outcome: EventOutcome, complete: bool = False):
        self.description = description
        self.outcome = outcome
        self.complete = complete


class Choices:
    def __init__(self, choices: list[Choice]):
        self.choices = choices

    def all_complete(self) -> bool:
        """Checks if all choices are complete."""
        return all(choice.complete for choice in self.choices)

    def display_choices(self):
        """Display all choices that aren't marked as complete."""
        for index, choice in enumerate(self.choices):
            if not choice.complete:
                print(f"{index + 1}: {choice.description}")

    def choose(self, choice: int, player: Player):
        """Apply the outcome of a choice."""
        chosen = self.choices[choice - 1]

        if not chosen.outcome.can_apply(player):
            # Constraint not met, don't execute the outcome and inform the player
            chosen.outcome.stay_in_event = True
            return chosen.outcome

        # Otherwise, execute the outcome as usual
        outcome = chosen.outcome.apply(player)
        chosen.complete = True  # Mark choice as complete
        return outcome
