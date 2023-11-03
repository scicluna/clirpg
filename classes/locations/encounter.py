from .gameelement import GameElement
from ..entities.player import Player
from ..entities.monster import Monster


class Encounter(GameElement):
    def __init__(self, name: str, monsters: list[Monster], player: Player, completed=False):
        self.name = name
        self.monsters = monsters
        self.player = player
        self.completed = completed

    def display_status(self):
        """Display status of player and monsters"""

        # Width of each block for status display
        block_width = 30

        # Display player status on left
        player_status = f"{self.player.name}\n{self.player.hp} / {self.player.maxhp}"
        if self.player.special_status:
            player_status += f"\n{self.player.special_status}"
        print(player_status.ljust(block_width), end="")

        # Display options block in the middle (can be blank or contain action options)
        options = "\n"  # Placeholder for future actions, e.g. "1: Attack, 2: Magic"
        print(options.center(block_width), end="")

        # Display monsters status on the right
        for monster in self.monsters:
            monster_status = f"{monster.name}\n{monster.hp} HP"
            print(monster_status.rjust(block_width), end="")
        print()  # Move to the next line after displaying all statuses

    def player_turn(self):
        """Handles player's turn"""
        self.player.open_attack_menu(self.monsters)

    def monsters_turn(self):
        """Handles the monsters' turn."""
        for monster in self.monsters:
            if monster.is_alive():
                monster.pick_attack(self.player)

    def is_encounter_resolved(self):
        """Check if the encounter is resolved (either player or all monsters are defeated)."""
        if not self.player.is_alive():
            return True
        for monster in self.monsters:
            if monster.is_alive():
                return False
        return True

    def trigger(self):
        """Start the encounter."""
        print("An encounter has started!")
        while not self.is_encounter_resolved():
            self.display_status()
            self.player_turn()
            if self.is_encounter_resolved():
                break
            self.monsters_turn()
        self.resolve()

    def resolve(self):
        # Determine the outcome of the encounter
        if self.player.is_alive():
            print("You are victorious!")
            self.completed = True
            for monster in self.monsters:
                self.player.add_items(monster.drop_all_loot())
                self.player.gold += monster.reward_gold()
                self.player.gain_experience(monster.reward_exp())
        else:
            print("You have been defeated.")
