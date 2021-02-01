import csv

from player import Player
from game import Game, InvalidGameError
from oracles import ensure_csv_updated


latest_csv = ensure_csv_updated()

with open(latest_csv) as input_csv:
    games_csv = csv.reader(input_csv)

    lines = []
    lines = list(games_csv)
    first_line = lines.pop(0)

with open("games2020.csv") as input_csv:
    games_csv = csv.reader(input_csv)
    lines.extend(list(games_csv)[1:])


line_dicts = []
for line in lines:
    line_dict = {}
    for i in range(len(first_line)):
        line_dict[first_line[i]] = line[i]
    line_dicts.append(line_dict)

line_dicts.sort(key=lambda d: d["gameid"])

# Creating Game objects - method #1
games = []
rejected_line_dicts = []


def add_game(game_dicts):
    try:
        games.append(Game(game))
    except InvalidGameError:
        rejected_line_dicts.extend(game_dicts)


game = [line_dicts.pop(0)]
for line_dict in line_dicts:
    if line_dict["gameid"] == game[-1]["gameid"]:
        game.append(line_dict)
    else:
        add_game(game)
        game = [line_dict]
add_game(game)

games.sort(key=lambda g: g.date)

games_missing_first_dragon = 0
games_missing_first_herald = 0
games_missing_first_tower = 0

for game in games:
    blue_player = Player.find(game.blue_jungler)
    if blue_player is None:
        blue_player = Player(game.blue_jungler)

    red_player = Player.find(game.red_jungler)
    if red_player is None:
        red_player = Player(game.red_jungler)

    blue_player.blue_games_dates.append(game.date)
    red_player.red_games_dates.append(game.date)

    if game.first_dragon == game.SIDE_BLUE:
        blue_player.blue_dragons_dates.append(game.date)
    elif game.first_dragon == game.SIDE_RED:
        red_player.red_dragons_dates.append(game.date)
    else:
        games_missing_first_dragon += 1

    if game.first_herald == game.SIDE_BLUE:
        blue_player.blue_heralds_dates.append(game.date)
    elif game.first_herald == game.SIDE_RED:
        red_player.red_heralds_dates.append(game.date)
    else:
        games_missing_first_herald += 1

    if game.first_tower == game.SIDE_BLUE:
        blue_player.blue_towers_dates.append(game.date)
    elif game.first_tower == game.SIDE_RED:
        red_player.red_towers_dates.append(game.date)
    else:
        games_missing_first_tower += 1


print("")
print(f"{games_missing_first_dragon=}, {games_missing_first_herald=}, {games_missing_first_tower=}")
print(f"Games rejected: {Game.amount_rejected}/{Game.amount_rejected + len(games)}")
print("")
