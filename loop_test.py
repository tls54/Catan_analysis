import random 


def player_roll():
    roll_1 = random.randint(1,6)
    roll_2 = random.randint(1,6)
    return roll_1, roll_2

total = 7
while total == 7:
    roll_1, roll_2 = player_roll()
    total = roll_1 + roll_2
