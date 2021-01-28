import webbrowser

from html import generate_html_file
from data import Team


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
