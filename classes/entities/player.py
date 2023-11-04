from .character import Character
from ..actions.attacks import attacks
from ..actions.magic import spells
from ..actions.item import Item


class Player(Character):
    def __init__(self, name: str, hp: int, damage: int, defense: int, mp: int, experience: int = 0, level: int = 1):
        super().__init__(name, hp, damage, defense)
        self.maxhp = hp
        self.mp = mp
        self.maxmp = mp
        self.experience = experience
        self.level = level
        self.attacks = [{"name": "Attack", "action": self.generic_attack}, {
            "name": "Items", "action": self.open_inventory_menu}]
        self.spells = []
        self.total_days_passed = 0
        self.equipped_weapon = None
        self.equipped_armor = None

    def display_status(self):
        """Displays player's status"""
        print(f"{self.name}\nHP: {self.hp}/{self.maxhp}\nMP: {self.mp}\nDamage: {self.damage}\nDefense: {self.defense}\nLevel: {self.level}\nExperience: {self.experience}/{10 + self.level*5}\nGold:{self.gold}\nDays passed: {self.total_days_passed}")

    def display_inventory(self):
        """Displays player's inventory"""
        print("Inventory:")
        for item in self.inventory:
            print(f"{item.quantity}x {item}")
        if len(self.inventory) == 0:
            print("Empty")

    def gain_experience(self, amount: int):
        """Increases player's experience. Also handles leveling up."""
        self.experience += amount
        next_level = 10 + self.level*5

        if self.experience >= next_level:
            self.level += 1
            self.experience -= next_level
            print(f"Congratulations! You are now level {self.level}!")

    def open_attack_menu(self, targets: list[Character]):
        """Displays all attack options and executes the choice."""
        while True:
            for index, attack in enumerate(self.attacks):
                print(f"{index + 1}: {attack['name']}")

            choice = input("Choose an option: ")

            target = None  # Initialize the target
            if choice == "1":  # handles generic attack and targeting
                alive_targets = [tgt for tgt in targets if tgt.is_alive()]

                if not alive_targets:
                    print("No valid targets!")
                    return

                if len(alive_targets) > 1:
                    for index, tgt in enumerate(alive_targets):
                        print(f"{index + 1}: {tgt.name.title()}")

                    while not target:  # Loop until a valid target is selected
                        target_choice = input("Choose your target: ")
                        if target_choice in [str(i) for i in range(1, len(alive_targets) + 1)]:
                            target = alive_targets[int(target_choice) - 1]
                        else:
                            print("Invalid target choice.")
                else:
                    target = alive_targets[0]

            if choice in [str(i) for i in range(1, len(self.attacks) + 1)]:
                # If the target hasn't been selected (not a generic attack)
                if not target:
                    # Default to the first target for simplicity
                    target = targets[0]
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
        """Adds a new spell to a player's spell menu"""
        if new_spell in spells:
            function_def = spells[new_spell]
            self.spells.append({"name": new_spell, "action": function_def})
        else:
            raise ValueError(f"Spell '{new_spell}' does not exist!")

    def open_inventory_menu(self, targets: list[Character]):
        """View player inventory and executes the choice"""

        # Filter out items with 0 quantity
        valid_items = [item for item in self.inventory if item.quantity > 0]

        while True:
            print("Inventory:")
            for index, item in enumerate(valid_items):
                print(f"{index + 1}: {item}")
            print(f"{len(valid_items)+1}: Exit")

            choice = input("Choose an item: ")

            if choice == str(len(valid_items) + 1):
                break

            if choice in [str(i) for i in range(1, len(valid_items) + 1)]:
                self.use_item(valid_items[int(choice) - 1])
                break
            else:
                print("Invalid choice.")

    def equip_weapon(self, weapon: Item):
        """Equips weapon and updates damage stat"""
        # Unequip the current weapon if there's one
        if self.equipped_weapon:
            self.unequip_weapon()

        # Increase player's damage by the weapon's damage
        self.damage += weapon.dmg
        self.equipped_weapon = weapon
        print(f"Equipped {weapon.name}!")

    def unequip_weapon(self):
        """Unequip weapon and deducts damage stat"""
        # Decrease player's damage by the weapon's damage
        self.damage -= self.equipped_weapon.dmg
        print(f"Unequipped {self.equipped_weapon.name}!")
        self.equipped_weapon = None

    def equip_armor(self, armor: Item):
        """Equip armor and update defense stat"""
        # Unequip the current armor if there's one
        if self.equipped_armor:
            self.unequip_armor()

        # Increase player's defense by the armor's defense
        self.defense += armor.defense
        self.equipped_armor = armor
        print(f"Equipped {armor.name}!")

    def unequip_armor(self):
        """"Unequips armor and deducts defense stat"""
        # Decrease player's defense by the armor's defense
        self.defense -= self.equipped_armor.defense
        print(f"Unequipped {self.equipped_armor.name}!")
        self.equipped_armor = None
