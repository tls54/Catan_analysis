import pandas as pd
import random
from datetime import datetime as dt
import matplotlib.pyplot as plt


def player_roll():
    roll_1 = random.randint(1, 6)
    roll_2 = random.randint(1, 6)
    return roll_1, roll_2


def simulate_rolls(num_players=4, total_rolls=10000, save_csv=True, plot=True):
    game_data = pd.DataFrame(columns=['Player', 'Dice_1', 'Dice_2', 'Total_roll'])

    players = [f'Player_{i+1}' for i in range(num_players)]

    for i in range(total_rolls):
        player = players[i % num_players]
        roll_1, roll_2 = player_roll()
        total = roll_1 + roll_2
        game_data.loc[len(game_data)] = [player, roll_1, roll_2, total]

    if save_csv:
        filename = f'Catan_benchmark_sim_{num_players}p_{total_rolls}_rolls_{dt.now().strftime("%Y%m%d")}.csv'
        game_data.to_csv(filename, index=False)
        print(f"Simulation complete. Results saved to '{filename}'.")

    if plot:
        game_data['Total_roll'].value_counts().sort_index().plot(
            kind='bar', title=f"Dice Roll Distribution ({total_rolls} Rolls, {num_players} Players)"
        )
        plt.xlabel("Dice Total")
        plt.ylabel("Frequency")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    return game_data


if __name__ == "__main__":
    simulate_rolls(num_players=2, total_rolls=1000, save_csv=True, plot=True)