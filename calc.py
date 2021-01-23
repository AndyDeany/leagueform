from statistics import stdev, mean

from scipy.stats import norm


def _create_data_set(first_heralds, total_matches):
    data = []
    data.extend((1 for _ in range(first_heralds)))
    data.extend((0 for _ in range(total_matches - first_heralds)))
    return data


def standard_deviation(data_set):
    if len(data_set) == 1:
        return 0
    return stdev(data_set)


def show_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games, objective_name):
    a_blue = _create_data_set(blue_team_wins, blue_team_games)
    b_red = _create_data_set(red_team_wins, red_team_games)

    combined_mean = mean(a_blue) - mean(b_red)
    combined_stdev = standard_deviation(a_blue) + standard_deviation(b_red)

    p_red_win = norm(combined_mean, combined_stdev**2).cdf(0)
    p_blue_win = 1 - p_red_win

    print(f"Blue team {objective_name}s: {blue_team_wins}/{blue_team_games}. ", end="")
    print(f"Red team {objective_name}s: {red_team_wins}/{red_team_games}.")

    print(f"P(Blue {objective_name}) = {round(p_blue_win, 3)} (implied odds: {round(1/p_blue_win, 2)}). ", end="")
    print(f"P(Red {objective_name}) = {round(p_red_win, 3)} (implied odds: {round(1/p_red_win, 2)}).")

    print("")
