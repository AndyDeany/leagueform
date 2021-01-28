from calc import get_implied_odds
from data import Player


def _print_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games, objective_name):
    p_blue_win, p_red_win = get_implied_odds(blue_team_wins, blue_team_games, red_team_wins, red_team_games)
    print(f"Blue team {objective_name}s: {blue_team_wins}/{blue_team_games}. ", end="")
    print(f"Red team {objective_name}s: {red_team_wins}/{red_team_games}.")
    print(f"P(Blue {objective_name}) = {round(p_blue_win, 3)} (implied odds: {round(1 / p_blue_win, 2)}). ", end="")
    print(f"P(Red {objective_name}) = {round(p_red_win, 3)} (implied odds: {round(1 / p_red_win, 2)}).")


def _generate_market_html(blue_team, red_team, blue_team_wins, blue_team_games, red_team_wins, red_team_games, market):
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


def _generate_match_html(blue_team, red_team):
    blue_jungler = Player.find(blue_team.jungler)
    red_jungler = Player.find(red_team.jungler)

    print(f"{blue_team.name} vs. {red_team.name}")
    _print_implied_odds(blue_jungler.blue_dragons, blue_jungler.blue_games, red_jungler.red_dragons, red_jungler.red_games, "dragon")
    _print_implied_odds(blue_jungler.blue_heralds, blue_jungler.blue_games, red_jungler.red_heralds, red_jungler.red_games, "herald")
    _print_implied_odds(blue_jungler.blue_towers, blue_jungler.blue_games, red_jungler.red_towers, red_jungler.red_games, "tower")
    print("")

    html = ""
    html += f"""<div class="match">\n<h1 style="color:#fff" align="center">{blue_team.name} vs. {red_team.name}</h1>"""
    html += _generate_market_html(blue_team, red_team, blue_jungler.blue_dragons, blue_jungler.blue_games, red_jungler.red_dragons, red_jungler.red_games, "dragon")
    html += _generate_market_html(blue_team, red_team, blue_jungler.blue_heralds, blue_jungler.blue_games, red_jungler.red_heralds, red_jungler.red_games, "herald")
    html += _generate_market_html(blue_team, red_team, blue_jungler.blue_towers, blue_jungler.blue_games, red_jungler.red_towers, red_jungler.red_games, "tower")
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
    for match in matches:
        html += _generate_match_html(match[0], match[1])
    html += "</div>\n</body>\n</html>"

    with open(file_name, "w") as file:
        file.write(html)
