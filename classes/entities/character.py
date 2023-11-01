class Character:
    def __init__(self, name: str, hp: int, damage: int, defense: int, gold: int = 0, inventory: list = None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.gold = gold
        self.inventory = inventory if inventory else []
        self.special_status = None

    def take_damage(self, damage: int) -> int:
        """Reduces the character's hp by the given damage, after accounting for defense. Returns the net damage dealt."""
        net_damage = max(damage - self.defense, 0)
        self.hp -= net_damage
        print(f"{self.name} took {net_damage} damage!")
        return net_damage  # might be useful to know how much damage was actually dealt

    def generic_attack(current_character: "Character", target: "Character") -> int:
        """Performs a generic attack on a target. Returns the net damage dealt."""
        return target.take_damage(current_character.damage)

    def is_alive(self) -> bool:
        """Checks if the character is still alive."""
        return self.hp > 0

    def add_items(self, item: str):
        """Adds item to the character's inventory."""
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Removes an item from the character's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
