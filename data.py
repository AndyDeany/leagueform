import csv

from player import Player
from game import Game, InvalidGameError
from oracles import update_and_get_latest_csv


def _get_lines_from_csvs(*csvs):
    with open(csvs[0]) as input_csv:
        lines = list(csv.reader(input_csv))
        first_line = lines.pop(0)

    for csv_name in csvs[1:]:
        with open(csv_name) as input_csv:
            lines.extend(list(csv.reader(input_csv))[1:])   # Ignore first line - metadata that we've stored already

    return first_line, lines


def _get_line_dicts(first_line, lines):
    line_dicts = []
    for line in lines:
        line_dict = {}
        for i in range(len(first_line)):
            line_dict[first_line[i]] = line[i]
        line_dicts.append(line_dict)

    line_dicts.sort(key=lambda d: d["gameid"])

    return line_dicts


def _get_game_objects(line_dicts):
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

    return games, rejected_line_dicts


def _add_games_data_to_players(games):
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
            raise ValueError(f"Invalid side for first dragon: {game.first_dragon}.")

        if game.first_herald == game.SIDE_BLUE:
            blue_player.blue_heralds_dates.append(game.date)
        elif game.first_herald == game.SIDE_RED:
            red_player.red_heralds_dates.append(game.date)
        else:
            raise ValueError(f"Invalid side for first herald: {game.first_herald}.")

        if game.first_tower == game.SIDE_BLUE:
            blue_player.blue_towers_dates.append(game.date)
        elif game.first_tower == game.SIDE_RED:
            red_player.red_towers_dates.append(game.date)
        else:
            raise ValueError(f"Invalid side for first tower: {game.first_tower}.")

    print("")
    print(f"Games rejected: {Game.amount_rejected}/{Game.amount_rejected + len(games)}")
    print(f"{Game.amount_missing_junglers=}")
    print(f"{Game.amount_missing_first_dragon=}")
    print(f"{Game.amount_missing_first_herald=}")
    print(f"{Game.amount_missing_first_tower=}")
    print("")


def process_data():
    latest_csv = update_and_get_latest_csv()
    first_line, lines = _get_lines_from_csvs(latest_csv, "games2020.csv")
    line_dicts = _get_line_dicts(first_line, lines)
    games, rejected_line_dicts = _get_game_objects(line_dicts)
    _add_games_data_to_players(games)
