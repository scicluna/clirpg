from ..entities.monster import Monster
from .encounter import Encounter
from ..entities.player import Player
from .event import Event


class EventOutcome:
    def __init__(self,
                 description: str,
                 health_change: int = 0,
                 gold_change: int = 0,
                 items: list[str] = None,
                 special_effect=None,
                 attacks: list[str] = None,
                 spells: list[str] = None,
                 monsters: list[Monster] = None,
                 incomplete: bool = False,
                 location_change: str = None,
                 new_event: Event = None):
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

    def apply(self, player: Player):
        """Apply the outcome to a player."""
        print(self.description)
        player.hp += self.health_change
        player.gold += self.gold_change
        player.special_status = self.special_effect
        for item in self.items:
            player.add_items(item)
        for attack in self.attacks:
            player.add_attack(attack)
        for spell in self.spells:
            player.add_magic(spell)

        if self.monsters:
            encounter = Encounter(self.monsters, player)
            encounter.trigger()

        return self


class Choice:
    def __init__(self, description: str, outcome: EventOutcome):
        self.description = description
        self.outcome = outcome


class Choices:
    def __init__(self, choices: list):
        self.choices = choices

    def display_choices(self):
        """Display all choices."""
        for index, choice in enumerate(self.choices):
            print(f"{index + 1}: {choice.description}")

    def choose(self, choice: int, player: Player):
        """Apply the outcome of a choice."""
        outcome = choice = self.choices[choice - 1].outcome.apply(player)
        return outcome
