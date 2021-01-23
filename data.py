import csv

from calc import show_implied_odds


class Player:

    all = []

    def __init__(self, name):
        self.name = name

        self.blue_games = 0
        self.blue_dragons = 0
        self.blue_heralds = 0
        self.blue_towers = 0

        self.red_games = 0
        self.red_dragons = 0
        self.red_heralds = 0
        self.red_towers = 0

        self.all.append(self)

    @classmethod
    def find(cls, name):
        for player in cls.all:
            if player.name == name:
                return player

    def __repr__(self):
        return f"{self.name}: Blue dragons {self.blue_dragons}/{self.blue_games}, Red dragons {self.red_dragons}/{self.red_games}, Blue heralds {self.blue_heralds}/{self.blue_games}, Red heralds {self.red_heralds}/{self.red_games}, Blue towers {self.blue_towers}/{self.blue_games}, Red towers {self.red_towers}/{self.red_games}."


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

        if None in (self.blue_jungler, self.red_jungler, self.first_dragon, self.first_herald, self.first_tower):
            type(self).amount_rejected += 1
            raise InvalidGameError("Couldn't find all required data, gameid=" + game_dict["gameid"])


with open("games2020.csv") as input_csv:
    games_csv = csv.reader(input_csv)

    lines = []
    lines = list(games_csv)
    first_line = lines.pop(0)

with open("games.csv") as input_csv:
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

    blue_player.blue_games += 1
    red_player.red_games += 1

    if game.first_dragon == game.SIDE_BLUE:
        blue_player.blue_dragons += 1
    elif game.first_dragon == game.SIDE_RED:
        red_player.red_dragons += 1
    else:
        games_missing_first_dragon += 1

    if game.first_herald == game.SIDE_BLUE:
        blue_player.blue_heralds += 1
    elif game.first_herald == game.SIDE_RED:
        red_player.red_heralds += 1
    else:
        games_missing_first_herald += 1

    if game.first_tower == game.SIDE_BLUE:
        blue_player.blue_towers += 1
    elif game.first_tower == game.SIDE_RED:
        red_player.red_towers += 1
    else:
        games_missing_first_tower += 1


print(f"{games_missing_first_dragon=}, {games_missing_first_herald=}, {games_missing_first_tower=}")
print(f"Games rejected: {Game.amount_rejected}/{Game.amount_rejected + len(games)}")
print("")


BLUE_JUNGLER = "UmTi"
RED_JUNGLER = "Peanut"

blue_jungler = Player.find(BLUE_JUNGLER)
red_jungler = Player.find(RED_JUNGLER)

show_implied_odds(blue_jungler.blue_dragons, blue_jungler.blue_games, red_jungler.red_dragons, red_jungler.red_games, "dragon")
show_implied_odds(blue_jungler.blue_heralds, blue_jungler.blue_games, red_jungler.red_heralds, red_jungler.red_games, "herald")
show_implied_odds(blue_jungler.blue_towers, blue_jungler.blue_games, red_jungler.red_towers, red_jungler.red_games, "tower")
