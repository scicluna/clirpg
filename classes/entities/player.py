from character import Character


class Player(Character):
    def __init__(self, name: str, hp: int, attack: int, defense: int, mp: int, experience: int = 0, level: int = 1):
        super().__init__(name, hp, attack, defense)
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

    # Any other player-specific methods can be added
