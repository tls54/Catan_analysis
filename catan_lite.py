import pandas as pd
import random
from datetime import datetime as dt


#  Deal with 7s in first few rolls (custom map)
# rotations = n (set by num players) 
# if len(dataframe) < rotations * num players
#   if total is 7
#       dont record and re roll 

def player_roll():
    roll_1 = random.randint(1,6)
    roll_2 = random.randint(1,6)
    return roll_1, roll_2

robber_buffer = { # num_players : num_rotations
    2: 3,
    3: 2, 
    4: 2
}

def main():
    players = []
    game = True
    num_players = int(input(f'How many people are playing? \n'))
    game_data = pd.DataFrame(columns=['Player', 'Dice_1', 'Dice_2', 'Total_roll'])

    for i in range(num_players):
        player = input(f'What is the name of player_{i+1}? (Input in the roll order) \n')
        players.append(player)
    
    while game:
        for player in players:
            roll_1, roll_2 = player_roll()
            total = roll_1 + roll_2

            if len(game_data) < (robber_buffer[num_players] * num_players): # if 2 players then 6 rolls must have successfully happened
                # Check for a 7
                if total == 7:
                    print(f'{player} rolled {roll_1} and {roll_2} (Total: {total})')
                    print(f"We are in the 'no Robber' stage so this won't be logged and {player} will roll again!")
                    # re-roll until not a 7
                    while total == 7:
                        roll_1, roll_2 = player_roll()
                        total = roll_1 + roll_2


            game_data.loc[len(game_data)] = [player, roll_1, roll_2, total]
            print(f"{player} rolled {roll_1} and {roll_2} (Total: {total})")


            claim_win = input(f"{player}, do you want to claim this as a win? (y/n): ").strip().lower()
            if claim_win == 'y':
                game_data.to_csv(f'Games/Catan_game_{dt.now().date()}.csv', index=False)
                print(f"{player} has claimed the win! Game over.")
                game = False
                break  # exits the for-loop immediately — next while loop won't run because game=False
            
        
    
if __name__ == '_main__':
    main()
