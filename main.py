#!/usr/bin/env python3
"""THE WORLD - Saturday, 21 November 2026.
A one-page newspaper front page summing up the day's world news.

Stdlib-only. No network, no third-party imports, no fonts from disk.
All text is rendered with an embedded 5x7 bitmap font.
Output goes ONLY to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Deterministic: identical bytes on every run.
"""
import hashlib
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font 5x7
# Each glyph is 7 rows of 5 bits ("1" = ink). ASCII only.
FONT = {
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '*': ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ',': ("00000", "00000", "00000", "00000", "00000", "01100", "00100"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '@': ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '[': ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    '\\': ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
    ']': ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    '^': ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '`': ("01000", "00100", "00010", "00000", "00000", "00000", "00000"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "00010", "10010"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '{': ("00110", "01000", "01000", "11100", "01000", "01000", "00110"),
    '|': ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    '}': ("01100", "00010", "00010", "00111", "00010", "00010", "01100"),
    '~': ("00000", "00000", "00000", "01001", "10110", "00000", "00000"),
}
FALLBACK = FONT['?']


def text_width(s, scale):
    return len(s) * 6 * scale - scale


# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (17, 17, 17)
SOFT = (84, 84, 76)
RULE = (180, 172, 152)
RED = (178, 28, 28)
DARKRED = (127, 18, 18)
BLUE = (30, 58, 95)
GOLD = (146, 90, 10)
GREEN = (22, 101, 52)
LIGHT = (238, 232, 216)
CARD = (255, 253, 247)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- canvas
buf = bytearray(W * H * 3)


def fill(c):
    r, g, b = c
    buf[0::3] = bytes([r]) * (W * H)
    buf[1::3] = bytes([g]) * (W * H)
    buf[2::3] = bytes([b]) * (W * H)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def rect(x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    r, g, b = c
    row = bytes((r, g, b)) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        buf[i:i + len(row)] = row


def border(x, y, w, h, c, t=1):
    rect(x, y, w, t, c)
    rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c)
    rect(x + w - t, y, t, h, c)


def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)


def draw_char(x, y, ch, scale, c):
    glyph = FONT.get(ch, FALLBACK)
    for row in range(7):
        bits = glyph[row]
        for col in range(5):
            if bits[col] == '1':
                rect(x + col * scale, y + row * scale, scale, scale, c)


def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s:
        draw_char(cx, y, ch, scale, c)
        cx += 6 * scale
    return cx - x


def draw_text_center(cx, y, s, scale, c):
    w = text_width(s, scale)
    draw_text(cx - w // 2, y, s, scale, c)


def wrap(s, max_chars):
    """Greedy word wrap to a list of lines, each <= max_chars."""
    lines = []
    for para in s.split('\n'):
        words = para.split(' ')
        cur = ''
        for wd in words:
            if not cur:
                cur = wd
            elif len(cur) + 1 + len(wd) <= max_chars:
                cur = cur + ' ' + wd
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(x, y, s, scale, c, max_chars, line_h=None):
    if line_h is None:
        line_h = 8 * scale + 1
    yy = y
    for ln in wrap(s, max_chars):
        draw_text(x, yy, ln, scale, c)
        yy += line_h
    return yy


# ---------------------------------------------------------------- PNG (stdlib only)
def _chunk(tag, data):
    out = struct.pack('>I', len(data)) + tag + data
    out += struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def png_bytes():
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw += buf[yy * stride:(yy + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    return (b'\x89PNG\r\n\x1a\n'
            + _chunk(b'IHDR', ihdr)
            + _chunk(b'IDAT', idat)
            + _chunk(b'IEND', b''))

# ---------------------------------------------------------------- data
# Every item was first reported on Saturday 21 November 2026 (UTC),
# in the Saturday wires (AP, Reuters, BBC, CNN, AFP, USGS, ESA, Schwab,
# Arab News, GMA, HT, NY Post). Friday-close markets and Friday-night
# events appear as carried in Saturday's editions. Items dated any other
# day were excluded. See DATE CHECK in the footer.

HEROES = [
    ("CLIMATE - ANTALYA, TURKIYE",
     "COP31 IN OVERTIME",
     "Fossil-fuel fight deadlocks talks past deadline; revised draft drops "
     "every mention of fossil fuels. Nearly 200 nations still split on finance."),
    ("MIDDLE EAST - RIYADH",
     "MISSILES OVER RIYADH",
     "Saudi defences intercept 3 Houthi ballistic missiles aimed at the "
     "capital, more over Jazan - the third straight night of attacks."),
    ("MARKETS - NEW YORK",
     "WALL ST ROUT",
     "S&P -3.7%, Nasdaq -5.3% in the worst week since April 2025. Nasdaq "
     "wipes out its 2026 gains; Nvidia sinks 14% in a day."),
]

MARKETS = [
    ("S&P 500", "6,910.39", "-3.70%"),
    ("NASDAQ", "22,617.73", "-5.28%"),
    ("DOW", "48,147.33", "-1.93%"),
    ("GOLD", "~$3,540", "-4.4%"),
    ("BITCOIN", "~$59,000", "LOWEST SINCE JUNE"),
    ("NVIDIA", "-14% DAY", "7TH WKLY LOSS"),
    ("ANTHROPIC", "~$89", "-9.1%  IPO $83"),
    ("TAIWAN TAIEX", "WORST WEEK", "SINCE 1990"),
]

# (region tag, headline) - main grid, 61 items
STORIES = [
    ("UKRAINE", "Russian missile hits Kryvyi Rih, Zelenskyy's hometown: 2 killed, 60 wounded."),
    ("UKRAINE", "Zelenskyy: Crimean Bridge strikes a 'fair response' after 109 Russian attacks on bridges."),
    ("UKRAINE", "Zelenskyy calls Putin a 'killer' after Trump calls the Russian leader a friend."),
    ("UKRAINE", "UK defence chief Streeting meets Zelenskyy in Kyiv; calls Putin a 'cold-blooded killer'."),
    ("RUSSIA", "Russian missile hits Poland as Kyiv's allies hold a military exercise, PM Tusk says."),
    ("DENMARK", "Denmark accuses Russia of plotting to kill rapper Kyivstoner; expels defence attache."),
    ("CHINA", "Trump, Xi and Putin end Shenzhen talks with nuclear-risk and energy pledges; no breakthrough."),
    ("CHINA", "Leaders issue joint declaration of peace after historic 90-minute trilateral at APEC Shenzhen."),
    ("TURKIYE", "COP31 in overtime: fossil-fuel fight deadlocks Antalya talks; draft drops fossil fuels."),
    ("TURKIYE", "COP31: China-Turkiye sign $15bn renewables deal; AIIB pledges $1.6bn climate finance."),
    ("SAUDI ARABIA", "Saudi defences intercept 3 Houthi ballistic missiles aimed at Riyadh, more over Jazan."),
    ("YEMEN", "'I tell my son it's just fireworks': life inside a Houthi-besieged Yemeni city."),
    ("GAZA", "Israeli strikes kill 6 in Gaza on Friday, medics say."),
    ("LEBANON", "UNIFIL logs extensive Israeli violations in south Lebanon in October: thousands of shells."),
    ("IRAN", "FM Araqchi: Iran seeks a diplomatic solution but will not give up domestic uranium enrichment."),
    ("IRAN", "Trump calls for a 'real deal' as US pledges continued economic pressure on Tehran."),
    ("IRAN", "Revolutionary Guard claims it shot down 2 US drones over the Strait of Hormuz; unverified."),
    ("MEXICO", "FBI most-wanted cartel boss 'Chapo Isidro' captured in Guasave, Sinaloa; gun battles follow."),
    ("MEXICO", "Two more cartel leaders detained in the same raid; FBI had offered a $5m bounty."),
    ("PERU", "M6.7 quake strikes the central Andes near Carhuamayo at 00:09 UTC; felt in Lima, no deaths."),
    ("INDIA", "PM Modi in Bihar to open the Nitish Setu bridge; visits IIT Kharagpur."),
    ("INDIA", "Cyclone Akvan to bring heavy rain; Ladakh panchayat polls held."),
    ("INDIA", "Rahul Gandhi attacks the government's economic policy at Columbia SIPA."),
    ("INDIA", "UP chief minister Yogi Adityanath's mother cremated; funeral held on Saturday."),
    ("NEPAL", "PM Balendra Shah faces his India test on a first visit."),
    ("PAKISTAN", "Pakistan beats Sri Lanka to win a first Test series in two years."),
    ("BANGLADESH", "Garment worker protests flare in Dhaka."),
    ("PHILIPPINES", "Duterte camp asks the ICC to reject an ex-Davao cop's recorded testimony."),
    ("PHILIPPINES", "Air Niugini jet makes an emergency landing at Davao airport."),
    ("PHILIPPINES", "Naga City votes in a plebiscite on highly urbanized city status."),
    ("PHILIPPINES", "PhilSA warns of Chinese rocket debris in Philippine waters."),
    ("SOUTH AFRICA", "ANC fights to keep control of key cities after an election setback."),
    ("SOUTH AFRICA", "Nearly 600 women killed within three months, police data shows."),
    ("UK", "New UK-EU deal does not depend on a tuition-fees agreement, Miliband says."),
    ("UK", "Burnham: UK to explore even closer ties with the EU after the deal."),
    ("UK", "EU-UK youth scheme: ages 18-31 may travel, work or study for up to 3 years."),
    ("UK", "Coldest night of autumn so far; cold alerts in force across Britain."),
    ("UK", "Trafalgar Square Christmas tree felled in Norway for London."),
    ("UK", "Catherine speaks openly about how cancer changed her in a BBC documentary."),
    ("USA", "FBI probes apparent hack of its NCIC crime database; USDA also reportedly hit."),
    ("USA", "Mamdani unveils a plan to close New York's Rikers Island jail by 2032."),
    ("USA", "Man convicted of starting the Palisades fire in Los Angeles."),
    ("USA", "US declassifies more UFO footage filmed in the Middle East."),
    ("USA", "Nikhil Gupta sentenced to 19+ years in a plot to kill Sikh leader Pannun in New York."),
    ("USA", "Asif Merchant gets 27 years for a Trump murder plot."),
    ("USA", "Florida pastor convicted in the plot to kill Haiti's President Moise."),
    ("USA", "Justice Dept seizes $1.2bn in crypto stolen from Binance."),
    ("USA", "Virginia reports the first measles-related child death of 2026; 290 cases this year."),
    ("USA", "Congress faces a possible shutdown before Christmas over funding and defence rows."),
    ("USA", "Federal judge rejects a long-term ban on Trump administration political ads."),
    ("USA", "DEA shuts the first known nitazene lab in the US, in Baton Rouge, Louisiana."),
    ("USA", "US soldier arrested in England on suspicion of spying for Russia."),
    ("FRANCE", "French police officers sentenced for beating music producer Michel Zecler."),
    ("FRANCE", "France seeks arrest warrants over an Iran-blamed fridge hack."),
    ("FRANCE", "Gerard Depardieu and a French author investigated over sexual allegations."),
    ("SUDAN", "Ex-official Ahmed Haroun, wanted by the ICC, arrested."),
    ("EL SALVADOR", "Salvadoran soldiers killed in an attack, officials say."),
    ("SPACE", "BepiColombo enters Mercury orbit at 19:24 CET after an 8-year ESA/JAXA journey."),
    ("SPACE", "BepiColombo's two orbiters, MPO and Mio, to split in December; science starts in April."),
    ("JAPAN", "Sagawa Express data leak reported."),
    ("JAPAN", "KKR in talks over CoCo Ichibanya."),
]

# (region tag, one-line headline) - brief band, 54 items
BRIEF = [
    ("SPORT", "Harden 51 pts; Cavs 128-119, passes Kobe"),
    ("SPORT", "Verstappen on pole in Vegas; Antonelli fastest"),
    ("SPORT", "India 486-4, lead NZ by 118; Rahul 136"),
    ("SPORT", "England record rugby win over New Zealand"),
    ("SPORT", "Wales beat All Blacks, first time in 73 yrs"),
    ("SPORT", "Chaudhary downs England in tetchy first T20"),
    ("SPORT", "Cummins keeps Australia Test captaincy"),
    ("SPORT", "Lehmann again denies sandpapergate knowledge"),
    ("SPORT", "India A beat Nepal by 306 runs; Nepal 26"),
    ("SPORT", "Kane tears ankle ligament, out for months"),
    ("SPORT", "Ronaldo scores 986th goal, misses penalty"),
    ("SPORT", "Pochettino set for Man Utd debut vs Liverpool"),
    ("SPORT", "ATP Finals semis; Andreeva wins WTA Finals"),
    ("SPORT", "Drake Maye out for season, fractured fibula"),
    ("SPORT", "Cade Cunningham posts historic 50-pt game"),
    ("SPORT", "Raptors upset Pistons"),
    ("SPORT", "Stars beat Golden Knights 4-3 in shootout"),
    ("SPORT", "F1 to return to V8 power in 2030"),
    ("SPORT", "Jon Henricks, 1956 swim champ, dies at 91"),
    ("SPORT", "England call up McKinney for SA Tests"),
    ("SPORT", "Khawaja in ball-tampering dispute"),
    ("SPORT", "Yankees release Gil"),
    ("CULTURE", "GTA VI: $3.79bn day one, biggest launch ever"),
    ("CULTURE", "GTA VI: Sensor Tower puts it at $2.36bn"),
    ("CULTURE", "'Sunrise on the Reaping' takes $51m Friday"),
    ("CULTURE", "'Wicked: For Good' opens, tracking $125m"),
    ("CULTURE", "Holmes documentary crosses $100m worldwide"),
    ("CULTURE", "Olivia Rodrigo's 'Stupid Song' hits No.1"),
    ("CULTURE", "Taylor Swift named Intl Artist of the Year"),
    ("CULTURE", "CMA Awards ratings reported"),
    ("CULTURE", "Culkin returns for new 'Home Alone' sequel"),
    ("CULTURE", "GTA VI cast revealed: Rourke is Jason"),
    ("TECH", "Anthropic slides after record IPO; AI unwinds"),
    ("TECH", "Microsoft retiring To Do app"),
    ("TECH", "Trump threatens ban on US AI centres abroad"),
    ("TECH", "Mitsui Shopping Park app pulled"),
    ("TECH", "CVN-81 carrier keeps Doris Miller's name"),
    ("TECH", "US Army pauses Iowa chemical detonation"),
    ("HEALTH", "US loses measles-free status as cases surge"),
    ("HEALTH", "Thanksgiving dinner costs higher this year"),
    ("WEATHER", "Fukushima snow outage reported"),
    ("UK", "Scouts face 1M GBP tourist tax on trips"),
    ("USA", "Democrats nominate Hakeem Jeffries for Speaker"),
    ("USA", "Congress resists $50bn air-travel rebuild plea"),
    ("USA", "Sarah McBride elected to leadership"),
    ("USA", "Ken Paxton drops lawsuits"),
    ("USA", "Tulip Siddiq takes legal action"),
    ("USA", "Chicago: mayor ballot fight; CFO resigns"),
    ("USA", "Two shot dead in Chicago's Noble Square"),
    ("PHILIPPINES", "Michelle Dee quits MGI All Stars"),
    ("PHILIPPINES", "DOTr eyes barrier-less tollways pilot"),
    ("INDIA", "Amit Shah on Siang Dam dialogue"),
    ("INDIA", "MEA clears Pakistani delegation's Taj visit"),
    ("EUROPE", "Cost-of-living protests sweep across Europe"),
]

TIMELINE = [
    ("00:09 UTC", "M6.7 quake in central Peru; felt in Lima"),
    ("MORNING", "3 Houthi missiles downed over Riyadh"),
    ("08:00 UTC", "GTA VI at $2.36bn, 24.58m copies"),
    ("DAY", "COP31 talks run past deadline in Antalya"),
    ("18:24 UTC", "BepiColombo enters Mercury orbit"),
    ("EVENING", "Cartel boss 'Chapo Isidro' captured"),
]

QUOTE = '"Putin is a killer." - Zelenskyy, Kyiv, 21 Nov (BBC)'

NON_REGIONS = {"SPORT", "CULTURE", "TECH", "HEALTH", "WEATHER", "SPACE"}


def count_stories():
    return len(STORIES) + len(BRIEF) + len(MARKETS)


def count_regions():
    tags = []
    for tag, _ in STORIES + BRIEF:
        if tag not in NON_REGIONS and tag not in tags:
            tags.append(tag)
    return len(tags), tags


def region_tally():
    counts = {}
    order = []
    for tag, _ in STORIES + BRIEF:
        if tag in NON_REGIONS:
            continue
        if tag not in counts:
            counts[tag] = 0
            order.append(tag)
        counts[tag] += 1
    ranked = sorted(order, key=lambda t: (-counts[t], t))
    return [(t, counts[t]) for t in ranked]

# ---------------------------------------------------------------- layout
MX = 16            # margin
CW = 992           # content width
COLW = 322         # column width
COLX = [16, 352, 688]


def section_bar(y, title, right=""):
    rect(MX, y, CW, 18, INK)
    draw_text(MX + 6, y + 5, title, 1, PAPER)
    if right:
        w = text_width(right, 1)
        draw_text(MX + CW - 6 - w, y + 5, right, 1, PAPER)
    return y + 18


def draw_masthead(n_stories, n_regions):
    # top rules
    hline(MX, 6, CW, INK, 2)
    draw_text_center(512, 14, "THE WORLD", 9, INK)
    # side ornaments
    draw_text(MX + 2, 30, "EST.", 1, SOFT)
    draw_text(MX + 2, 40, "MMXXVI", 1, SOFT)
    draw_text(MX + CW - 44, 30, "No. 325", 1, SOFT)
    draw_text(MX + CW - 44, 40, "SAT EDN", 1, SOFT)
    dateline = "SATURDAY, 21 NOVEMBER 2026  |  %d STORIES  -  %d REGIONS  -  ONE DAY" % (
        n_stories, n_regions)
    draw_text_center(512, 76, dateline, 1, DARKRED)
    hline(MX, 90, CW, INK, 2)
    hline(MX, 93, CW, INK, 1)


def draw_hero(x, y, w, h, kicker, headline, deck, accent):
    rect(x, y, w, h, CARD)
    border(x, y, w, h, INK, 1)
    rect(x, y, w, 16, accent)
    draw_text(x + 6, y + 4, kicker, 1, WHITE)
    # headline, scale 3, wrapped to fit
    lines = wrap(headline, (w - 12) // 18)
    yy = y + 22
    for ln in lines:
        draw_text(x + 6, yy, ln, 3, INK)
        yy += 22
    # red rule under headline
    hline(x + 6, yy + 1, w - 12, RED, 2)
    draw_wrapped(x + 6, yy + 7, deck, 1, SOFT, (w - 12) // 6, 9)


def draw_markets(y):
    draw_text(MX, y, "MARKETS - FRIDAY CLOSE: THE WORST WEEK SINCE APRIL 2025", 1, DARKRED)
    draw_text(MX + CW - text_width("ALL THREE MAJOR INDEXES IN CORRECTION", 1), y,
              "ALL THREE MAJOR INDEXES IN CORRECTION", 1, SOFT)
    chip_w = (CW - 3 * 8) // 4
    chip_h = 20
    for i, (label, val, chg) in enumerate(MARKETS):
        cx = MX + (i % 4) * (chip_w + 8)
        cy = y + 12 + (i // 4) * (chip_h + 4)
        rect(cx, cy, chip_w, chip_h, CARD)
        border(cx, cy, chip_w, chip_h, RULE, 1)
        draw_text(cx + 5, cy + 3, label, 1, SOFT)
        draw_text(cx + 5, cy + 11, val, 1, INK)
        wchg = text_width(chg, 1)
        draw_text(cx + chip_w - 5 - wchg, cy + 11, chg, 1, RED)


def draw_main_item(x, y, tag, headline):
    """One grid item: red tag + headline, exactly 2 lines, 19px tall."""
    full = tag + ": " + headline
    lines = wrap(full, COLW // 6)
    # safety: trim words until it fits in 2 lines
    while len(lines) > 2:
        headline = headline.rsplit(" ", 1)[0] + "..."
        full = tag + ": " + headline
        lines = wrap(full, COLW // 6)
    tag_txt = tag + ": "
    tw = text_width(tag_txt, 1)
    draw_text(x, y, tag_txt, 1, RED)
    rest = lines[0][len(tag_txt):]
    draw_text(x + tw, y, rest, 1, INK)
    if len(lines) > 1:
        draw_text(x, y + 9, lines[1], 1, INK)
    return y + 19


def draw_brief_item(x, y, tag, headline):
    full = tag + ": " + headline
    if text_width(full, 1) > COLW:
        # trim headline to fit one line
        while text_width(full, 1) > COLW and len(headline) > 4:
            headline = headline[:-4] + "..."
            full = tag + ": " + headline
    tag_txt = tag + ": "
    tw = text_width(tag_txt, 1)
    draw_text(x, y, tag_txt, 1, RED)
    draw_text(x + tw, y, full[len(tag_txt):], 1, INK)
    return y + 8


def draw_timeline(y):
    rect(MX, y, CW, 46, LIGHT)
    border(MX, y, CW, 46, RULE, 1)
    draw_text(MX + 6, y + 3, "THE DAY IN UTC", 1, BLUE)
    # timeline dots + labels, two rows of three; trim events to fit the column
    for i, (t, ev) in enumerate(TIMELINE):
        col = i % 3
        row = i // 3
        tx = MX + 10 + col * 330
        ty = y + 15 + row * 15
        rect(tx, ty + 1, 5, 5, RED)
        ttxt = t + "  "
        draw_text(tx + 9, ty, ttxt, 1, BLUE)
        max_ev = (330 - 9 - text_width(ttxt, 1)) // 6
        while len(ev) > max_ev and len(ev) > 4:
            ev = ev[:-4] + "..."
        draw_text(tx + 9 + text_width(ttxt, 1), ty, ev, 1, INK)


def draw_tally(y, tally):
    # join "TAG n" items atomically so no item is split across lines
    items = ["%s %d" % (t, c) for t, c in tally]
    lines = []
    cur = "REGION TALLY:  "
    for it in items:
        sep = "" if cur.endswith("  ") else ", "
        if len(cur) + len(sep) + len(it) <= CW // 6:
            cur = cur + sep + it
        else:
            lines.append(cur)
            cur = it
    lines.append(cur)
    yy = y
    for ln in lines:
        draw_text(MX, yy, ln, 1, SOFT)
        yy += 9
    return yy


def draw_quote(y):
    rect(MX, y, CW, 24, BLUE)
    draw_text_center(512, y + 5, QUOTE, 2, WHITE)
    return y + 24


def draw_footer(y, n_stories, n_regions):
    hline(MX, y, CW, INK, 1)
    draw_text(MX, y + 5,
              "DATE CHECK: every item first reported Sat 21 Nov 2026. Friday-close markets and",
              1, SOFT)
    draw_text(MX, y + 14,
              "Friday-night events as carried in Saturday's wires. Items from other dates excluded.",
              1, SOFT)
    draw_text(MX, y + 23,
              "SOURCES: AP - REUTERS - BBC - CNN - AFP - USGS - ESA - SCHWAB - ARAB NEWS - GMA - HT - NY POST",
              1, SOFT)
    right = "%d STORIES - %d REGIONS" % (n_stories, n_regions)
    draw_text(MX + CW - text_width(right, 1), y + 5, right, 1, DARKRED)
    draw_text(MX + CW - text_width("THE WORLD - 21 NOV 2026", 1), y + 23,
              "THE WORLD - 21 NOV 2026", 1, DARKRED)


def build():
    n_stories = count_stories()
    n_regions, _tags = count_regions()
    tally = region_tally()
    fill(PAPER)

    draw_masthead(n_stories, n_regions)

    # hero row
    hy, hh = 100, 116
    accents = [DARKRED, BLUE, GOLD]
    for i, (kicker, head, deck) in enumerate(HEROES):
        draw_hero(COLX[i], hy, COLW, hh, kicker, head, deck, accents[i])

    # markets strip
    draw_markets(224)

    # main grid
    y = section_bar(288, "THE WORLD IN BRIEF - TOP STORIES",
                    "%d STORIES" % len(STORIES))
    gy = y + 6
    per_col = (len(STORIES) + 2) // 3
    for ci in range(3):
        yy = gy
        for item in STORIES[ci * per_col:(ci + 1) * per_col]:
            yy = draw_main_item(COLX[ci], yy, item[0], item[1])
    grid_bottom = gy + per_col * 19

    # brief band
    y = section_bar(grid_bottom + 6, "THE DAY IN BRIEF - SPORT, CULTURE, TECH & MORE",
                    "%d ITEMS" % len(BRIEF))
    by = y + 5
    per_col_b = (len(BRIEF) + 2) // 3
    for ci in range(3):
        yy = by
        for item in BRIEF[ci * per_col_b:(ci + 1) * per_col_b]:
            yy = draw_brief_item(COLX[ci], yy, item[0], item[1])
    brief_bottom = by + per_col_b * 8

    # timeline, tally, quote, footer
    ty = brief_bottom + 6
    draw_timeline(ty)
    ty2 = draw_tally(ty + 52, tally)
    qy = draw_quote(ty2 + 4)
    draw_footer(qy + 4, n_stories, n_regions)

    return n_stories, n_regions


def main():
    n_stories, n_regions = build()
    data = png_bytes()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    with open(out, "wb") as f:
        f.write(data)
    md5 = hashlib.md5(data).hexdigest()
    print("stories=%d regions=%d size=%d md5=%s out=%s"
          % (n_stories, n_regions, len(data), md5, out))


if __name__ == "__main__":
    main()
