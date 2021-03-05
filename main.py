import webbrowser

from htmlgen import generate_html_file
from data import process_data
from team import Team
from scraper import get_upcoming_matches
from aws import upload_file


# LEC
Team.ASTRALIS = Team("Astralis", "Zanzarah")
Team.EXCEL = Team("Excel", "Dan")
Team.SCHALKE = Team("Schalke 04", "Gilius")
Team.FNATIC = Team("Fnatic", "Selfmade")
Team.G2 = Team("G2 Esports", "Jankos")
Team.MAD_LIONS = Team("MAD Lions", "Elyoya")
Team.MISFITS = Team("Misfits Gaming", "Razork")
Team.ROGUE = Team("Rogue", "Inspired")
Team.SK = Team("SK Gaming", "TynX")
Team.VITALITY = Team("Team Vitality", "Skeanz")

# LCS
Team._100T = Team("100 Thieves", "Closer")
Team.C9 = Team("Cloud9", "Blaber")
Team.CLG = Team("Counter Logic Gaming", "Broxah")
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
Team.BRO = Team("Fredit BRION", "UmTi")
Team.GEN = Team("GenG", "Clid")
Team.HLE = Team("Hanwha Life Esports", "Arthur")
Team.KT = Team("KT Rolster", "GIDEON")
Team.LSB = Team("Liiv Sandbox", "OnFleek")
Team.NS = Team("NS Redforce", "Peanut")
Team.T1 = Team("T1", "Oner")

# LPL
Team.BLG = Team("Bilibili Gaming", "Meteor")
Team.EDG = Team("EDward Gaming", "jiejie")
Team.ES = Team("eStar", "H4cker")
Team.FPX = Team("FunPlus Phoenix", "Tian")
Team.INVICTUS = Team("Invictus Gaming", "XUN")
Team.JDG = Team("JD Gaming (pedo)", "Kanavi")
Team.LGD = Team("LGD Gaming", "Kui")
Team.LNG = Team("LNG Esports", "Tarzan")
Team.OMG = Team("Oh My God", "Aki")
Team.RA = Team("Rare Atom", "Leyan")
Team.RW = Team("Rogue Warriors", "Haro")
Team.RNG = Team("RNG", "Wei")
Team.SN = Team("Suning (pedo)", "SofM")
Team.WE = Team("Team WE", "beishang")
Team.TES = Team("Top Esports", "Karsa")
Team.TT = Team("TT Gaming", "Xiaopeng")
Team.V5 = Team("Victory Five", "Weiwei")

# LLA
Team.AK = Team("All Knights", "Grell")
Team.ESTRAL = Team("Estral Esports", "Mightybear")
Team.FURIOUS = Team("Furious", "Bugi")
Team.INFINITY = Team("Infinity eSports", "SolidSnake")
Team.ISURUS = Team("Isurus", "Tierwulf")
Team.KLG = Team("Kaos Latin Gamers", "QQMore")
Team.R7 = Team("Rainbow 7", "Xypherz")
Team.XTEN = Team("XTEN", "Unforgiven")

# TCL
Team.AURORA = Team("Team AURORA", "Kamil")
Team.SUPERM = Team("SuperMassive", "kireas")
Team.NASR = Team("NASR Turkey", "Kituruken")
Team.ISTANBUL = Team("Istanbul Wildcats", "Ferret")
Team.GALATASARAY = Team("Galatasaray Esports", "Mojito")
Team.GALAKTICOS = Team("Galakticos", "Tumay")
Team.DP = Team("Dark Passage", "Typhoon")
Team.BESIKTAS = Team("Besiktas Esports", "Robin")
Team.FIVER = Team("5 Ronin", "Skewer")
Team.FENER = Team("1907 Fenerbache", "Elramir")


HTML_FILE = "stats.html"

matches = [
    # (Blue Team, Red Team),
    (Team.HLE, Team.NS),
    (Team.GEN, Team.LSB),
    (Team.ES, Team.JDG),
    (Team.V5, Team.SN),
]

matches.extend(get_upcoming_matches("LCS", "LEC", hours=36))

matches.extend([
])

process_data()
generate_html_file(HTML_FILE, matches)
upload_file(HTML_FILE)
webbrowser.open_new_tab(HTML_FILE)
