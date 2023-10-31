from character import Character


class Player(Character):
    def __init__(self, name: str, hp: int, attack: int, defense: int, mp: int, experience: int = 0, level: int = 1):
        super().__init__(name, hp, attack, defense)
        self.mp = mp
        self.experience = experience
        self.level = level

    def gain_experience(self, amount: int):
        """Increases player's experience. Could also handle leveling up."""
        self.experience += amount
        # Logic for leveling up can be added here

    # Any other player-specific methods can be added
