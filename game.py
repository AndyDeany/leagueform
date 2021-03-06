from datetime import datetime


class Game:

    amount_rejected = 0
    amount_missing_junglers = 0
    amount_missing_first_dragon = 0
    amount_missing_first_herald = 0
    amount_missing_first_tower = 0
    amount_missing_first_blood = 0

    SIDE_BLUE = "Blue"
    SIDE_RED = "Red"

    ROLE_JUNGLE = "jng"

    def __init__(self, game_dicts):
        self.blue_jungler = None
        self.red_jungler = None

        self.first_dragon = None
        self.first_herald = None
        self.first_tower = None
        self.first_blood = None

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

            if game_dict["firstblood"] == "1":
                self.first_blood = game_dict["side"]

        self.date = datetime.strptime(game_dict["date"], "%Y-%m-%d %H:%M:%S")

        if None in (self.blue_jungler, self.red_jungler, self.first_dragon, self.first_herald, self.first_tower, self.first_blood):
            type(self).amount_rejected += 1

            if None in (self.blue_jungler, self.red_jungler):
                type(self).amount_missing_junglers += 1
            if self.first_dragon is None:
                type(self).amount_missing_first_dragon += 1
            if self.first_herald is None:
                type(self).amount_missing_first_herald += 1
            if self.first_tower is None:
                type(self).amount_missing_first_tower += 1
            if self.first_blood is None:
                type(self).amount_missing_first_blood += 1

            raise InvalidGameError("Couldn't find all required data, gameid=" + game_dict["gameid"])


class InvalidGameError(ValueError):
    """Exception to be raised when data is missing from a set of game dicts to create a complete image of the game."""
