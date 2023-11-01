from character import Character
from ..actions.attacks import attacks
from ..actions.magic import spells


class Player(Character):
    def __init__(self, name: str, hp: int, damage: int, defense: int, mp: int, experience: int = 0, level: int = 1):
        super().__init__(name, hp, damage, defense)
        self.mp = mp
        self.experience = experience
        self.level = level
        self.attacks = [{"name": "Attack", "action": self.generic_attack}]
        self.spells = []

    def gain_experience(self, amount: int):
        """Increases player's experience. Also handles leveling up."""
        self.experience += amount
        next_level = 10 + self.level*5

        if self.experience >= next_level:
            self.level += 1
            self.experience -= next_level
            print(f"Congratulations! You are now level {self.level}!")

    def open_attack_menu(self, target: Character):
        """Displays all attack options and executes the choice."""
        while True:
            for index, attack in enumerate(self.attacks):
                print(f"{index + 1}: {attack['name']}")

            choice = input("Choose an option: ")

            if choice in [str(i) for i in range(1, len(self.attacks) + 1)]:
                self.attacks[int(choice) - 1]["action"](target)
                break
            else:
                print("Invalid choice.")

    def add_attack(self, new_attack: str):
        """Adds an attack to player's attack menu"""
        if new_attack in attacks:
            function_def = attacks[new_attack]
            self.attacks.append({"name": new_attack, "action": function_def})
        else:
            raise ValueError(
                f"The attack '{new_attack}' does not exist in the attacks list!")

    def add_magic(self, new_spell: str):
        if new_spell in spells:
            function_def = spells[new_spell]
            self.spells.append({"name": new_spell, "action": function_def})
        else:
            raise ValueError(f"Spell '{new_spell}' does not exist!")

    # Any other player-specific methods can be added
