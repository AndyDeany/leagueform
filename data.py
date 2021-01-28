import csv
import webbrowser

from calc import get_implied_odds


class Team:
    def __init__(self, name, jungler):
        self.name = name
        self.jungler = jungler


# LEC
Team.ASTRALIS = Team("Astralis", "Zanzarah")
Team.EXCEL = Team("Excel", "Dan")
Team.SCHALKE = Team("Schalke 04", "Gilius")
Team.FNATIC = Team("Fnatic", "Selfmade")
Team.G2 = Team("G2", "Jankos")
Team.MAD_LIONS = Team("MAD Lions", "Elyoya")
Team.MISFITS = Team("Misfits Gaming", "Razork")
Team.ROGUE = Team("Rogue", "Inspired")
Team.SK = Team("SK", "TynX")
Team.VITALITY = Team("Team Vitality", "Skeanz")

# LCS
Team.EG = Team("Evil Geniuses", "Svenskeren")
Team.GG = Team("Golden Guardians", "Iconic")
Team.TL = Team("Team Liquid", "Santorin")
Team.TSM = Team("TSM", "Spica")
Team.FLYQUEST = Team("FlyQuest", "Josedeodo")

# LCK
Team.GEN_G = Team("GenG", "Clid")
Team.HLE = Team("Hanwha Life Esports", "Arthur")
Team.BRION = Team("Fredit BRION", "UmTi")
Team.DWG = Team("Damwon (DWG KIA)", "Canyon")
Team.DRX = Team("DRX", "Pyosik")
Team.KT = Team("KT Rolster", "Blank")
Team.T1 = Team("T1", "Ellim")
Team.LSB = Team("Liiv Sandbox", "Croco")


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
            if player.name.lower() == name.lower():
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


with open("games.csv") as input_csv:
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



def print_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games, objective_name):
    p_blue_win, p_red_win = get_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games)

    print(f"Blue team {objective_name}s: {blue_team_wins}/{blue_team_games}. ", end="")
    print(f"Red team {objective_name}s: {red_team_wins}/{red_team_games}.")

    print(f"P(Blue {objective_name}) = {round(p_blue_win, 3)} (implied odds: {round(1 / p_blue_win, 2)}). ", end="")
    print(f"P(Red {objective_name}) = {round(p_red_win, 3)} (implied odds: {round(1 / p_red_win, 2)}).")


def generate_market_html(blue_team, red_team, blue_team_wins, blue_team_games, red_team_wins, red_team_games, market):
    p_blue_win, p_red_win = get_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games)

    html = f"""
    <div class="market" align="center">
        <table>
            <tr>
                <th>{market.title()}s</th>
                <th>{blue_team.name}</th>
                <th>{red_team.name}</th>
            </tr>
            <tr>
                <td>Record</td>
                <td>{blue_team_wins}/{blue_team_games}</td>
                <td>{red_team_wins}/{red_team_games}</td>
            </tr>
            <tr>
                <td>Probability</td>
                <td>{round(p_blue_win, 3)}</td>
                <td>{round(p_red_win, 3)}</td>
            </tr>
            <tr>
                <td>Implied Odds</td>
                <td>{round(1 / p_blue_win, 2)}</td>
                <td>{round(1 / p_red_win, 2)}</td>
            </tr>
        </table>
    </div>
    """
    return html


def generate_match_html(blue_team, red_team):
    blue_jungler = Player.find(blue_team.jungler)
    red_jungler = Player.find(red_team.jungler)

    print_implied_odds(blue_jungler.blue_dragons, blue_jungler.blue_games, red_jungler.red_dragons, red_jungler.red_games, "dragon")
    print_implied_odds(blue_jungler.blue_heralds, blue_jungler.blue_games, red_jungler.red_heralds, red_jungler.red_games, "herald")
    print_implied_odds(blue_jungler.blue_towers, blue_jungler.blue_games, red_jungler.red_towers, red_jungler.red_games, "tower")

    html = ""
    html += f"""<div class="match">\n<h1 style="color:#fff" align="center">{blue_team.name} vs. {red_team.name}</h1>"""
    html += generate_market_html(blue_team, red_team, blue_jungler.blue_dragons, blue_jungler.blue_games, red_jungler.red_dragons, red_jungler.red_games, "dragon")
    html += generate_market_html(blue_team, red_team, blue_jungler.blue_heralds, blue_jungler.blue_games, red_jungler.red_heralds, red_jungler.red_games, "herald")
    html += generate_market_html(blue_team, red_team, blue_jungler.blue_towers, blue_jungler.blue_games, red_jungler.red_towers, red_jungler.red_games, "tower")
    html += "</div>"
    return html


def generate_html_file(file_name, matches):
    html = """
    <html>
        <head>
            <link rel="stylesheet" href="css/style.css">
            <link rel="stylesheet" href="less/style.less">
            <link rel="preconnect" href="https://fonts.gstatic.com">
            <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        </head>
        <body align="center">
        <div id="container" align="center">
    """
    for match in MATCHES:
        html += generate_match_html(match[0], match[1])
    html += "</div>\n</body>\n</html>"

    with open(file_name, "w") as file:
        file.write(html)


HTML_FILE = "stats.html"

MATCHES = [
    # (Blue Team, Red Team),
    (Team.DRX, Team.KT),
    (Team.KT, Team.DRX),
    (Team.T1, Team.LSB),
    (Team.LSB, Team.T1),
]

generate_html_file(HTML_FILE, MATCHES)
webbrowser.open_new_tab(HTML_FILE)

