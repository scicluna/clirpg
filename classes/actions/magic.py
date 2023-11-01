from ..entities.character import Character


def open_magic_menu(current_character: Character, target: Character):
    """Displays all magic options and executes the choice."""
    while True:
        for index, spell in enumerate(current_character.spells):
            print(f"{index + 1}: {spell['name']}")

        choice = input("Choose an option: ")

        if choice in [str(i) for i in range(1, len(current_character.spells) + 1)]:
            current_character.spells[int(
                choice) - 1]["action"](current_character, target)
            break
        else:
            print("Invalid choice.")


def firebolt(caster: "Character", target: "Character") -> int:
    """Casts a firebolt spell on a target. Returns the damage dealt."""
    damage = 10  # Some formula for calculating firebolt damage
    return target.take_damage(damage)


def heal(caster: "Character", target: "Character") -> int:
    """Heals the target. Returns the amount healed."""
    healing = 5  # Some formula for calculating healing
    target.hp += healing
    return healing  # this could be useful if you want to print how much was healed


spells = {
    "Firebolt": firebolt,
    "Heal": heal,
}
