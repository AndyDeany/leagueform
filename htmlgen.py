from datetime import datetime

from calc import get_implied_odds
from player import Player
from team import Team
from scraper import Match


def _generate_market_html(blue_team, red_team, market):
    blue_jungler = Player.find(blue_team.jungler, error=True)
    red_jungler = Player.find(red_team.jungler, error=True)

    blue_team_wins = getattr(blue_jungler, f"blue_{market}s")
    red_team_wins = getattr(red_jungler, f"red_{market}s")
    blue_team_games = blue_jungler.blue_games
    red_team_games = red_jungler.red_games

    date = datetime(2021, 1, 1, 0, 0, 0)
    blue_team_2021_wins = blue_jungler.items_since(f"blue_{market}s", date)
    red_team_2021_wins = red_jungler.items_since(f"red_{market}s", date)
    blue_team_2021_games = blue_jungler.blue_games_since(date)
    red_team_2021_games = red_jungler.red_games_since(date)

    p_blue_win, p_red_win = get_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games)

    # print(f"Blue team {market}s: {blue_team_wins}/{blue_team_games}. ", end="")
    # print(f"Red team {market}s: {red_team_wins}/{red_team_games}.")
    # print(f"P(Blue {market}) = {round(p_blue_win, 3)} (implied odds: {round(1 / p_blue_win, 2)}). ", end="")
    # print(f"P(Red {market}) = {round(p_red_win, 3)} (implied odds: {round(1 / p_red_win, 2)}).")

    html = f"""
    <div class="market" align="center">
        <table>
            <tr>
                <th>{market.replace("_", " ").title()}s</th>
                <th>{blue_team.name}</th>
                <th>{red_team.name}</th>
            </tr>
            <tr>
                <td>Record (2021)</td>
                <td>{blue_team_wins}/{blue_team_games} ({blue_team_2021_wins}/{blue_team_2021_games})</td>
                <td>{red_team_wins}/{red_team_games} ({red_team_2021_wins}/{red_team_2021_games})</td>
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


def _generate_match_html(blue_team, red_team):
    # print(f"\n{blue_team.name} vs. {red_team.name}")
    html = ""
    html += f"""<div class="match">\n<h1 style="color:#fff" align="center"><span style="color:#1cb3ff">{blue_team.name}</span> vs. <span style="color:#de4040">{red_team.name}</span></h1>"""
    html += _generate_market_html(blue_team, red_team, "dragon")
    html += _generate_market_html(blue_team, red_team, "herald")
    html += _generate_market_html(blue_team, red_team, "tower")
    html += _generate_market_html(blue_team, red_team, "first_blood")
    html += "</div>"
    return html


def generate_html_file(file_name, matches):
    html = """<html>
        <head>
            <link rel="stylesheet" href="css/style.css">
            <link rel="stylesheet" href="less/style.less">
            <link rel="preconnect" href="https://fonts.gstatic.com">
            <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
            <link rel="shortcut icon" type="image/png" href="images/favicon.png">
        </head>
        <body align="center">
        <div id="container" align="center">
    """
    for match in matches:
        if isinstance(match, Match):
            match = (Team.find(match.team1_fullname), Team.find(match.team2_fullname))
        html += _generate_match_html(match[0], match[1])
    html += "</div>\n</body>\n</html>"

    with open(file_name, "w") as file:
        file.write(html)
