import csv
from datetime import datetime

from oracles import ensure_csv_updated


class Team:
    def __init__(self, name, jungler):
        self.name = name
        self.jungler = jungler


class Player:

    all = []

    def __init__(self, name):
        self.name = name

        self.blue_games_dates = []
        self.blue_dragons_dates = []
        self.blue_heralds_dates = []
        self.blue_towers_dates = []

        self.red_games_dates = []
        self.red_dragons_dates = []
        self.red_heralds_dates = []
        self.red_towers_dates = []

        self.all.append(self)

    @classmethod
    def find(cls, name):
        for player in cls.all:
            if player.name.lower() == name.lower():
                return player

    def __repr__(self):
        return f"{self.name}: Blue dragons {self.blue_dragons}/{self.blue_games}, Red dragons {self.red_dragons}/{self.red_games}, Blue heralds {self.blue_heralds}/{self.blue_games}, Red heralds {self.red_heralds}/{self.red_games}, Blue towers {self.blue_towers}/{self.blue_games}, Red towers {self.red_towers}/{self.red_games}."

    @property
    def blue_games(self):
        return len(self.blue_games_dates)

    @property
    def blue_dragons(self):
        return len(self.blue_dragons_dates)

    @property
    def blue_heralds(self):
        return len(self.blue_heralds_dates)

    @property
    def blue_towers(self):
        return len(self.blue_towers_dates)

    @property
    def red_games(self):
        return len(self.red_games_dates)

    @property
    def red_dragons(self):
        return len(self.red_dragons_dates)

    @property
    def red_heralds(self):
        return len(self.red_heralds_dates)

    @property
    def red_towers(self):
        return len(self.red_towers_dates)

    def items_since(self, item, date):
        item_dates = getattr(self, f"{item}_dates")
        return len([item_date for item_date in item_dates if item_date > date])

    def blue_games_since(self, date):
        return self.items_since("blue_games", date)

    def blue_dragons_since(self, date):
        return self.items_since("blue_dragons", date)

    def blue_heralds_since(self, date):
        return self.items_since("blue_heralds", date)

    def blue_towers_since(self, date):
        return self.items_since("blue_towers", date)

    def red_games_since(self, date):
        return self.items_since("red_games", date)

    def red_dragons_since(self, date):
        return self.items_since("red_dragons", date)

    def red_heralds_since(self, date):
        return self.items_since("red_heralds", date)

    def red_towers_since(self, date):
        return self.items_since("red_towers", date)


class InvalidGameError(ValueError):
    """Exception to be raised when data is missing from a set of game dicts to create a complete image of the game."""


class Game:

    amount_rejected = 0

    SIDE_BLUE = "Blue"
    SIDE_RED = "Red"

    ROLE_JUNGLE = "jng"

    def __init__(self, game_dicts):
        self.blue_jungler = None
        self.red_jungler = None

        self.first_dragon = None
        self.first_herald = None
        self.first_tower = None

        for game_dict in game_dicts:
            if game_dict["position"] == self.ROLE_JUNGLE:
                if game_dict["side"] == self.SIDE_BLUE:
                    self.blue_jungler = game_dict["player"]
                elif game_dict["side"] == self.SIDE_RED:
                    self.red_jungler = game_dict["player"]

            if game_dict["firstdragon"] == "1":
                self.first_dragon = game_dict["side"]

            if game_dict["firstherald"] == "1":
                self.first_herald = game_dict["side"]

            if game_dict["firsttower"] == "1":
                self.first_tower = game_dict["side"]

        self.date = datetime.strptime(game_dict["date"], "%Y-%m-%d %H:%M:%S")

        if None in (self.blue_jungler, self.red_jungler, self.first_dragon, self.first_herald, self.first_tower):
            type(self).amount_rejected += 1
            raise InvalidGameError("Couldn't find all required data, gameid=" + game_dict["gameid"])


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
