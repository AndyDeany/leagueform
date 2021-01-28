import webbrowser

from html import generate_html_file
from data import Team


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
Team._100T = Team("100 Thieves", "Closer")
Team.C9 = Team("Cloud9", "Blaber")
Team.CLG = Team("CLG", "Broxah")
Team.DIGNITAS = Team("Dignitas", "Dardoch")
Team.EG = Team("Evil Geniuses", "Svenskeren")
Team.FLYQUEST = Team("FlyQuest", "Josedeodo")
Team.GG = Team("Golden Guardians", "Iconic")
Team.IMMORTALS = Team("Immortals", "Xerxe")
Team.TL = Team("Team Liquid", "Santorin")
Team.TSM = Team("TSM", "Spica")

# LCK
Team.AF = Team("Afreeca Freecs", "Dread")
Team.DRX = Team("DRX", "Pyosik")
Team.DWG = Team("Damwon (DWG KIA)", "Canyon")
Team.BRION = Team("Fredit BRION", "UmTi")
Team.GEN_G = Team("GenG", "Clid")
Team.HLE = Team("Hanwha Life Esports", "Arthur")
Team.KT = Team("KT Rolster", "Blank")
Team.LSB = Team("Liiv Sandbox", "Croco")
Team.NS = Team("NS Redforce", "Peanut")
Team.T1 = Team("T1", "Ellim")


HTML_FILE = "stats.html"

MATCHES = [
    # (Blue Team, Red Team),
    (Team.NS, Team.AF),
    (Team.AF, Team.NS),
    (Team.DWG, Team.HLE),
    (Team.HLE, Team.DWG),
    (Team.MAD_LIONS, Team.EXCEL),
    (Team.SCHALKE, Team.SK),
    (Team.G2, Team.ASTRALIS),
    (Team.MISFITS, Team.ROGUE),
    (Team.VITALITY, Team.FNATIC),
    (Team._100T, Team.C9),
    (Team.C9, Team._100T),
]

generate_html_file(HTML_FILE, MATCHES)
webbrowser.open_new_tab(HTML_FILE)
