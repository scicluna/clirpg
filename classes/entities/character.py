class Character:
    def __init__(self, name: str, hp: int, attack: int, defense: int, gold: int = 0, inventory: list = None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = gold
        self.inventory = inventory if inventory else []

    def take_damage(self, damage: int):
        """Reduces the character's hp by the given damage, after accounting for defense."""
        net_damage = max(damage - self.defense, 0)
        self.hp -= net_damage
        return net_damage  # might be useful to know how much damage was actually dealt

    def is_alive(self) -> bool:
        """Checks if the character is still alive."""
        return self.hp > 0

    def add_to_inventory(self, item):
        """Adds an item to the character's inventory."""
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Removes an item from the character's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
