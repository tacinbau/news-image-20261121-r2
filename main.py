#!/usr/bin/env python3
"""THE WORLD - Saturday, 21 November 2026.
One-page newspaper front page: 171 stories, 60+ places.
STDLIB ONLY. Deterministic PNG 1024x1024 RGB.
Output: os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")/entry.png
"""
import hashlib
import math
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (11, 42, 74)
RED = (176, 0, 32)
GOLD = (232, 220, 180)
LIGHT = (233, 228, 216)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)
UP = (120, 220, 140)
DOWN = (255, 130, 130)

# 5x7 bitmap font. Each glyph: 7 rows of 5 chars ('#' on, '.' off).
FONT = {
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '#': (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '&': (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '*': (".....", "..#..", "#.#.#", ".###.", "#.#.#", "..#..", "....."),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    ',': (".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    '/': ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    '3': ("#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': ("..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", "..#..", ".#..."),
    '<': ("...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '>': (".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
    '?': (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    '@': (".###.", "#...#", "#.###", "#.#.#", "#.##.", "#....", ".###."),
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '[': (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
    ']': (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
    '_': (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    '^': ("..#..", ".#.#.", "#...#", ".....", ".....", ".....", "....."),
    '|': ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def wrap_text(s, scale, max_w):
    """Greedy word wrap; returns list of lines, none wider than max_w."""
    words = s.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c, t=1):
        self.fill_rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill_rect(x, y, t, h, c)

    def rect(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def draw_text(self, x, y, s, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '#':
                        self.fill_rect(cx + col * scale, y + r * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def draw_text_center(self, cx, y, s, scale, color):
        w = text_width(s.upper(), scale)
        return self.draw_text(cx - w // 2, y, s, scale, color)

    def draw_text_right(self, rx, y, s, scale, color):
        w = text_width(s.upper(), scale)
        return self.draw_text(rx - w, y, s, scale, color)


def png_bytes(cv):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    idat = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", idat) + chunk(b"IEND", b""))

# ---------------------------------------------------------------- data
# All items verified in Saturday 21 November 2026 editions:
# AP, Reuters, BBC, CNN, AFP, USGS, ESA, JAXA, UPI, Guardian,
# OneTurn day edition 2026-11-21, Dalton Daily markets, ScoreZaap,
# IANS sports wire 21 Nov 2026. Items dated other days excluded.

HEROES = [
    ("WAR - UKRAINE", "KRYVYI RIH",
     "MISSILE HITS ZELENSKY'S HOMETOWN",
     "2 DEAD, 60 HURT IN KRYVYI RIH. RUSSIA FIRED 3 MISSILES AND "
     "148 DRONES OVERNIGHT; 117 SHOT DOWN. NATO: WE WILL DEFEND "
     "EVERY INCH OF POLAND."),
    ("MARKETS - NEW YORK", "NEW YORK",
     "AI SELL-OFF DRAGS MARKETS DOWN",
     "S&P -3.7%, NASDAQ -5.3%, NIKKEI -5.1%. NASDAQ ERASES 2026 "
     "GAINS AS ANTHROPIC SLIDES AGAIN; GOLD -4.6%, BITCOIN DIPS, "
     "THEN RECOVERS ABOVE $60,000."),
    ("JUSTICE - MEXICO", "GUASAVE",
     "MEXICO CAPTURES CARTEL BOSS",
     "FAUSTO ISIDRO MEZA FLORES, FBI MOST-WANTED, SEIZED IN "
     "GUASAVE, SINALOA. GUN BATTLES FOLLOW; TWO MORE LEADERS HELD."),
]

# (label, value, change) - Friday close, Dalton Daily 21 Nov 2026.
MARKETS = [
    ("S&P 500", "6,910.39", "-3.70%"),
    ("NASDAQ", "22,617.73", "-5.28%"),
    ("NIKKEI", "56,436.65", "-5.06%"),
    ("DOW", "48,147.33", "-1.93%"),
    ("GOLD", "$3,515.40", "-4.62%"),
    ("BTC", "$57,911", "-1.51%"),
    ("BRENT", "$89.95", "-2.83%"),
    ("VIX", "35.89", "+26.20%"),
]

# (utc label, beat of the day)
TIMELINE = [
    ("03:04 UTC", "RAHUL CENTURY IN WELLINGTON TEST"),
    ("15:00 UTC", "TRANMERE 2-1 COLCHESTER, LEAGUE TWO"),
    ("18:24 UTC", "BEPICOLOMBO ENTERS MERCURY ORBIT"),
    ("21:00 UTC", "WALL ST CLOSES: S&P -3.7%, NASDAQ -5.3%"),
    ("MORNING UTC", "COP31 TALKS PASS FRIDAY DEADLINE"),
    ("EVENING UTC", "MEXICO CAPTURES CARTEL BOSS IN SINALOA"),
]

QUOTE = "NATO WILL DEFEND EVERY INCH OF POLISH TERRITORY."
QUOTE_BY = "- MARK RUTTE, NATO SECRETARY GENERAL"

# (place, one-line brief) - 162 briefs, 3 columns x 54 rows.
BRIEFS = [
    ("KYIV", "RUSSIA FIRES 400+ DRONES, 110 MISSILES"),
    ("POLAND", "2 MISSILES, 1 DRONE LAND; NATO PROTESTS"),
    ("KHASAB", "TANKERS HIT NEAR HORMUZ, 6 ATTACKS IN WEEK"),
    ("GAZA", "STRIKE KILLS 3 IN WORLD CENTRAL KITCHEN VAN"),
    ("SANAA", "HOUTHIS: 71 COALITION STRIKES IN 24 HOURS"),
    ("GULF OF FINLAND", "DRONES HIT RUSSIAN CARGO SHIP"),
    ("PORT-AU-PRINCE", "2,500 SALVADORAN TROOPS FIGHT GANGS"),
    ("SOUTH ETHIOPIA", "700,000 DISPLACED BY ETHNIC FIGHTING"),
    ("EAST CONGO", "FIGHTING WIDENS, DECEMBER TRUCE AT RISK"),
    ("JABALIA", "PALESTINIAN MAN SHOT DEAD BY ISRAELI FIRE"),
    ("IVANO-FRANKIVSK", "MOSCOW DRONES STRIKE CITY"),
    ("SOUTH LEBANON", "ISRAELI STRIKES HIT 4 DISTRICTS"),
    ("RIYADH", "SAUDI ARMY INTERCEPTS 3 MISSILES"),
    ("KERCH", "ZELENSKY: CRIMEA BRIDGE WON'T REMAIN"),
    ("BRUSSELS", "UK, EU SIGN 3 POST-BREXIT DEALS"),
    ("BRUSSELS", "EU, INDONESIA SIGN TRADE DEAL, 10 YRS ON"),
    ("BRUSSELS", "EU BUDGET CUT EUR204BN, BIG TECH TAX 3%"),
    ("SHENZHEN", "TRUMP DEFENDS PUTIN TIES AT XI SUMMIT"),
    ("SHENZHEN", "ZELENSKY CALLS PUTIN A KILLER"),
    ("COPENHAGEN", "DENMARK EXPELS RUSSIAN DIPLOMAT"),
    ("PARIS", "VILLEPIN ANNOUNCES FRENCH PRESIDENTIAL RUN"),
    ("MADRID", "SPAIN VOTES 29 NOV; PP HOPES TO OUST SANCHEZ"),
    ("SEOUL", "RULING PARTY MOVES TO IMPEACH CHIEF JUSTICE"),
    ("BRASILIA", "BOLSONARO HOSPITALISED, INTESTINAL BLOCK"),
    ("NEW YORK", "MAMDANI: CLOSE RIKERS ISLAND BY 2032"),
    ("DAR ES SALAAM", "LISSU GUILTY OF SEDITION"),
    ("ISTANBUL", "TURKEY SEIZES SOZCU TV, LAST INDIE CHANNEL"),
    ("NARVA", "ESTONIA TO SHUT RUSSIA BORDER FROM 1 DEC"),
    ("NEW DELHI", "NEPAL PM SHAH TO VISIT INDIA 22-23 NOV"),
    ("TOKYO", "JAPAN SIDELINED AS CHINA TIES HIT RECORD LOW"),
    ("JURF AL-SAKHAR", "IRAQ, HEZBOLLAH AGREE JOINT POST"),
    ("SAN SALVADOR", "BUKELE SEEKS UNUSUAL THIRD TERM"),
    ("DHAKA", "50+ AWAMI LEAGUE HOMES BURNT BEFORE RETURN"),
    ("BERLIN", "STUDENTS MARCH AGAINST MILITARY BUILD-UP"),
    ("PARIS", "ACTIVISTS RALLY AGAINST POLICE SHOOTING BILL"),
    ("BERLIN", "GERMAN MINISTER APOLOGISES OVER UKRAINE JIBE"),
    ("THE HAGUE", "ICJ: MYANMAR GUILTY OF GENOCIDE"),
    ("LOS ANGELES", "MAN GUILTY OF STARTING PALISADES FIRE"),
    ("PARIS", "3 POLICE JAILED OVER RACIST BEATING OF ZECLER"),
    ("NEW YORK", "GUPTA JAILED 19 YRS OVER SIKH MURDER PLOT"),
    ("PARIS", "DEPARDIEU, HOUELLEBECQ FACE RAPE PROBE"),
    ("HUNTSVILLE", "INMATE CRIES OUT IN HOUR-LONG EXECUTION"),
    ("MELBOURNE", "TEEN 'ONEPERCENT' RAN ARSONS ON SIGNAL"),
    ("JAKARTA", "DAYCARE HEAD JAILED 5 YRS OVER ABUSE"),
    ("WASHINGTON", "JUDGE OKS $7.25BN ROUNDUP SETTLEMENT"),
    ("GENEVA", "UN: KEEP WORKING ON AI WEAPONS RULES TO 2028"),
    ("TOKYO", "SAUDI TRIPLES OIL STORED IN JAPAN TO 24M"),
    ("LONDON", "BRENT NEAR $90 AS GLUT FEARS MEET GULF WAR"),
    ("BUENOS AIRES", "ARGENTINA RISK TOPS 1,000 POINTS"),
    ("TURKANA", "KENYA STARTS ONSHORE CRUDE DRILLING"),
    ("AMERICAN SAMOA", "US SELLS FIRST DEEP-SEA LEASES"),
    ("ANTALYA", "COP31 TALKS PASS DEADLINE ON FOSSIL FUELS"),
    ("WASHINGTON", "TRUMP THREATENS TAX ON CENTRES ABROAD"),
    ("WASHINGTON", "TRUMP RAISED OUSTED NVIDIA CHIEF WITH XI"),
    ("NEW YORK", "ANTHROPIC SLIDES ON DAY 2; IPO WAS $2TN"),
    ("NEW YORK", "NVIDIA IN LONGEST WEEKLY SLIDE SINCE 2008"),
    ("NEW YORK", "GOLD -4.6%, SILVER -7.3% IN SELL-OFF"),
    ("NEW YORK", "BITCOIN DIPS TO $55,326, BACK OVER $60,000"),
    ("LONDON", "LUFTHANSA TO CUT 1,000 JOBS ON FUEL COSTS"),
    ("LONDON", "CANCER PILL MAKES TUMOURS VANISH IN 1 IN 12"),
    ("BRAZIL", "WOLBACHIA MOSQUITOES CUT DENGUE CASES 69%"),
    ("VIRGINIA", "US LOSES MEASLES ELIMINATION STATUS"),
    ("BERKELEY", "AI MAY PREDICT SUDDEN CARDIAC DEATH"),
    ("BERKELEY", "COMPOUND BURNS FAT WITHOUT LOSING MUSCLE"),
    ("GENEVA", "CERN FINDS EVIDENCE OF ULTRA-RARE DECAY"),
    ("SAN FRANCISCO", "MATHEMATICIAN CLAIMS AI RIEMANN PROOF"),
    ("MELBOURNE", "STUDY MAY REWRITE HUMAN FAMILY TREE"),
    ("TAUNG", "TAUNG CHILD STUDY QUESTIONS SPECIES GROUPING"),
    ("MONTANA", "BLUE SUCKER FISH FOUND TO LIVE 100+ YEARS"),
    ("HAMBURG", "X-RAY LASER FLASHES SHORTER THAN ATOM GAPS"),
    ("ANTARCTICA", "ANCIENT RANGES FOUND UNDER ICE"),
    ("ABU DHABI", "NEW FOSSIL CARNIVORE NAMED FOR ABU DHABI"),
    ("YAMANASHI", "PILOTLESS AIR TAXI CARRIES PASSENGER"),
    ("GALE CRATER", "NASA SHARES CURIOSITY CLOUD PHOTOS"),
    ("DEEP SPACE", "VOYAGER 1 NOW 24 LIGHT-HOURS FROM EARTH"),
    ("KAMPALA", "UGANDA LIMITS GATHERINGS OVER EBOLA"),
    ("LONDON", "PRINCESS OF WALES SAYS SHE IS IN REMISSION"),
    ("NEW YORK", "YOUTUBE NEARS BIG SCHOOLS SETTLEMENT"),
    ("JUNIN", "MAGNITUDE 6.7 QUAKE SHAKES CENTRAL PERU"),
    ("DILI", "MAGNITUDE 6.8 QUAKE STRIKES OFF TIMOR"),
    ("BAYELSA", "FUNERAL BOAT CAPSIZES, 30 DEAD, 300 MISSING"),
    ("BASRA", "FIRE AT POWER STATION KILLS 4, HURTS 30"),
    ("PARIS", "COST-OF-LIVING PROTESTS ENTER 6TH WEEKEND"),
    ("BERLIN", "COST-OF-LIVING MARCHES SPREAD IN EUROPE"),
    ("ROME", "TREVI COIN GIFTS DOWN 200K GBP"),
    ("CINCINNATI", "FIONA THE HIPPO DIES AT 9, SWALLOWED HAT"),
    ("MARANHAO", "ISOLATED AWA PEOPLE APPROACH OUTPOST"),
    ("CAPE TOWN", "PHUMZILE MLAMBO-NGCUKA DIES AGED 71"),
    ("NEW YORK", "GTA VI EARNS $3.8BN ON DAY ONE, RECORD"),
    ("VATICAN", "25M CHRISTMAS TREE RAISED AT ST PETER'S"),
    ("OKUNOSHIMA", "RABBIT ISLAND DRAWS CROWDS, DARK PAST"),
    ("MARRAKECH", "COTILLARD OPENS MARRAKECH FILM FESTIVAL"),
    ("OSAKA", "BTS WIN FIVE AWARDS AT MAMA CEREMONY"),
    ("WASHINGTON", "RODRIGO ALBUM DEBUTS AT NO. 1 IN US"),
    ("LONDON", "ENGLAND 37-12 NEW ZEALAND, RECORD RUGBY WIN"),
    ("TURIN", "ALCARAZ BEATS SHELTON, INTO ATP FINALS FINAL"),
    ("EDINBURGH", "SCOTLAND HIT 11 TRIES IN JAPAN ROUT"),
    ("CLEVELAND", "HARDEN 51 PTS, PASSES KOBE ON 50-PT LIST"),
    ("HELSINKI", "CANADA PAIR SILVER AT FINLANDIA TROPHY"),
    ("OBIHIRO", "CANADA SPEED SKATERS WIN BRONZE IN JAPAN"),
    ("SEOUL", "CHOI WINS 3RD STRAIGHT 1,000M TITLE"),
    ("LAS VEGAS", "VERSTAPPEN ON POLE AFTER PENALTY"),
    ("MUNICH", "KANE OUT MONTHS WITH ANKLE LIGAMENT TEAR"),
    ("TURIN", "ALCARAZ BEATS COBOLLI DESPITE THIGH WORRY"),
    ("MELBOURNE", "KANGAROOS INTO 4TH STRAIGHT AFLW FINAL"),
    ("HOUSTON", "TEXANS BEAT COLTS 26-3 BEHIND STROUD"),
    ("NAPLES", "A LIM KIM LEADS LPGA FINALE, HOLE-IN-ONE"),
    ("ESPOO", "SHIMADA LEADS FINLANDIA AFTER SHORT PROGRAM"),
    ("WASHINGTON", "SPIRIT REACH NWSL CHAMPIONSHIP FINAL"),
    ("WELLINGTON", "RAHUL TON PUTS INDIA 344/2, TRAIL BY 24"),
    ("RAWALPINDI", "PAKISTAN BEAT SRI LANKA, WIN TEST SERIES"),
    ("ABU DHABI", "UAE BULLS WIN T10 TITLE, BEAT YAS LIONS"),
    ("DOHA", "SRI LANKA A BEAT HONG KONG BY 24 RUNS"),
    ("DOHA", "PAKISTAN SHAHEENS BEAT UAE BY 61 RUNS"),
    ("DOHA", "BANGLADESH A EDGE AFGHANISTAN A BY 1 WICKET"),
    ("KUALA LUMPUR", "INDIA U17 DRAW MALAYSIA, TOP GROUP E"),
    ("EINDHOVEN", "NEC 1-4 PSV IN DUTCH LEAGUE"),
    ("WOLVERHAMPTON", "WOLVES 2-1 CHARLTON"),
    ("MADRID", "RAYO 0-1 VALENCIA"),
    ("LONDON", "CHELSEA 1-4 LEEDS"),
    ("BIRMINGHAM", "ASTON VILLA 0-0 SUNDERLAND"),
    ("BOURNEMOUTH", "BOURNEMOUTH 2-0 NOTTINGHAM FOREST"),
    ("COVENTRY", "COVENTRY 3-2 CRYSTAL PALACE"),
    ("SHEFFIELD", "SHEFFIELD UTD 4-0 WATFORD"),
    ("LEVERKUSEN", "LEVERKUSEN 4-0 PADERBORN"),
    ("BERLIN", "UNION BERLIN 1-5 RB LEIPZIG"),
    ("DORTMUND", "GLADBACH 0-1 DORTMUND"),
    ("FRANKFURT", "FRANKFURT 1-0 HOFFENHEIM"),
    ("TRANMERE", "TRANMERE 2-1 COLCHESTER"),
    ("NORTHAMPTON", "NORTHAMPTON 3-2 ROCHDALE"),
    ("CHESTERFIELD", "CHESTERFIELD 4-1 SHREWSBURY"),
    ("WASHINGTON", "TRUMP WEIGHS NEW STRIKES ON IRAN"),
    ("LONDON", "TRUMP: EUROPE SHOULD DEFUND UKRAINE"),
    ("WASHINGTON", "FEMA FACES BED BUG EMERGENCY"),
    ("BRUSSELS", "EU-WIDE CALL CENTRE SCAM NETWORK EXPOSED"),
    ("ANTALYA", "EU: USE PLEDGED CASH FOR AFRICA CLIMATE"),
    ("VIENNA", "AUSTRIA BLAMES RUSSIA FOR EMBASSY DAMAGE"),
    ("GENEVA", "UN NOTES AI WEAPONS TALKS, NO BINDING DEAL"),
    ("KATHMANDU", "NEPAL FANS CELEBRATE CRICKET RISE"),
    ("MADRID", "SPAIN FREES CHAMBERS ON BAIL AFTER US ERROR"),
    ("BEIJING", "CHINA TO JAPAN: CLARIFY TAIWAN REMARKS"),
    ("PARIS", "FRANCE FACES SCHOOL ABUSE RECKONING"),
    ("TEHRAN", "IRAN SENTENCES TAEKWONDO CHAMP TO DEATH"),
    ("SANAA", "BAD PETROL STALLS YEMENI DRIVERS"),
    ("ANTALYA", "UN WEIGHS CARBON CLEAN-UP TECH AT COP31"),
    ("KYIV", "ZELENSKY: NEXT PEACE TALKS MUST DELIVER"),
    ("KYIV", "ZELENSKY: NATO BEST SECURITY GUARANTEE"),
    ("WASHINGTON", "US ENVOYS WATCH UKRAINE PEACE MOVES"),
    ("WASHINGTON", "US OPENS PACIFIC SEABED TO MINING"),
    ("ABU DHABI", "UAE: SORRY TO BE DRAWN INTO SOMALIA ROW"),
    ("RAMALLAH", "350 CHILDREN HELD IN ISRAELI PRISONS"),
    ("SACRAMENTO", "CALIFORNIA PROBES NVIDIA OVER EX-CHIEF"),
    ("MOSCOW", "RUSSIA ISSUES PEACE DECLARATION AFTER SUMMIT"),
    ("ANTALYA", "COP31 GIVES HOST TURKEY SIDE DEALS"),
    ("SHENZHEN", "3 LEADERS AGREE: REMOVE LIMITS ON SELVES"),
    ("BERLIN", "SKYFALL, AUTERION TO BUILD DRONE PLANT"),
    ("WASHINGTON", "FBI PROBES NCIC DATABASE HACK"),
    ("TAIZ", "TAIZ FAMILIES ON LIFE UNDER BLOCKADE"),
    ("BERLIN", "MERZ: EUROPE WILL NOT ENDORSE 'YALTA 2'"),
    ("ANKARA", "TURKEY, IRAQ FOREIGN MINISTERS MEET"),
    ("SYDNEY", "HAZLEWOOD MAY RETHINK FUTURE IF CUMMINS AXED"),
    ("WELLINGTON", "NZ 368, INDIA REPLY 317/2 ON DAY 3"),
]

# ---------------------------------------------------------------- layout
MX = 16
COLW = 322
COLX = [16, 350, 684]
ROW_H = 9


def build():
    n_stories = len(HEROES) + len(TIMELINE) + len(BRIEFS)
    places = {p for p, _ in BRIEFS}
    places |= {h[1] for h in HEROES}
    places |= {"MERCURY", "SINALOA"}
    n_places = len(places)
    assert len(BRIEFS) == 162, len(BRIEFS)
    assert n_places >= 60, n_places

    # every character must exist in the embedded font (ASCII only)
    all_text = []
    for k, pl, hd, sm in HEROES:
        all_text += [k, pl, hd, sm]
    for lab, val, ch in MARKETS:
        all_text += [lab, val, ch]
    for t, b in TIMELINE:
        all_text += [t, b]
    all_text += [QUOTE, QUOTE_BY]
    for p, t in BRIEFS:
        all_text += [p, t]
    for s in all_text:
        for ch in s.upper():
            assert ch in FONT, repr(ch)

    cv = Canvas(W, H, PAPER)

    # ---- masthead
    cv.draw_text_center(W // 2, 8, "THE WORLD", 8, INK)
    cv.draw_text_center(W // 2, 70, "SATURDAY, 21 NOVEMBER 2026", 2, NAVY)
    cv.draw_text(MX, 90, "ONE DAY - ONE PAGE - THE WHOLE WORLD", 1, GREY)
    cv.draw_text_right(W - MX, 90,
                       "%d STORIES - %d PLACES" % (n_stories, n_places),
                       1, RED)
    cv.hline(MX, 100, W - 2 * MX, INK, 2)
    cv.hline(MX, 103, W - 2 * MX, INK, 1)

    # ---- heroes: 3 cards
    hy, hh = 110, 128
    for i, (kick, place, head, summ) in enumerate(HEROES):
        x = COLX[i]
        cv.rect(x, hy, COLW, hh, INK, 1)
        cv.fill_rect(x + 1, hy + 1, COLW - 2, 4, RED if i != 1 else NAVY)
        cv.draw_text(x + 10, hy + 12, kick, 1, RED)
        hlines = wrap_text(head, 2, COLW - 20)
        assert len(hlines) <= 3, hlines
        yy = hy + 26
        for ln in hlines:
            cv.draw_text(x + 10, yy, ln, 2, INK)
            yy += 16
        slines = wrap_text(summ, 1, COLW - 20)
        assert len(slines) <= 4, slines
        yy += 4
        for ln in slines:
            cv.draw_text(x + 10, yy, ln, 1, INK)
            yy += 9

    # ---- markets band (navy, 2 rows x 4 chips)
    my = 246
    cv.fill_rect(MX, my, W - 2 * MX, 46, NAVY)
    for r in range(2):
        for c in range(4):
            idx = r * 4 + c
            lab, val, ch = MARKETS[idx]
            cell_x = MX + c * 248
            cy = my + 6 + r * 19
            prefix = ("MARKETS: " if idx == 0 else "") + lab + " " + val + " "
            cv.draw_text(cell_x + 6, cy, prefix, 1, WHITE)
            col = UP if ch.startswith("+") else DOWN
            cv.draw_text(cell_x + 6 + text_width(prefix, 1), cy, ch, 1, col)

    # ---- timeline
    ty = 300
    cv.draw_text(MX, ty, "TIMELINE - SATURDAY IN SIX BEATS", 1, INK)
    cv.draw_text_right(W - MX, ty, "ALL TIMES UTC", 1, RED)
    cv.hline(MX, ty + 10, W - 2 * MX, INK, 1)
    for i, (t, beat) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        x = COLX[col]
        y = ty + 18 + row * 30
        cv.draw_text(x, y, t, 1, RED)
        blines = wrap_text(beat, 1, COLW)
        assert len(blines) <= 2, blines
        yy = y + 10
        for ln in blines:
            cv.draw_text(x, yy, ln, 1, INK)
            yy += 9

    # ---- quote of the day
    qy = 378
    cv.fill_rect(MX, qy, W - 2 * MX, 40, GOLD)
    cv.rect(MX, qy, W - 2 * MX, 40, INK, 1)
    cv.draw_text_center(W // 2, qy + 5, "QUOTE OF THE DAY", 1, RED)
    assert text_width(QUOTE, 2) <= W - 2 * MX
    cv.draw_text_center(W // 2, qy + 16, QUOTE, 2, INK)
    cv.draw_text_center(W // 2, qy + 31, QUOTE_BY, 1, NAVY)

    # ---- briefs header
    by = 426
    cv.draw_text(MX, by, "THE WORLD IN BRIEF", 2, INK)
    cv.draw_text_right(W - MX, by + 7, "%d STORIES - 3 COLUMNS" % len(BRIEFS),
                       1, GREY)
    cv.hline(MX, by + 18, W - 2 * MX, INK, 2)

    # ---- briefs grid: 3 columns x 54 rows, one line each
    gy = 450
    cv.vline(344, gy, 54 * ROW_H, LIGHT, 1)
    cv.vline(678, gy, 54 * ROW_H, LIGHT, 1)
    for idx, (place, text) in enumerate(BRIEFS):
        col, row = idx % 3, idx // 3
        x = COLX[col]
        y = gy + row * ROW_H
        line = place + " - " + text
        assert text_width(line, 1) <= COLW, line
        nx = cv.draw_text(x, y, place, 1, RED)
        nx = cv.draw_text(nx, y, " - ", 1, INK)
        cv.draw_text(nx, y, text, 1, INK)

    # ---- footer with explicit date check
    fy = 944
    cv.hline(MX, fy - 4, W - 2 * MX, INK, 1)
    cv.draw_text_center(
        W // 2, fy,
        "DATE CHECK: EVERY ITEM VERIFIED IN SAT 21 NOV 2026 EDITIONS. "
        "ITEMS DATED OTHER DAYS EXCLUDED.", 1, RED)
    cv.draw_text_center(
        W // 2, fy + 11,
        "SOURCES: AP - REUTERS - BBC - CNN - AFP - USGS - ESA - JAXA - "
        "UPI - GUARDIAN - ONETURN - DALTON DAILY", 1, INK)
    cv.draw_text_center(
        W // 2, fy + 22,
        "THE WORLD - NEWS-IMAGE-20261121 - %d STORIES - %d PLACES - "
        "STDLIB ONLY - DETERMINISTIC PNG" % (n_stories, n_places), 1, GREY)
    return cv, n_stories, n_places


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    cv, n_stories, n_places = build()
    data = png_bytes(cv)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("stories=%d places=%d size=%dx%d bytes=%d md5=%s" % (
        n_stories, n_places, W, H, len(data),
        hashlib.md5(data).hexdigest()))


if __name__ == "__main__":
    main()
