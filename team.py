class Team:

    all = []

    def __init__(self, name, jungler):
        self.name = name
        self.jungler = jungler

        self.all.append(self)

    @classmethod
    def find(cls, name):
        for team in cls.all:
            if team.name.lower() == name.lower():
                return team
        raise ValueError(f"Couldn't find team '{name}'.")
