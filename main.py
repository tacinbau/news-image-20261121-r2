#!/usr/bin/env python3
"""THE WORLD - Saturday, 21 November 2026.
Front-page broadsheet: 3 heroes, briefs in 3 columns, market strip,
UTC timeline, Quote of the Day, explicit DATE CHECK footer.

Stdlib only: hashlib, math, os, struct, zlib. No network, no PIL,
no third-party imports. Writes ONLY to $MAKEFUN_OUTPUT_DIR/entry.png.
Deterministic: identical input -> identical bytes (no timestamps).
"""

import hashlib
import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (248, 244, 236)
INK = (22, 19, 14)
RED = (158, 27, 27)
NAVY = (31, 58, 95)
TEAL = (15, 76, 76)
MUTED = (107, 101, 90)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows, each row a 5-bit int (bit 4 = leftmost pixel).
# Lowercase is rendered as uppercase (broadsheet caps style).
FONT = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    '3': (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ',': (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ':': (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ';': (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x06, 0x04, 0, 0x04),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    '"': (0x0A, 0x0A, 0, 0, 0, 0, 0),
    '-': (0, 0, 0, 0x0E, 0, 0, 0),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '/': (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '%': (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '#': (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    '@': (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    '+': (0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0),
    '*': (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
    '=': (0, 0, 0x1F, 0, 0x1F, 0, 0),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    '[': (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    ']': (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
    '_': (0, 0, 0, 0, 0, 0, 0x1F),
}

_REPL = {
    '\u2014': '-', '\u2013': '-', '\u2019': "'", '\u2018': "'",
    '\u201c': '"', '\u201d': '"', '\u00b7': '.', '\u2022': '.',
    '\u00e9': 'E', '\u00e8': 'E', '\u00fc': 'U', '\u00f6': 'O',
}


def clean(s):
    out = []
    for ch in s:
        if ch in _REPL:
            ch = _REPL[ch]
        ch = ch.upper()
        out.append(ch if ch in FONT else ' ')
    return ''.join(out)


def tw(s, scale=1):
    """Drawn pixel width of text at scale (advance 6*scale, no trailing gap)."""
    n = len(clean(s))
    return n * 6 * scale - scale if n else 0


# ---------------------------------------------------------------- canvas
canvas = bytearray(W * H * 3)


def fill(c):
    canvas[:] = bytes(c) * (W * H)


def rect(x, y, w, h, c):
    if w <= 0 or h <= 0:
        return
    row = bytes(c) * w
    for yy in range(y, y + h):
        i = (yy * W + x) * 3
        canvas[i:i + w * 3] = row


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i:i + 3] = bytes(c)


def draw_text(x, y, s, scale=1, c=INK, bold=False):
    """Draw text; raises ValueError if it would run off the right edge."""
    s = clean(s)
    if x + tw(s, scale) > W:
        raise ValueError('text overflows right edge: %r' % s)
    cx = x
    for ch in s:
        glyph = FONT[ch]
        passes = (0, 1) if bold else (0,)
        for dx in passes:
            for r in range(7):
                bits = glyph[r]
                if not bits:
                    continue
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        rect(cx + dx + col * scale, y + r * scale,
                             scale, scale, c)
        cx += 6 * scale
    return cx


def draw_text_centered(cx, y, s, scale=1, c=INK, bold=False):
    draw_text(cx - tw(s, scale) // 2, y, s, scale, c, bold)


def globe(cx, cy, r, c):
    """Small wire globe: circle + one meridian + equator, via math."""
    steps = 120
    for i in range(steps):
        a = 2.0 * math.pi * i / steps
        px(cx + int(round(r * math.cos(a))), cy + int(round(r * math.sin(a))), c)
        px(cx + int(round((r * 0.45) * math.cos(a))),
           cy + int(round(r * math.sin(a))), c)
    rect(cx - r, cy - 1, 2 * r + 1, 2, c)


# ---------------------------------------------------------------- PNG writer
def _chunk(typ, data):
    return (struct.pack('>I', len(data)) + typ + data +
            struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF))


def png_bytes():
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += canvas[y * W * 3:(y + 1) * W * 3]
    return (b'\x89PNG\r\n\x1a\n' + _chunk(b'IHDR', ihdr) +
            _chunk(b'IDAT', zlib.compress(bytes(raw), 6)) +
            _chunk(b'IEND', b''))

# ---------------------------------------------------------------- data
# Every item verified against live reporting dated Sat 21 Nov 2026
# (AP, Reuters, BBC, AFP, USGS, ESA, NYT, CNN).
# Items dated other days were EXCLUDED - see footer DATE CHECK.
# (region, text) - region feeds the masthead region count.

HEROES = [
    ("KYIV — WAR IN EUROPE", RED,
     ["RUSSIA RAINS FIRE", "ON KYIV — AND", "POLAND"],
     ["400+ DRONES, 110 MISSILES HIT KYIV; 8 DEAD.",
      "3 OBJECTS LAND IN POLAND. NATO: GRAVE BREACH.",
      "RUTTE IN WARSAW: EVERY INCH WILL BE DEFENDED."]),
    ("NEW YORK — MARKETS", NAVY,
     ["MARKETS IN", "FREEFALL AS", "AI ROUT BITES"],
     ["S&P -3.7%, NASDAQ -5.3%, NIKKEI -5.1%.",
      "DOW, S&P IN CORRECTION; VIX SPIKES TO 35.89.",
      "NVIDIA -14% IN A DAY; ANTHROPIC -9% AFTER IPO."]),
    ("MERCURY — SPACE", TEAL,
     ["BEPICOLOMBO", "REACHES MERCURY", "AFTER 8 YEARS"],
     ["ESA-JAXA CRAFT ENTERS ORBIT 18:24 UTC.",
      "ONLY THE 2ND CRAFT EVER TO CIRCLE",
      "THE INNERMOST PLANET. SCIENCE STARTS APR 2027."]),
]

COLUMNS = [
    [("WAR & DIPLOMACY", [
        ("Ukraine", "KRYVYI RIH — MISSILE KILLS 2, WOUNDS 42"),
        ("Ukraine", "KYIV — ZELENSKY: BRIDGE STRIKES \"FAIR RESPONSE\""),
        ("UK", "KYIV — STREETING: PUTIN \"COLD-BLOODED KILLER\""),
        ("Ukraine", "KYIV — ZELENSKY: PUTIN IS \"A KILLER\""),
        ("EU", "BERLIN — TRUMP TOLD EU TO SPEND LESS ON UKRAINE"),
        ("Poland", "WARSAW — NATO COUNCIL TO MEET MONDAY ON BREACH"),
        ("Finland", "GULF OF FINLAND — DRONES SET RUSSIAN SHIP ABLAZE"),
        ("Denmark", "COPENHAGEN — DENMARK EXPELS RUSSIAN ATTACHE"),
        ("Denmark", "COPENHAGEN — 2 HELD OVER PLOT TO KILL RAPPER"),
        ("Germany", "BERLIN — GERMAN MINISTER SORRY OVER \"STUPID\" JIBE"),
        ("Germany", "BERLIN — DRONE PLANT DEAL FOR UKRAINE, GERMANY"),
        ("UN", "GENEVA — UN KILLER-ROBOT TALKS TO RUN UNTIL 2028"),
        ("China", "SHENZHEN — XI EMERGES STRONGER FROM SUMMIT"),
        ("USA", "MIAMI — ZELENSKY OPEN TO PUTIN TALKS AT G20"),
        ("USA", "WASHINGTON — TRUMP WEIGHS NEW STRIKES ON IRAN"),
        ("Qatar", "TEHRAN — QATARI DELEGATION HOLDS TALKS IN TEHRAN"),
    ]),
     ("AMERICAS", [
        ("Mexico", "SINALOA — MEXICO CAPTURES \"EL CHAPO ISIDRO\""),
        ("Mexico", "SINALOA — CARTEL ROADBLOCKS BURN AFTER CAPTURE"),
        ("USA", "WASHINGTON — FBI PROBES HACK OF CRIME DATABASE"),
        ("USA", "WASHINGTON — TRUMP FIRES SENIOR TECH ADVISER"),
        ("USA", "WASHINGTON — TRUMP: BAN AI CENTRES ABROAD"),
        ("USA", "SACRAMENTO — CALIFORNIA SUBPOENAS NVIDIA"),
        ("USA", "SACRAMENTO — WAYMO BANNED FROM STATE FREEWAYS"),
        ("USA", "LOS ANGELES — PALISADES FIRE STARTER GUILTY"),
        ("USA", "NEW YORK — MAMDANI: CLOSE RIKERS JAIL BY 2032"),
        ("USA", "WASHINGTON — CONGRESS COOL ON $50BN AIR OVERHAUL"),
        ("USA", "WASHINGTON — TRUMP AUDITIONS RUBIO, VANCE"),
        ("USA", "NEW YORK — JUDGE OKS $7.25BN BAYER SETTLEMENT"),
        ("Mexico", "TAPACHULA — 250-MIGRANT CARAVAN REACHES MEXICO"),
        ("Brazil", "SAO PAULO — LULA BACKS SANCHEZ IN SPAIN VOTE"),
        ("Haiti", "PORT-AU-PRINCE — SALVADORAN TROOPS FIGHT GANGS"),
        ("USA", "WASHINGTON — ICE-PACT SHERIFFS OUSTED BY VOTERS"),
        ("USA", "WASHINGTON — THANKSGIVING DINNER TO COST MORE"),
        ("USA", "WASHINGTON — MAN WHO WRECKED $60M JET CHARGED"),
    ]),
     ("MIDDLE EAST", [
        ("Palestine", "GAZA CITY — ISRAELI STRIKE KILLS 3 IN AID VEHICLE"),
        ("Palestine", "GAZA — ISRAELI FIRE KILLS PALESTINIANS"),
        ("Palestine", "GAZA — 350 CHILDREN HELD IN ISRAELI PRISONS"),
        ("Lebanon", "BEIRUT — ISRAELI STRIKES HIT 4 SOUTH LEBANON AREAS"),
        ("Lebanon", "BEIRUT — EUROPE PUSHES TO REPLACE UN PEACEKEEPERS"),
        ("Iraq", "BAGHDAD — TROOPS TO MOVE ON JURF AL-SAKHAR"),
        ("Yemen", "SANAA — HOUTHI LOYALTY TEST FOR RULING GPC"),
        ("Iran", "TEHRAN — TAEKWONDO CHAMPION SENTENCED TO DEATH"),
        ("UAE", "DUBAI — UAE \"REGRETS\" ROLE IN SOMALIA ROW"),
        ("Persian Gulf", "HORMUZ — PUGH SWIMS STRAIT TO FLAG WAR ECO TOLL"),
        ("Iraq", "BASRA — POWER STATION FIRE KILLS 4, INJURES 30"),
        ("Syria", "DAMASCUS — SYRIA DETAINES EX-GENERAL OVER MASSACRE"),
        ("Israel", "JERUSALEM — THE BATTLE OVER A JERUSALEM CAFE"),
    ])],
    [("EUROPE", [
        ("UK", "LONDON — EU YOUTH SCHEME: LIVE, WORK UP TO 3 YEARS"),
        ("UK", "LONDON — MILIBAND: EU DEAL NOT TIED TO FEES"),
        ("UK", "LONDON — TRAFALGAR TREE FELLED IN OSLO"),
        ("UK", "LONDON — UK COLDEST NIGHT OF AUTUMN SO FAR"),
        ("UK", "LONDON — UK TO SEEK EVEN CLOSER EU TIES: BURNHAM"),
        ("France", "PARIS — MARCHES DRAW 82,500 AS PROTESTS COOL"),
        ("France", "PARIS — DEPARDIEU, HOUELLEBECQ FACE SEX PROBE"),
        ("France", "PARIS — POLICE SENTENCED FOR BEATING ZECLER"),
        ("France", "PARIS — RALLY AGAINST POLICE GUN BILL"),
        ("Germany", "BERLIN — STUDENTS MARCH AGAINST REARMAMENT"),
        ("Italy", "ROME — ITALY OKS TESLA ASSISTED DRIVING FIRST"),
        ("Italy", "ROME — WORKERS, STUDENTS STRIKE OVER LIVING COSTS"),
        ("Italy", "ROME — ITALY PASSES ANTISEMITISM LAW"),
        ("Spain", "MADRID — SPAIN HEADS TO NOV 29 SNAP ELECTION"),
        ("Spain", "MADRID — SANCHEZ: OURS IS \"ONE OF CLEANEST\" GOVTS"),
        ("Spain", "MADRID — DATA CENTRES MUST USE 80% GREEN POWER"),
        ("EU", "BRUSSELS — COSTA PITCHES 3% BIG-TECH TAX"),
        ("Norway", "OSLO — NORWAY WARNS OF RISING TERROR THREAT"),
        ("EU", "BRUSSELS — EU OIL PLAN PUTS ARMY FUEL FIRST"),
        ("Poland", "WARSAW — POLAND SEEKS NATO REINFORCEMENTS"),
        ("Turkey", "ANKARA — JAILED MAYOR BARRED FROM 2028 RACE"),
        ("Turkey", "ISTANBUL — 420M OF HAGIA SOPHIA TUNNELS FOUND"),
        ("Europe", "EUROPE — PROTESTS SWEEP 25+ COUNTRIES FOR WAGES"),
        ("Turkey", "ANTALYA — COP31 IN OVERTIME AS FUEL FIGHT RAGES"),
    ]),
     ("AFRICA", [
        ("South Africa", "CAPE TOWN — MLAMBO-NGCUKA DIES AGED 71"),
        ("South Africa", "CAPE TOWN — ANC FIGHTS TO HOLD KEY CITIES"),
        ("South Africa", "PRETORIA — RESERVE BANK HOLDS RATE AT 7.25%"),
        ("Somalia", "MOGADISHU — SOMALIA EXPELS UAE AMBASSADOR"),
        ("Kenya", "NAIROBI — KENYA POLICE HEADCOUNT OVER RUSSIA FEARS"),
        ("Kenya", "NAIROBI — US FIRM WINS MRIMA HILL MINING DEAL"),
        ("Kenya", "NAIROBI — 2 STUDENTS HURT IN BUS CROSSFIRE"),
        ("Nigeria", "ABUJA — 36 STATES BACK LOCAL POLICE REFORM"),
        ("Nigeria", "ABUJA — CUSTOMS HALTS TRAINING OF 3,852 RECRUITS"),
        ("Nigeria", "IBADAN — TINUBU HONOURS BOAT TRAGEDY VICTIMS"),
        ("Ethiopia", "ADDIS ABABA — 700,000 DISPLACED IN SOUTH"),
        ("Ethiopia", "ADDIS ABABA — ETHIOPIA ELECTED TO ICAO COUNCIL"),
        ("Ethiopia", "ADDIS ABABA — AIRLINE HIT BY LOYALTY CYBERATTACK"),
        ("Egypt", "CAIRO — AL-AZHAR HAILS ICJ ROHINGYA RULING"),
        ("Egypt", "CAIRO — EGYPT NEARS $2.3BN IMF DISBURSEMENT"),
        ("Senegal", "DAKAR — SENEGAL BYPASSES HOUSE FOR $2.2BN IMF DEAL"),
        ("Uganda", "KAMPALA — TRADERS END STRIKE AFTER TAX PLEDGE"),
        ("Gabon", "LIBREVILLE — GABON HANDS EXXONMOBIL OIL MANDATE"),
        ("Ghana", "ACCRA — MAHAMA: CHIEFS MUST SHUN PARTY POLITICS"),
        ("DR Congo", "KINSHASA — WHO WARNS OF EBOLA CHILD DEATHS"),
        ("Morocco", "RABAT — MOROCCO, MALI WIN BIG AT U17 WORLD CUP"),
        ("Liberia", "MONROVIA — LIBERIA SPEAKER IN NIGERIA HOTEL ROW"),
    ])],
    [("ASIA-PACIFIC", [
        ("Timor-Leste", "DILI — M6.8 QUAKE OFF TIMOR-LESTE, NO TSUNAMI"),
        ("India", "NEW DELHI — TAINTED ALCOHOL KILLS 11, 180+ IN CARE"),
        ("China", "BEIJING — ARMY SUSPENDS SF EXPRESS FROM DEALS"),
        ("China", "BEIJING — CHINA TO JAPAN: CLARIFY TAIWAN REMARKS"),
        ("Japan", "TOKYO — TAKAICHI SNUBBED BY XI IN CHINA"),
        ("Japan", "FUKUSHIMA — 1,500 TRAPPED BY HEAVY SNOW"),
        ("South Korea", "SEOUL — LEE TOURS SK AI DATA CENTRE, FLAGS CRUNCH"),
        ("South Korea", "SEOUL — KOREA EYES CURB ON \"IMPERIAL PRESIDENCY\""),
        ("North Korea", "PYONGYANG — KIM TOURS SCHOOL FACTORIES AFTER SNUB"),
        ("Philippines", "MANILA — PHILIPPINES RESUMES RICE BUYING"),
        ("Vietnam", "HANOI — VIETNAM PASSES FAST LAND-SEIZURE LAW"),
        ("Indonesia", "JAKARTA — DAYCARE CHIEF JAILED 5 YEARS FOR ABUSE"),
        ("Nepal", "KATHMANDU — NEPAL FANS CELEBRATE CRICKET RISE"),
    ]),
     ("MARKETS & BUSINESS", [
        ("USA", "NEW YORK — NASDAQ -5.3%, NOW DOWN FOR THE YEAR"),
        ("USA", "NEW YORK — VIX JUMPS 86% IN A WEEK TO 35.89"),
        ("USA", "NEW YORK — NVIDIA -14% IN A DAY, -22% IN A WEEK"),
        ("USA", "NEW YORK — AMD -13%, MICRON -14%, BROADCOM -12%"),
        ("USA", "NEW YORK — ANTHROPIC -9% A DAY AFTER $2TN IPO"),
        ("Japan", "TOKYO — NIKKEI -5.1% AS AI ROUT SPREADS"),
        ("South Korea", "SEOUL — KOSPI -5% IN OVERNIGHT SELL-OFF"),
        ("UK", "LONDON — TECH SELL-OFF DRAGS MARKETS DOWN"),
        ("USA", "NEW YORK — GOLD'S WORST WEEK SINCE MARCH"),
        ("USA", "NEW YORK — DOW, S&P IN CORRECTION, 10% OFF PEAKS"),
        ("USA", "NEW YORK — S&P IN 7-DAY SLIDE, LONGEST SINCE 2020"),
        ("USA", "NEW YORK — WEEK: DOW -8%, S&P -8.6%, NASDAQ -10%"),
    ]),
     ("SCIENCE & HEALTH", [
        ("UK", "LONDON — PANCREATIC PILL: 1 IN 12 CLEAR"),
        ("UK", "LONDON — MOSQUITOES BRED TO FEND OFF DENGUE"),
        ("USA", "WASHINGTON — US DECLASSIFIES MORE UFO FOOTAGE"),
        ("USA", "WASHINGTON — AIDE 'MAY HAVE CRACKED' MATHS PUZZLE"),
        ("Peru", "LIMA — M6.7 QUAKE SHAKES PERU, FELT IN LIMA"),
        ("USA", "LOS ANGELES — $114M WILDLIFE CROSSING NEARS DONE"),
        ("USA", "WASHINGTON — ROMANCE SCAMS USE STOLEN FACES"),
    ]),
     ("SPORT", [
        ("UK", "LONDON — ENGLAND 37-12 NEW ZEALAND, RECORD WIN"),
        ("Australia", "MELBOURNE — AUSTRALIA EDGE ENGLAND BY 3 WICKETS"),
        ("Australia", "MELBOURNE — CHAUDHARY 66 SEALS MCG THRILLER"),
        ("UK", "MANCHESTER — MAN CITY 1-1 FULHAM, 20-GAME RUN ENDS"),
        ("UK", "LONDON — LEEDS WIN 4-1 AWAY AT CHELSEA"),
        ("UK", "LONDON — TONIGHT: ARSENAL V NEWCASTLE"),
        ("USA", "LAS VEGAS — VERSTAPPEN ON POLE FOR TONIGHT'S GP"),
        ("USA", "LAS VEGAS — ANTONELLI FASTEST BUT DROPS TO 6TH"),
        ("USA", "DENVER — JOKIC POWERS NUGGETS PAST ROCKETS 133-124"),
        ("USA", "LOS ANGELES — WATKINS 36 PTS AS USC BEAT BAYLOR"),
    ]),
     ("CULTURE & LIFE", [
        ("UK", "LONDON — CATHERINE TALKS CANCER IN FILM \"HEAL\""),
        ("USA", "LOS ANGELES — GTA 6 SALES TOP $2.3BN IN 2 DAYS"),
        ("Philippines", "MANILA — PET CREMATION SCAM AIRED ON LIVESTREAM"),
        ("UK", "LONDON — PHOEBE BRIDGERS PHONE BAN SPARKS FAN ART"),
        ("UK", "LONDON — TRADWIFE FOR 2 DAYS: \"I WAS EXHAUSTED\""),
    ])],
]

# Friday 20 Nov closes (markets shut Saturday) - labelled as such on the page.
MARKET_CHIPS = ("S&P 500 6,910 -3.7% | DOW 48,147 -1.9% | "
                "NASDAQ 22,618 -5.3% | NIKKEI -5.1% | KOSPI -5% | "
                "VIX 35.89 | NVIDIA -14% | ANT $88.91 -9%")

TIMELINE = [
    ("00:09", "PERU M6.7 QUAKE"),
    ("04:26", "DENMARK: RUSSIA PLOT"),
    ("05:44", "S. AFRICA: MLAMBO-NGCUKA DIES"),
    ("07:17", "ZELENSKY: BRIDGE STRIKES \"FAIR\""),
    ("08:54", "COP31 DEADLOCK"),
    ("13:30", "DEPARDIEU PROBE OPENS"),
    ("17:03", "FRANCE MARCHES: 82,500"),
    ("18:24", "BEPICOLOMBO IN MERCURY ORBIT"),
]

QUOTE = "I CAN GUARANTEE THAT NATO WILL DEFEND EVERY INCH OF POLISH TERRITORY."
QUOTE_BY = "— MARK RUTTE, NATO SECRETARY GENERAL, WARSAW"

FOOTER = [
    "DATE CHECK: ALL STORIES DATED SAT 21 NOV 2026.",
    "EXCLUDED: ICJ RULING + ANTHROPIC IPO (THU 19 NOV); UK-EU SIGNING, "
    "TESLA ARGENTINA, UEFA DRAW, EU-INDONESIA DEAL, GUPTA CASE (FRI 20 NOV).",
    "MARKET CLOSES ARE FRI 20 NOV - MARKETS SHUT SAT. "
    "SOURCES: AP, REUTERS, BBC, AFP, USGS, ESA, NYT, CNN.",
]

# ---------------------------------------------------------------- layout
MX = 20            # side margin
CW = 320           # column / hero width
COLX = [20, 352, 684]
BRIEF_TOP = 244
BRIEF_BOTTOM = 894
LINE_H = 12
HEAD_H = 15


def draw_hero(x, y, kicker, accent, head_lines, deck_lines):
    rect(x, y, CW, 124, WHITE)
    rect(x, y, CW, 4, accent)
    # 1px border
    rect(x, y + 4, CW, 1, INK)
    rect(x, y + 123, CW, 1, INK)
    rect(x, y, 1, 124, INK)
    rect(x + CW - 1, y, 1, 124, INK)
    draw_text(x + 8, y + 10, kicker, 1, accent, bold=True)
    yy = y + 24
    for line in head_lines:
        assert tw(line, 2) <= CW - 16, line
        draw_text(x + 8, yy, line, 2, INK)
        yy += 16
    yy = y + 78
    for line in deck_lines:
        assert tw(line, 1) <= CW - 16, line
        draw_text(x + 8, yy, line, 1, INK)
        yy += 10


def draw_brief(x, y, text):
    assert tw(text, 1) <= CW - 16, text
    rect(x, y + 2, 3, 3, RED)
    head, sep, rest = text.partition(" — ")
    tx = x + 8
    if sep:
        draw_text(tx, y, head, 1, INK, bold=True)
        tx += tw(head, 1)
        draw_text(tx, y, " - " + rest, 1, INK)
    else:
        draw_text(tx, y, text, 1, INK)


def draw_column(x, sections):
    y = BRIEF_TOP
    for title, items in sections:
        draw_text(x, y, title, 1, RED, bold=True)
        rect(x, y + 10, CW, 1, RED)
        y += HEAD_H
        for _region, text in items:
            draw_brief(x, y, text)
            y += LINE_H
        y += 2
    assert y <= BRIEF_BOTTOM, "column overflows brief area: %d" % y
    return y


def main():
    n_briefs = sum(len(items) for col in COLUMNS for _t, items in col)
    regions = set()
    for col in COLUMNS:
        for _t, items in col:
            for region, _text in items:
                regions.add(region)
    regions.update(("Ukraine", "USA", "Mercury"))  # hero datelines
    n_stories = n_briefs + len(HEROES)

    fill(PAPER)
    rect(0, 0, W, 4, RED)
    globe(52, 31, 17, INK)

    draw_text_centered(W // 2, 10, "THE WORLD", 6, INK)
    date_line = ("SATURDAY, 21 NOVEMBER 2026 - %d STORIES - %d REGIONS - "
                 "ONE DAY, EVERYWHERE" % (n_stories, len(regions)))
    assert tw(date_line, 1) <= W - 2 * MX
    draw_text_centered(W // 2, 58, date_line, 1, INK)
    rect(MX, 72, W - 2 * MX, 1, INK)
    rect(MX, 75, W - 2 * MX, 1, INK)

    for x, (kicker, accent, head_lines, deck_lines) in zip(COLX, HEROES):
        draw_hero(x, 82, kicker, accent, head_lines, deck_lines)
    rect(MX, 212, W - 2 * MX, 1, INK)

    label = "MARKETS - FRI 20 NOV CLOSE"
    draw_text(MX, 220, label, 1, RED, bold=True)
    chips_x = MX + tw(label, 1) + 12
    assert chips_x + tw(MARKET_CHIPS, 1) <= W - MX, "market strip too wide"
    draw_text(chips_x, 220, MARKET_CHIPS, 1, INK)
    rect(MX, 236, W - 2 * MX, 1, INK)

    for x, sections in zip(COLX, COLUMNS):
        draw_column(x, sections)
    rect(MX, 898, W - 2 * MX, 1, INK)

    draw_text(MX, 904, "SATURDAY IN UTC", 1, RED, bold=True)
    for row in range(2):
        y = 918 + row * 14
        for i in range(4):
            t, text = TIMELINE[row * 4 + i]
            x = MX + i * 244
            assert tw(t + " " + text, 1) <= 244, text
            draw_text(x, y, t, 1, RED, bold=True)
            draw_text(x + tw(t, 1) + 6, y, text, 1, INK)
    rect(MX, 946, W - 2 * MX, 1, INK)

    assert tw(QUOTE, 2) <= W - 2 * MX
    draw_text_centered(W // 2, 954, QUOTE, 2, INK)
    draw_text_centered(W // 2, 972, QUOTE_BY, 1, MUTED)
    rect(MX, 986, W - 2 * MX, 1, INK)

    y = 992
    for line in FOOTER:
        assert tw(line, 1) <= W - 2 * MX, line
        draw_text(MX, y, line, 1, MUTED)
        y += 10

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    data = png_bytes()
    with open(path, "wb") as f:
        f.write(data)
    print("stories=%d briefs=%d heroes=%d regions=%d" %
          (n_stories, n_briefs, len(HEROES), len(regions)))
    print("md5=%s" % hashlib.md5(data).hexdigest())
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
