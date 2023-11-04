## Description:
A cozy inn where travelers share stories of their journeys.

## Choices:
Description: Share your own adventurous tale.
- Outcome: The crowd loves your story and you make new friends.
- stay_in_event = True

Description: Listen to the stories of ancient heroes.
- Outcome: You are inspired by the tales and feel motivated.
- stay_in_event = True

Description: Offer to buy a round of drinks.
- Outcome: You spend some gold, but the camaraderie is worth it.
- gold_change = -15
- stay_in_event = True 

Description: Retire early for a good night's sleep.
- Outcome: You rest well and recover from your travels.
- hp = +3
- location_change = "Elven Outpost"