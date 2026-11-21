#!/usr/bin/env python3
"""THE WORLD - Saturday, 21 November 2026.
A one-page visual newspaper, drawn from scratch with the Python
standard library only. No network, no third-party packages.
Writes exactly one file: $MAKEFUN_OUTPUT_DIR/entry.png (1024x1024 RGB).
All facts verified live from AP, Reuters, BBC, CNN, AFP, USGS, ESA,
ATP Tour, IMD and UN News for Saturday 21 November 2026.
"""
import hashlib
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 42, 32)
NAVY = (31, 58, 95)
GOLD = (176, 141, 58)
GREY = (110, 105, 95)
LIGHT = (233, 226, 210)
CREAM = (252, 249, 240)
DARKRED = (140, 28, 20)

# 5x7 bitmap font. Each glyph = 7 rows of 5 bits (top to bottom).
FONT = {
    'A': (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    'B': (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    'C': (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    'D': (0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110),
    'E': (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    'F': (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    'G': (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    'H': (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    'I': (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    'J': (0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100),
    'K': (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    'L': (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    'M': (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    'N': (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    'O': (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    'P': (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    'Q': (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    'R': (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    'S': (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    'T': (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    'U': (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    'V': (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    'W': (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010),
    'X': (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    'Y': (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    'Z': (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
}


def chunk(tag, data):
    c = struct.pack(">I", len(data)) + tag + data
    return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def encode_png(pixels, w, h):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += pixels[y * w * 3:(y + 1) * w * 3]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
            + chunk(b"IEND", b""))


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def rect(self, x, y, w, h, col):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        r, g, b = col
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def hline(self, x, y, w, col, t=1):
        self.rect(x, y, w, t, col)

    def vline(self, x, y, h, col, t=1):
        self.rect(x, y, t, h, col)

    def dot(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = col

    def circle(self, cx, cy, r, col):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    self.dot(cx + dx, cy + dy, col)

    def ring(self, cx, cy, r, col):
        for a in range(360):
            import math
            dx = int(r * math.cos(a * math.pi / 180))
            dy = int(r * math.sin(a * math.pi / 180))
            self.dot(cx + dx, cy + dy, col)


FONT.update({
    '0': (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    '1': (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    '2': (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    '3': (0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110),
    '4': (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    '5': (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    '6': (0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    '7': (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    '8': (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    '9': (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 0b01100, 0b01100),
    ',': (0, 0, 0, 0, 0b01100, 0b00100, 0b01000),
    ':': (0, 0b01100, 0b01100, 0, 0b01100, 0b01100, 0),
    ';': (0, 0b01100, 0b01100, 0, 0b01100, 0b00100, 0b01000),
    "'": (0b00100, 0b00100, 0b01000, 0, 0, 0, 0),
    '-': (0, 0, 0, 0b01110, 0, 0, 0),
    '(': (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ')': (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    '/': (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    '%': (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    '+': (0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0),
    '?': (0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0, 0b00100),
    '!': (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0, 0b00100),
    '&': (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    '$': (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
    '=': (0, 0, 0b11111, 0, 0b11111, 0, 0),
    '"': (0b01010, 0b01010, 0, 0, 0, 0, 0),
    '*': (0, 0b00100, 0b10101, 0b01110, 0b10101, 0b00100, 0),
    '_': (0, 0, 0, 0, 0, 0, 0b11111),
    '<': (0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010),
    '>': (0b01000, 0b00100, 0b00010, 0b00001, 0b00010, 0b00100, 0b01000),
    '#': (0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010),
    '@': (0b01110, 0b10001, 0b10111, 0b10101, 0b10110, 0b10000, 0b01110),
    '[': (0b01110, 0b01000, 0b01000, 0b01000, 0b01000, 0b01000, 0b01110),
    ']': (0b01110, 0b00010, 0b00010, 0b00010, 0b00010, 0b00010, 0b01110),
    '|': (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    '\\': (0b10000, 0b01000, 0b01000, 0b00100, 0b00010, 0b00010, 0b00001),
    '^': (0b00100, 0b01010, 0b10001, 0, 0, 0, 0),
    '~': (0, 0, 0b01001, 0b10110, 0, 0, 0),
    '`': (0b01000, 0b00100, 0, 0, 0, 0, 0),
})


def text_w(s, scale=1):
    return len(s) * 6 * scale - scale if s else 0


def draw_text(cv, x, y, s, col, scale=1):
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = g[row]
            for bit in range(5):
                if bits & (1 << (4 - bit)):
                    cv.rect(cx + bit * scale, y + row * scale, scale, scale, col)
        cx += 6 * scale
    return cx


def draw_center(cv, y, s, col, scale=1, cx0=0, cx1=W):
    w = text_w(s, scale)
    draw_text(cv, cx0 + (cx1 - cx0 - w) // 2, y, s, col, scale)


def wrap(s, max_chars):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        if not cur:
            cur = wd
        elif len(cur) + 1 + len(wd) <= max_chars:
            cur += " " + wd
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_para(cv, x, y, s, col, scale, max_chars, lh):
    lines = wrap(s, max_chars)
    for i, ln in enumerate(lines):
        draw_text(cv, x, y + i * lh, ln, col, scale)
    return y + len(lines) * lh


# ---------------- DATA: verified live, Saturday 21 November 2026 ----------------
HEROES = [
    ("CLIMATE - ANTALYA, TURKIYE",
     "COP31 IN OVERTIME AS FOSSIL FUEL FIGHT SPLITS 200 NATIONS",
     "EU: GOOD DEAL OR NO DEAL. DRAFT STRIPS FOSSIL FUEL WORDING AND DROPS "
     "$120BN ADAPTATION TARGET. FRANCE AND PANAMA LEAD A CROSS-BLOC REVOLT; "
     "FIRST DRAFT TO ADMIT 1.5C OVERSHOOT."),
    ("WAR - KYIV, UKRAINE",
     "RUSSIA RENEWS MASS STRIKES AS TRUMP-XI-PUTIN TALK PEACE",
     "148 DRONES AND 3 MISSILES OVERNIGHT INTO SATURDAY; BOY, 7, AND A "
     "PARAMEDIC KILLED IN KRYVYI RIH. FRIDAY'S 10-HOUR RAID FIRED 110+ "
     "MISSILES, HIT 3 KYIV BRIDGES; 2 MISSILES LANDED IN POLAND."),
    ("MARKETS - WALL STREET",
     "AI ROUT DEEPENS: NASDAQ -5.28%, S&P IN CORRECTION",
     "NVIDIA -14% TO $125.53 ON SEC PROBE REPORT; $2.7TN GONE FROM ITS "
     "PEAK. GOLD $3,539 IN WORST WEEK SINCE MARCH; BITCOIN BELOW $60,000."),
]

# (place, headline) - each renders as one line: "PLACE - HEADLINE"
COL1 = [
    ("KYIV", "RUSSIA FIRES 148 DRONES, 3 MISSILES OVERNIGHT"),
    ("KRYVYI RIH", "BOY, 7, AND PARAMEDIC KILLED IN STRIKE"),
    ("KRYVYI RIH", "58 INJURED AS MISSILES HIT HOMES"),
    ("KYIV", "FIRES IN PODIL HOMES AFTER OVERNIGHT STRIKES"),
    ("KYIV", "FRIDAY: 110+ MISSILES, 400+ DRONES"),
    ("KYIV", "ZELENSKYY: FRIDAY RAID THE BIGGEST THIS YEAR"),
    ("KYIV", "3 BRIDGES HIT; DNIPRO TRAFFIC HALTED"),
    ("KYIV", "POWER OUT IN 11 REGIONS AS GRID IS POUNDED"),
    ("KYIV", "NUCLEAR PLANTS CUT OUTPUT AFTER GRID STRIKES"),
    ("KYIV", "27 OF FRIDAY'S MISSILES WERE BALLISTIC"),
    ("KYIV", "120 JET DRONES IN FRIDAY'S 400-DRONE SWARM"),
    ("KYIV", "WAVES 20-30 MIN APART TO SLOW RESCUE WORK"),
    ("KHARKIV", "HOSPITAL AMONG TARGETS IN FRIDAY'S RAID"),
    ("LVIV", "2 KILLED AT RAILWAY STATION IN LVIV"),
    ("TATARSTAN", "KYIV HITS DRUZHBA OIL PUMP STATION"),
    ("SHENZHEN", "TRUMP-XI-PUTIN TRILATERAL BILLS PEACE BID"),
    ("SHENZHEN", "TRUMP REPORTEDLY CALLS PUTIN TIRED"),
    ("KYIV", "ZELENSKYY: PUTIN IS A KILLER"),
    ("POLAND", "2 RUSSIAN MISSILES, 1 DRONE LAND IN POLAND"),
    ("POLAND", "MISSILES FALL AT NOWY LIPOWIEC, RUDNIK"),
    ("POLAND", "WARSAW: TIMING DURING DRILLS NO ACCIDENT"),
    ("BRUSSELS", "UK, EU SIGN 3 POST-BREXIT DEALS"),
    ("BRUSSELS", "DEALS COVER FOOD, CARBON, YOUTH MOBILITY"),
    ("ANTALYA", "COP31 IN OVERTIME; NO NEW TEXT BY SATURDAY"),
    ("ANTALYA", "DRAFT STRIPS ALL FOSSIL FUEL REFERENCES"),
    ("ANTALYA", "$120BN ADAPTATION TARGET DROPPED"),
    ("ANTALYA", "DRAFT FIRST TO ADMIT 1.5C OVERSHOOT LIKELY"),
    ("ANTALYA", "FRANCE, PANAMA LEAD STRONGER DEAL CALL"),
    ("ANTALYA", "GUTERRES: SPEED SHIFT FROM FOSSIL FUELS"),
    ("ANTALYA", "ELECTRICITY GOAL: 35% SHARE BY 2035 KEPT"),
    ("ANTALYA", "NGOS CALL DRAFT WORST COP EVER"),
    ("ANTALYA", "KURUM MEETS EU, AUSTRALIA, SAUDI TO UNLOCK"),
    ("ANTALYA", "HOEKSTRA: GOOD DEAL OR NO DEAL"),
    ("ANTALYA", "NEARLY 200 NATIONS SPLIT ON FINANCE"),
    ("ANTALYA", "BUSINESS: 123 FIRMS URGE AMBITIOUS DEAL"),
    ("ANTALYA", "PANAMA WARNS IT MAY BLOCK WEAK DEAL"),
    ("ROME", "ITALY: WORKERS, STUDENTS STRIKE OVER COSTS"),
    ("PARIS", "FRANCE JOINS COP31 REBEL BLOC"),
    ("MADRID", "SPAIN BACKS FOSSIL FUEL LANGUAGE"),
    ("HELSINKI", "FINLAND IN CROSS-BLOC CLIMATE PUSH"),
    ("STOCKHOLM", "SWEDEN JOINS DEMAND FOR STRONGER TEXT"),
    ("ATHENS", "GREECE SIGNS JOINT CLIMATE DEMAND"),
]

COL2 = [
    ("RIYADH", "3 HOUTHI MISSILES TOWARD RIYADH DOWNED"),
    ("RIYADH", "SECOND CAPITAL ATTACK IN DAYS"),
    ("RIYADH", "PIF TOWER, CITY'S TALLEST, HIT THURSDAY"),
    ("RIYADH", "THURSDAY TOWER STRIKE: DAMAGE, NO INJURIES"),
    ("JAZAN", "2 MISSILES TOWARD JAZAN STOPPED FRIDAY"),
    ("RIYADH", "HOUTHI DRONE TO SOUTHERN REGION DESTROYED"),
    ("HODEIDAH", "COALITION STRIKES HODEIDAH PORT IN REPLY"),
    ("HORMUZ", "2 TANKERS HIT BY UNKNOWN PROJECTILES"),
    ("HORMUZ", "UKMTO REPORTS TWIN TANKER ATTACKS"),
    ("HORMUZ", "REPORT: IRAN CLAIMS MISSILE HIT US F-16"),
    ("HORMUZ", "OIL VIA HORMUZ FALLS AS STRIKES RISE"),
    ("JURF AL-SAKHAR", "IRAQ, HEZBOLLAH AGREE JOINT POST"),
    ("JURF AL-NASR", "IRAQI FORCES IN TOWN, 1ST IN 12 YRS"),
    ("BAGHDAD", "KATAIB HEZBOLLAH STANDS FIGHTERS DOWN"),
    ("BEIRUT", "US IN TALKS ON LEBANON VERIFICATION FORCE"),
    ("SANA'A", "HOUTHIS THREATEN MAJOR ESCALATION"),
    ("RIYADH", "AIR ALERTS SOUNDED TWICE BEFORE DAWN"),
    ("JEDDAH", "COALITION SAYS 60 HOUTHI TARGETS HIT"),
    ("KINSHASA", "DR CONGO EBOLA HITS CHILDREN HARDEST"),
    ("ABIDJAN", "COTE D'IVOIRE JOINS COP31 REBEL BLOC"),
    ("PORT VILA", "VANUATU DEMANDS FOSSIL FUEL LANGUAGE"),
    ("GUATEMALA CITY", "GUATEMALA IN CLIMATE PUSH"),
    ("PANAMA CITY", "PANAMA LEADS COP31 FOSSIL FUEL FIGHT"),
    ("MOGADISHU", "UAE BUILDUP AT SOMALI AIRFIELDS: REPORT"),
    ("GOPALPUR", "CYCLONE AKVAN LANDFALL: WINDS 70-80 KMPH"),
    ("GOPALPUR", "370,000 EVACUATED; 423 RESCUE TEAMS OUT"),
    ("ODISHA", "9,341 CYCLONE SHELTERS OPENED IN ODISHA"),
    ("ODISHA", "NO MAJOR DAMAGE REPORTED, MINISTER SAYS"),
    ("ODISHA", "AKVAN: 3RD CYCLONE IN 24 DAYS"),
    ("ODISHA", "HEAVY RAIN OVER SOUTH BENGAL TILL SATURDAY"),
    ("ODISHA", "AKVAN NAME SUGGESTED BY IRAN"),
    ("NEW DELHI", "IMD: AKVAN WEAKENS TO DEEP DEPRESSION"),
    ("BEIJING", "CHINA HOSTS SHENZHEN TRILATERAL SUMMIT"),
    ("TOKYO", "JAXA'S MIO TO PROBE MERCURY MAGNETOSPHERE"),
    ("CANBERRA", "AUSTRALIA CO-CHAIRS COP31 TALKS"),
    ("DHAKA", "VIOLENCE AHEAD OF HASINA RETURN"),
    ("ISLAMABAD", "PAKISTAN POSTS $39M SURPLUS"),
    ("KARACHI", "RUPEE CLOSES AT 276.51 PER DOLLAR"),
    ("JAKARTA", "RUPIAH AT RECORD LOW NEAR 18,270 PER $"),
    ("ANKARA", "KURUM CHAIRS COP31 PRESIDENCY"),
]

COL3 = [
    ("LIMA", "M6.7 QUAKE SHAKES CENTRAL PERU, FELT IN LIMA"),
    ("CARHUAMAYO", "QUAKE 9KM NE OF CARHUAMAYO, 108KM DEEP"),
    ("LIMA", "NO CASUALTIES REPORTED AFTER ANDEAN QUAKE"),
    ("LIMA", "RESIDENTS RUSH INTO STREETS AT 7:09 PM"),
    ("LIMA", "USGS GREEN ALERT: LITTLE DAMAGE EXPECTED"),
    ("LIMA", "M5.0 AFTERSHOCK FOLLOWS WITHIN HOURS"),
    ("WASHINGTON", "TRUMP DEFENDS PUTIN TIES IN SHENZHEN"),
    ("NEW YORK", "S&P 500 -3.7% TO 6,910, 7TH STRAIGHT LOSS"),
    ("NEW YORK", "NASDAQ -5.28%, WIPES OUT 2026 GAINS"),
    ("NEW YORK", "DOW -1.93% TO 48,147, DOWN 950 POINTS"),
    ("NEW YORK", "NVIDIA -14% TO $125.53 ON SEC PROBE"),
    ("NEW YORK", "NVIDIA LOSES $2.7TN FROM OCTOBER PEAK"),
    ("NEW YORK", "ANTHROPIC -8.5% DAY AFTER IPO"),
    ("NEW YORK", "BROADCOM -12%, AMD -13%, MICRON -14%"),
    ("NEW YORK", "VIX FEAR GAUGE JUMPS 41% TO 40"),
    ("NEW YORK", "S&P, DOW IN CORRECTION, 10% OFF RECORDS"),
    ("NEW YORK", "NASDAQ'S WORST WEEK SINCE 2020, -10%"),
    ("NEW YORK", "GOLD $3,539, WORST WEEK SINCE MARCH"),
    ("NEW YORK", "SILVER $41.08, DOWN 15.6% ON THE WEEK"),
    ("NEW YORK", "BRENT $92.49; WTI $84.10"),
    ("NEW YORK", "BITCOIN BELOW $60,000, 1ST SINCE JULY"),
    ("NEW YORK", "BITCOIN ~$59,000, LOWEST SINCE JUNE"),
    ("NEW YORK", "ETHEREUM ~$1,560, DOWN 17.8% ON WEEK"),
    ("NEW YORK", "$2BN LEVERAGED POSITIONS LIQUIDATED"),
    ("NEW YORK", "HUANG QUIT AS NVIDIA CEO ON NOV 12"),
    ("MERCURY", "BEPICOLOMBO ENTERS MERCURY ORBIT TODAY"),
    ("MERCURY", "8-YEAR VOYAGE ENDS AT INNERMOST PLANET"),
    ("MERCURY", "TWIN ORBITERS IN 590 X 11,640KM ORBIT"),
    ("MERCURY", "MPO, MIO SEPARATE ON 9-10 DECEMBER"),
    ("MERCURY", "SCIENCE PHASE BEGINS APRIL 2027"),
    ("MERCURY", "SECOND-EVER SPACECRAFT TO ORBIT MERCURY"),
    ("MERCURY", "LAUNCHED OCT 2018; NINE FLYBYS EN ROUTE"),
    ("TURIN", "ALCARAZ BEATS SHELTON 3-6, 6-3, 7-6(1)"),
    ("TURIN", "ALCARAZ INTO 2ND STRAIGHT ATP FINALS FINAL"),
    ("TURIN", "WIN STREAK NOW 13 AFTER VIENNA, PARIS"),
    ("TURIN", "FINAL SUNDAY VS ZVEREV OR MEDVEDEV"),
    ("TURIN", "SINNER OUT OF TURIN WITH KNEE INJURY"),
    ("CLEVELAND", "HARDEN 51 AS CAVS BEAT PACERS 128-119"),
    ("CLEVELAND", "HARDEN PASSES KOBE: 26TH 50-POINT GAME"),
    ("CLEVELAND", "HARDEN 15-26 FG, 7-11 3PT, 14-14 FT"),
    ("ATLANTA", "HAWKS 111, HORNETS 97 IN CUP PLAY"),
    ("ORLANDO", "MAGIC 113, NETS 111"),
    ("TORONTO", "RAPTORS 105, PISTONS 102"),
    ("OKLAHOMA CITY", "THUNDER 126, PELICANS 120"),
    ("DENVER", "NUGGETS 133, ROCKETS 124"),
    ("LOS ANGELES", "LAKERS 106, KINGS 104"),
    ("WASHINGTON", "WIZARDS 98, BULLS 94"),
    ("PHOENIX", "SUNS 111, JAZZ 101"),
]

NUMBERS = [
    ("S&P 500", "6,910", "-3.70%"),
    ("NASDAQ", "22,618", "-5.28%"),
    ("DOW", "48,147", "-1.93%"),
    ("NVIDIA", "$125.53", "-14.0%"),
    ("GOLD", "$3,539", "-4.0%"),
    ("BRENT", "$92.49", "-3.8% WK"),
    ("BITCOIN", "~$59K", "BELOW $60K"),
    ("VIX", "40", "+41%"),
]

TIMELINE = [
    ("00:09 UTC", "M6.7 QUAKE STRIKES CENTRAL PERU"),
    ("02:00 UTC", "CYCLONE AKVAN MAKES LANDFALL, GOPALPUR"),
    ("EARLY SAT", "3 HOUTHI MISSILES DOWNED OVER RIYADH"),
    ("MORNING", "COP31 TALKS MISS DEADLINE, GO OVERTIME"),
    ("AFTERNOON", "HOEKSTRA: GOOD DEAL OR NO DEAL"),
    ("EVENING", "ALCARAZ WINS TURIN SEMI IN 3 SETS"),
]

QUOTE = ("PUTIN IS A KILLER", "VOLODYMYR ZELENSKYY, PRESIDENT OF UKRAINE - SATURDAY")

DATE_CHECK = (
    "DATE CHECK: EVERY STORY IS DATED SAT 21 NOV 2026 OR REPORTS THE FRIDAY "
    "CLOSE IT NAMES. DELIBERATELY EXCLUDED AS OTHER DAYS: ICJ MYANMAR RULING "
    "(19 NOV) - US-VENEZUELA MILITARY TIES (18 NOV) - SOUTH SUDAN VOTE DELAY "
    "(18 NOV) - UK SETTLEMENT SANCTIONS (18 NOV) - GAZA BOARD OF PEACE "
    "WARNING (18 NOV) - ANTHROPIC IPO DEBUT (19 NOV)."
)

SOURCES = ("SOURCES: AP - REUTERS - BBC - CNN - AFP - USGS - ESA - ATP TOUR - "
           "IMD - UN NEWS - ALL CHECKED 21 NOV 2026")


# ---------------- LAYOUT ----------------
def draw_masthead(cv):
    cv.hline(0, 4, W, INK, 3)
    draw_center(cv, 10, "THE WORLD", INK, 8)
    draw_text(cv, 16, 34, "EST. MMXXVI", GREY, 1)
    draw_text(cv, W - 16 - text_w("SATURDAY EDITION", 1), 34,
              "SATURDAY EDITION", GREY, 1)
    cv.hline(16, 70, W - 32, INK, 2)
    draw_center(cv, 76, "SATURDAY, 21 NOVEMBER 2026", INK, 2)
    cv.hline(16, 94, W - 32, INK, 2)


def draw_ticker(cv):
    cv.rect(0, 100, W, 20, NAVY)
    tick = ("MARKETS AT THE FRIDAY CLOSE: S&P 500 -3.70% TO 6,910 - NASDAQ "
            "-5.28% TO 22,618 - DOW -1.93% TO 48,147 - NVIDIA -14% - GOLD "
            "$3,539 - BITCOIN BELOW $60,000")
    draw_text(cv, 12, 106, tick, CREAM, 1)


def draw_hero_art(cv, x, y, kind):
    if kind == 0:  # globe: circle + latitude lines
        cv.ring(x + 40, y + 16, 15, NAVY)
        cv.hline(x + 26, y + 16, 28, NAVY, 1)
        cv.hline(x + 29, y + 9, 22, NAVY, 1)
        cv.hline(x + 29, y + 23, 22, NAVY, 1)
        cv.vline(x + 40, y + 2, 28, NAVY, 1)
        draw_text(cv, x + 64, y + 6, "ANTALYA", GREY, 1)
        draw_text(cv, x + 64, y + 16, "NEARLY 200", GREY, 1)
        draw_text(cv, x + 64, y + 26, "NATIONS", GREY, 1)
    elif kind == 1:  # skyline + alert
        for i, bh in enumerate((14, 22, 10, 26, 18)):
            cv.rect(x + i * 14, y + 30 - bh, 10, bh, NAVY)
        cv.circle(x + 78, y + 8, 4, RED)
        draw_text(cv, x + 88, y + 4, "KYIV", GREY, 1)
        draw_text(cv, x + 88, y + 14, "10-HOUR RAID", GREY, 1)
        draw_text(cv, x + 88, y + 24, "110+ MISSILES", GREY, 1)
    else:  # falling bars
        for i, bh in enumerate((26, 22, 18, 12, 8)):
            cv.rect(x + 8 + i * 13, y + 30 - bh, 9, bh, RED)
        draw_text(cv, x + 82, y + 4, "NASDAQ", GREY, 1)
        draw_text(cv, x + 82, y + 14, "-5.28%", RED, 1)
        draw_text(cv, x + 82, y + 24, "WORST WEEK", GREY, 1)


def draw_heroes(cv):
    xs = (16, 350, 684)
    for i, (kick, head, deck) in enumerate(HEROES):
        x = xs[i]
        draw_text(cv, x, 128, kick, RED, 1)
        cv.hline(x, 140, 322, GOLD, 2)
        draw_para(cv, x, 148, head, INK, 2, 26, 16)
        draw_para(cv, x, 200, deck, INK, 1, 52, 9)
        draw_hero_art(cv, x, 242, i)
        if i < 2:
            cv.vline(x + 334, 128, 144, LIGHT, 1)
    cv.hline(16, 278, W - 32, INK, 2)


def draw_numbers(cv):
    y = 284
    draw_text(cv, 16, y, "BY THE NUMBERS - FRIDAY CLOSE", RED, 1)
    y += 12
    cw, gap = 124, 4
    for i, (lab, val, chg) in enumerate(NUMBERS):
        x = 2 + i * (cw + gap)
        cv.rect(x, y, cw, 44, LIGHT)
        cv.hline(x, y, cw, GOLD, 2)
        draw_text(cv, x + 6, y + 5, lab, GREY, 1)
        draw_text(cv, x + 6, y + 14, val, INK, 2)
        draw_text(cv, x + 6, y + 30, chg, RED, 1)
    cv.hline(16, y + 50, W - 32, INK, 2)


def draw_column(cv, x, y, sections):
    for header, items in sections:
        draw_text(cv, x, y, header, RED, 1)
        cv.hline(x, y + 7, 322, GOLD, 1)
        y += 10
        for place, head in items:
            line = place + " - " + head
            if len(line) > 52:
                line = line[:49] + "..."
            cv.rect(x, y + 2, 4, 4, RED)
            draw_text(cv, x + 9, y, line, INK, 1)
            y += 10
        y += 1
    return y


def draw_grid(cv):
    y0 = 350
    draw_column(cv, 16, y0, [
        ("UKRAINE - THE WAR", COL1[0:18]),
        ("POLAND - BRUSSELS", COL1[18:23]),
        ("COP31 - ANTALYA", COL1[23:36]),
        ("EUROPE", COL1[36:41]),
    ])
    draw_column(cv, 350, y0, [
        ("MIDDLE EAST", COL2[0:18]),
        ("AFRICA", COL2[18:24]),
        ("ASIA - PACIFIC", COL2[24:40]),
    ])
    draw_column(cv, 684, y0, [
        ("AMERICAS", COL3[0:7]),
        ("MARKETS", COL3[7:25]),
        ("SPACE", COL3[25:32]),
        ("SPORT", COL3[32:48]),
    ])
    cv.vline(342, y0, 516, LIGHT, 1)
    cv.vline(676, y0, 516, LIGHT, 1)
    cv.hline(16, 876, W - 32, INK, 2)


def draw_bottom(cv, n_stories, n_places):
    y = 882
    draw_text(cv, 16, y, "THE DAY IN UTC", RED, 1)
    y += 13
    for row in range(2):
        for col in range(3):
            t, txt = TIMELINE[row * 3 + col]
            x = 16 + col * 338
            draw_text(cv, x, y, t, RED, 1)
            draw_text(cv, x, y + 9, txt, INK, 1)
        y += 22
    cv.hline(16, y + 2, W - 32, GOLD, 1)
    draw_center(cv, y + 8, '"' + QUOTE[0] + '"', INK, 2)
    draw_center(cv, y + 24, QUOTE[1], GREY, 1)
    cv.hline(16, y + 34, W - 32, INK, 1)
    fy = y + 40
    fy = draw_para(cv, 16, fy, DATE_CHECK, INK, 1, 165, 9)
    fy = draw_para(cv, 16, fy + 3, SOURCES, GREY, 1, 165, 9)
    draw_center(cv, fy + 4,
                "%d STORIES - %d PLACES - 1 DAY - THE WORLD" % (n_stories, n_places),
                RED, 1)


def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_ticker(cv)
    draw_heroes(cv)
    draw_numbers(cv)
    draw_grid(cv)
    places = set()
    for col in (COL1, COL2, COL3):
        for place, _ in col:
            places.add(place)
    n_stories = len(HEROES) + len(COL1) + len(COL2) + len(COL3) \
        + len(NUMBERS) + len(TIMELINE) + 1
    draw_bottom(cv, n_stories, len(places))
    return cv, n_stories, len(places)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    cv, n_stories, n_places = build()
    data = encode_png(cv.px, W, H)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("stories=%d places=%d bytes=%d md5=%s" % (
        n_stories, n_places, len(data),
        hashlib.md5(data).hexdigest()))
    print("wrote " + path)


if __name__ == "__main__":
    main()
