from classes.entities.monster import Monster
from classes.entities.player import Player
from ...classes.locations.event import Event
from ...classes.locations.choices import Choices, Choice, EventOutcome


def create_t1_events(player: Player):
    events = {
        "starting_town": Event(
            "You're about to leave town! What do you bring with you?",
            Choices([
                Choice("My trusty shovel", EventOutcome(items=["shovel"])),
                Choice("I take my trusty dagger",
                       EventOutcome(items=["dagger"])),
                Choice("I take some gold coins", EventOutcome(gold_change=2))
            ]),
            player
        ),

        "forest_encounter": Event(
            "You come across a mysterious figure in the forest. What do you do?",
            Choices([
                Choice("Approach cautiously",
                       EventOutcome(
                           description="The figure hands you a strange herb", items=["magic herb"])),
                Choice("Draw your weapon", EventOutcome(
                    description="The figure attacks!", monsters=[Monster(name="Myserious Figure", hp=20, damage=2, defense=0, loot=["magic herb"], exp=5)])),
                Choice("Avoid the figure", EventOutcome(
                    description="You back away slowly..."))
            ]),
            player
        )
        # ... Add more events as needed
    }
    return events
