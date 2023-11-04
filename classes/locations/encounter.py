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
        """Display status of player and monsters, aligned with player's status sections."""
        player_name = f"{self.player.name.title()}"
        player_hp = f"hp: {self.player.hp}/{self.player.maxhp}"
        player_mp = f"mp: {self.player.mp}/{self.player.maxmp}"

        # Create a list of alive monsters
        monsters = [(monster.name.title(), f"{monster.hp}") for monster in self.monsters if monster.is_alive()]

        # Determine the maximum number of lines to print based on the player and monsters count
        max_lines = max(4, len(monsters))

        for i in range(max_lines):
            if i == 0:
                # Always print player's name and first monster if available
                monster_info = f"{monsters[i][0]} {monsters[i][1]}" if i < len(monsters) else ""
                print(f"{player_name}           {monster_info}")
            elif i == 1:
                # Print player's HP and second monster if available
                monster_info = f"{monsters[i][0]} {monsters[i][1]}" if i < len(monsters) else ""
                print(f"{player_hp}      {monster_info}")
            elif i == 2:
                # Print player's MP and third monster if available
                monster_info = f"{monsters[i][0]} {monsters[i][1]}" if i < len(monsters) else ""
                print(f"{player_mp}      {monster_info}")
            elif i == 3:
                # Fourth line for fourth monster if available
                monster_info = f"{monsters[i][0]} {monsters[i][1]}" if i < len(monsters) else ""
                print(f"              {monster_info}")
            elif i > 3:
                # Additional monsters if there are more than four
                print(f"              {monsters[i][0]} {monsters[i][1]}")


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
        print("An encounter has started!\n")
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
