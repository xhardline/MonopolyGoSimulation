from constants import DESTINATION_PATH
from CardPacksSimulator import monte_carlo_sim

def __main__():
    results = monte_carlo_sim(num_players=1000)
    results.to_csv(DESTINATION_PATH)

__main__()
