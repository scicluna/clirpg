from ...classes.actions.item import Item, ItemType
from ...classes.entities.player import Player
from ...classes.locations.event import Choices, Choice, EventOutcome, Event
from ...classes.town.town import Town
from ...classes.entities.monster import Monster


def create_t1_events(player: Player):
    # Monsters
    monsters = {
        "bandit": Monster("bandit", hp=8, damage=2, defense=0, gold=2),
    }

    # Items
    items = {
        "knife": Item("knife", "A small knife", 1, ItemType.WEAPON, dmg=1),
        "shovel": Item("shovel", "A small shovel", 1, ItemType.SPECIAL),
        "leather_armor": Item("leather armor", "A set of leather armor", 1, ItemType.ARMOR, defense=1),
        "rope": Item("rope", "A long rope", 1, ItemType.SPECIAL),
        "lantern": Item("lantern", "A lantern", 1, ItemType.SPECIAL, special="light"),
        "longsword": Item("longsword", "A longsword", 1, ItemType.WEAPON, dmg=2)
    }

    # Event Outcomes
    outcomes = {
        "knife": EventOutcome("You have acquired a knife", items=[items["knife"]], stay_in_event=True),
        "gold": EventOutcome("You have obtained 2 gp", gold_change=2, stay_in_event=True),
        "shovel": EventOutcome("You have acquired a shovel", items=[items["shovel"]], stay_in_event=True),
        "leather armor": EventOutcome("You have bought leather armor!", items=[items["leather_armor"]], gold_change=-5, stay_in_event=True),
        "rope": EventOutcome("You have acquired a rope", items=[items["rope"]], gold_change=-2, stay_in_event=True),
        "lantern": EventOutcome("You have acquired a lantern", items=[items["lantern"]], gold_change=-4, stay_in_event=True),
        "longsword": EventOutcome("You have acquired a longsword", items=[items["longsword"]], gold_change=-8, stay_in_event=True),
        "barkeep1": EventOutcome("I get the barkeep's attention...", new_event="loreva_barkeep1"),
        "barkeep2": EventOutcome("He huffs and explains...", new_event="loreva_barkeep2"),
        "regulars1": EventOutcome("I ask around the bar...", new_event="loreva_regulars1"),
        "back_to_town": EventOutcome("You return back to town", new_event="loreva_town"),
        "back_to_tavern": EventOutcome("Back to the tavern", new_event="loreva_tavern"),
        "kings_road_engarde": EventOutcome(
            "I tread lightly, keeping my eyes open for any signs of danger.", monsters=[monsters["bandit"], monsters["bandit"], monsters["bandit"], monsters["bandit"]]),
        "kings_road_flee": EventOutcome("As you run, one knicks you with his dagger. you quickly flee back to Loreva.", health_change=-2, new_event="loreva_town")
        # ... continue with all outcomes
    }

    # Events
    my_house = Event(
        "I headed back to my house to grab a few extra supplies before my journey.",
        Choices([
            Choice("I grab my knife", outcomes["knife"]),
            Choice("I take my life's savings",
                   outcomes["gold"]),
            Choice("I pack my shovel", outcomes["shovel"]),
            Choice("Exit", outcomes["back_to_town"])
        ]), player)

    loreva_tavern = Event(
        "I take a seat at the tavern bar-side hoping to learn more about my journey to Victoria Summit.",
        Choices([
            Choice("I ask the barkeep",
                   outcomes["barkeep1"]),
            Choice("I ask the regulars",
                   outcomes["regulars1"]),
            Choice("Exit", outcomes["back_to_town"])
        ]), player)

    loreva_barkeep1 = Event("When I ask the barkeep he looks back at me with a deadpan stare. He asks 'maybe if you buy something i'll tell you'",
                            Choices([
                                Choice("I hand him a gold and ask again",
                                       outcomes["barkeep2"]),
                                Choice("I refuse and head on my way",
                                       outcomes["back_to_town"])
                            ]), player)

    loreva_barkeep2 = Event("All right kid, I'll tell you all I know. The King's Road is by far your most direct route towards Victoria Summit, but I wouldn't head that way If I were you. They say that bandits roam those roads these days. But on the other hand, you'll be able to stop at Terna City. Other than that, I don't know much. I know Wern's Woods is a bit dangerous this days, with all of the goblin sightings and all.",
                            Choices([
                                Choice("Wow, Thanks!",
                                       outcomes["back_to_tavern"])
                            ]), player)

    loreva_regulars1 = Event("I ask around the bar and one of the regulars imparts upon me something interesting... Apparently Roe's River crossing is a fairly safe route to take towards Victoria Summit. But you need to know the password -- for you see -- a troll lives under that bridge and taxes everyone who passes it. They can either pay 5 gold or tell him the words: 'fuck off'",
                             Choices([
                                 Choice("Wow, Thanks!",
                                        outcomes["back_to_tavern"])
                             ]), player)

    loreva_market = Event("I check out the marketplace before I leave, hoping to find some supplies to buy.",
                          Choices([
                              Choice("Leather Armor: 5gp", outcomes["leather armor"]
                                     ),
                              Choice("Rope: 2gp", outcomes["rope"]),
                              Choice("Lantern: 4gp", outcomes["lantern"]),
                              Choice("Longsword: 8gp", outcomes['longsword']),
                              Choice("Exit", outcomes["back_to_town"])
                          ]), player)

    kings_road = Event(
        "You find yourself surrounded on the king's road, four armed highwaymen pointing their swords at you. Their leader tells you: 'Drop your belongings and we'll spare your life.'",
        Choices([
            Choice("En Garde!", outcomes["kings_road_engarde"]),
            Choice("Run Away!!!", outcomes["kings_road_flee"])
        ]), player)

    events = {
        "loreva_town": Town(visit_locations=[
            {"name": "My House", "event": my_house},
            {"name": "The Tavern", "event": loreva_tavern},
            {"name": "The Market", "event": loreva_market}
        ]),
        "loreva_barkeep1": loreva_barkeep1,
        "loreva_barkeep2": loreva_barkeep2,
        "loreva_regulars1": loreva_regulars1,
        "kings_road": kings_road,
        # ... other individual events like market, barkeep1, barkeep2, etc.
    }

    return events
