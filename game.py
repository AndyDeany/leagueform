from datetime import datetime


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


class InvalidGameError(ValueError):
    """Exception to be raised when data is missing from a set of game dicts to create a complete image of the game."""