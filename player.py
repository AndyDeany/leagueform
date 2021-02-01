class Player:

    all = []

    def __init__(self, name):
        self.name = name

        self.blue_games_dates = []
        self.blue_dragons_dates = []
        self.blue_heralds_dates = []
        self.blue_towers_dates = []
        self.blue_first_bloods_dates = []

        self.red_games_dates = []
        self.red_dragons_dates = []
        self.red_heralds_dates = []
        self.red_towers_dates = []
        self.red_first_bloods_dates = []

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
    def blue_first_bloods(self):
        return len(self.blue_first_bloods_dates)

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

    @property
    def red_first_bloods(self):
        return len(self.red_first_bloods_dates)

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

    def blue_first_bloods_since(self, date):
        return self.items_since("blue_first_bloods", date)

    def red_games_since(self, date):
        return self.items_since("red_games", date)

    def red_dragons_since(self, date):
        return self.items_since("red_dragons", date)

    def red_heralds_since(self, date):
        return self.items_since("red_heralds", date)

    def red_towers_since(self, date):
        return self.items_since("red_towers", date)

    def red_first_bloods_since(self, date):
        return self.items_since("red_first_bloods", date)
