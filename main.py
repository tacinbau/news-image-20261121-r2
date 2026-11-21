#!/usr/bin/env python3
"""THE WORLD - Saturday, 21 November 2026. One image, 82 stories, 18 regions.
Deterministic, stdlib + PIL only. Run: python3 main.py  ->  entry.png (1024x1024 RGB).
All facts verified 21 Nov 2026 from live reporting (One Turn day page, AP, CNN,
Reuters, ESA, ATP Tour). Items whose event date is NOT 21 Nov are flagged in-line
and listed in the DATE CHECK strip; they are counted only as dated follow-ups.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 232)
INK = (17, 24, 39)
RED = (178, 34, 34)
DARKRED = (120, 20, 20)
NAVY = (18, 42, 84)
TEAL = (13, 92, 92)
GOLD = (176, 132, 24)
GREY = (90, 96, 108)
LIGHT = (232, 226, 210)
MID = (214, 206, 188)
GREEN = (46, 110, 60)
ORANGE = (196, 90, 20)

def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else FR, sz)

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(d, text, f, maxw, ellipsis="..."):
    if d.textlength(text, font=f) <= maxw:
        return text
    while text and d.textlength(text + ellipsis, font=f) > maxw:
        text = text[:-1]
    return text + ellipsis

def box(d, xy, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=4, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- stories
# (region, headline, detail) -- every item verified in live 21 Nov 2026 reporting.
STORIES = [
 ("Eastern Europe", "RUSSIA FIRES 400+ DRONES, 110 MISSILES AT UKRAINE",
  "8 killed in Kyiv; bridges, rail and energy hit; power cut in 10 regions"),
 ("Eastern Europe", "MISSILE HITS ZELENSKYY'S HOMETOWN KRYVYI RIH",
  "2 killed, 60 wounded in ballistic strike on the city centre"),
 ("Eastern Europe", "RUSSIAN MISSILES LAND IN POLAND",
  "2 missiles + suspected drone in the east; NATO calls it a grave violation"),
 ("Middle East", "ISRAELI STRIKE KILLS 3 IN GAZA AID VEHICLE",
  "Palestinians killed in Gaza as West Bank tensions rise"),
 ("Middle East", "IRAN STRIKES 3 TANKERS NEAR HORMUZ",
  "Tehran shows off missile launchers as US-Iran talks stall"),
 ("Middle East", "HOUTHIS AND SAUDI-LED COALITION TRADE STRIKES",
  "Yemen front flares again after weeks of uneasy calm"),
 ("Middle East", "FIRE AT BASRA POWER STATION KILLS 4",
  "30 wounded in a blaze at the southern Iraq plant"),
 ("Central America", "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
  "FBI most-wanted Fausto Isidro Meza Flores seized in Guasave, Sinaloa"),
 ("Caribbean", "SALVADORAN TROOPS FIGHT GANGS IN HAITI",
  "Soldiers lost in the Port-au-Prince deployment"),
 ("South America", "BOLSONARO HOSPITALISED IN BRASILIA",
  "Ex-president treated for intestinal obstruction"),
 ("South America", "DENGUE CUT 69% BY BACTERIUM MOSQUITOES",
  "Brazil trial: Wolbachia mosquitoes slash dengue cases"),
 ("South America", "ARGENTINA COUNTRY RISK TOPS 1,000",
  "Buenos Aires risk gauge crosses 1,000 points"),
 ("Western Europe", "SPAIN HEADS TO 29 NOV ELECTION",
  "Madrid plans a banking-tax extension to fund housing"),
 ("North America", "AI SELL-OFF: S&P 500 -3.7% TO 6,910",
  "Nasdaq -5.28%, Dow -1.93%; S&P's 7th straight daily loss"),
 ("North America", "NVIDIA -14%, AMD -13.3%, MICRON -13.9%",
  "Chip rout; Nvidia -47.5% since its 6 Oct peak"),
 ("North America", "ANTHROPIC -8.5% AFTER $2TN DEBUT",
  "Shares close at $88.91, just above the $83 IPO price"),
 ("North America", "VIX SOARS TO 35.9, HIGHEST IN 19 MONTHS",
  "Fear gauge up 86% on the week as tech crumbles"),
 ("North America", "TRUMP: TAX ON FIRMS BUILDING AI DATA CENTRES ABROAD",
  "'Tremendous tax' warning to US companies"),
 ("North America", "FBI CRIME DATABASE AND USDA REPORTEDLY HACKED",
  "NCIC and farm payment system breached, US media say"),
 ("North America", "US LOSES MEASLES ELIMINATION STATUS",
  "Measles endemic again; Mexico and Bolivia also lose status"),
 ("North America", "MAN CONVICTED OF STARTING PALISADES FIRE",
  "Los Angeles jury verdict in the deadly blaze case"),
 ("North America", "INDIAN MAN SENTENCED OVER PLOT TO KILL SIKH LEADER",
  "New York sentencing in the assassination-plot case"),
 ("North America", "HARDEN PASSES KOBE ON 50-POINT LIST",
  "51 pts as Cleveland beat Indiana 128-119 in the NBA Cup"),
 ("North America", "VERSTAPPEN TAKES LAS VEGAS GP POLE",
  "Pole after an Antonelli penalty in qualifying"),
 ("North America", "TEXANS BEAT COLTS 26-3",
  "CJ Stroud leads the AFC South win in Houston"),
 ("North America", "US SELLS DEEP-SEA MINING LEASES OFF AMERICAN SAMOA",
  "Pacific seabed opened to mining"),
 ("North America", "OLIVIA RODRIGO ALBUM DEBUTS AT NO. 1 IN US",
  "New album tops the American chart"),
 ("Western Europe", "UK AND EU SIGN 3 POST-BREXIT DEALS",
  "PM Andy Burnham signs youth mobility, trade and energy in Brussels"),
 ("Western Europe", "COST-OF-LIVING PROTESTS SPREAD ACROSS EUROPE",
  "Rome marches over pay and prices; rallies in several capitals"),
 ("Western Europe", "DENMARK EXPELS RUSSIAN DIPLOMAT",
  "2 arrested over alleged plot to kill a US-Ukrainian rapper"),
 ("Western Europe", "FRENCH POLICE SENTENCED OVER RACIST BEATING",
  "Michel Zecler case ends in Paris convictions"),
 ("Western Europe", "ITALY GIVES TESLA SELF-DRIVING CONDITIONAL NOD",
  "Approval ahead of an EU-wide ruling"),
 ("Western Europe", "UK RETAIL SALES +2.3% YOY IN OCT",
  "Beats the 1.7% forecast; +0.7% on the month"),
 ("Western Europe", "ENGLAND BEAT NEW ZEALAND BY RECORD MARGIN",
  "Twickenham, Nations Championship rugby"),
 ("Western Europe", "SCOTLAND BEAT JAPAN 11 TRIES TO NIL",
  "Edinburgh rout in the Nations Championship"),
 ("Western Europe", "ALCARAZ BEATS SHELTON, REACHES ATP FINAL",
  "3-6 6-3 7-6(1) in Turin; 13th straight win"),
 ("Western Europe", "HARRY KANE OUT FOR MONTHS",
  "Torn ankle ligament; Bayern draw 1-1 with Cologne"),
 ("North Africa", "MARION COTILLARD OPENS MARRAKECH FILM FESTIVAL",
  "French star opens the Moroccan festival"),
 ("Eastern Europe", "TRUMP TELLS EUROPE TO DEFUND UKRAINE",
  "Angry call after the Putin summit, Telegraph reports"),
 ("Eastern Europe", "TRUMP WEIGHS NEW STRIKES ON IRAN",
  "As Israel presses for action, officials say"),
 ("Eastern Europe", "RUSSIA GRASPS US OFFER ON EUROPEAN SECURITY",
  "Moscow revives old demands in the talks"),
 ("Eastern Europe", "TRUMP DEFENDS PUTIN TIES; ZELENSKYY CALLS PUTIN A KILLER",
  "Summit fallout in Kyiv and Washington"),
 ("East Asia", "TRUMP, XI AND PUTIN HOLD RARE 3-WAY TALKS",
  "Shenzhen summit on nuclear risks; no breakthrough"),
 ("East Asia", "APEC ADOPTS SHENZHEN OUTLOOK  *19 NOV*",
  "Leaders' declaration adopted 19 Nov; Vietnam hosts in 2027"),
 ("East Asia", "JAPAN SIDELINED BY CHINA AS TIES HIT RECORD LOW",
  "Tokyo-Beijing freeze deepens"),
 ("East Asia", "NIKKEI -5.1%, KOSPI -5.5%, TAIEX -6.2%",
  "Asia tech rout; SoftBank -14.5%, Samsung -7%"),
 ("East Asia", "JAPAN CORE INFLATION 2.2% IN OCT",
  "Price gauge rises in Tokyo data"),
 ("East Asia", "SAUDI-JAPAN OIL STOCKPILE DEAL AGREED",
  "Tokyo energy pact signed"),
 ("East Asia", "PILOTLESS AIR TAXI CARRIES PASSENGER IN JAPAN",
  "Yamanashi test flight with a passenger aboard"),
 ("East Asia", "CHOI MIN-JEONG WINS 3RD STRAIGHT WORLD TOUR TITLE",
  "Short-track 1,000m gold on home ice in Seoul"),
 ("East Asia", "BTS WIN 5 AWARDS AT MAMA IN OSAKA",
  "K-pop sweep at the Japan ceremony"),
 ("Southeast Asia", "AIR NIUGINI JET LANDS SAFELY IN DAVAO",
  "146 aboard safe after engine-fire warning; Hong Kong-PNG flight"),
 ("Southeast Asia", "AUSTRALIA-CANADA-NZ JOINT APEC STATEMENT",
  "21 Nov pledge on peace and stability in the region"),
 ("Southeast Asia", "CONTACT GROUP ON ONLINE SCAM CENTRES  *19 NOV*",
  "US, Australia, Indonesia, Philippines + 9 more; statement 19 Nov"),
 ("South Asia", "NEPAL PM BALENDRA SHAH TO NEW DELHI 22 NOV",
  "Modi meeting announced for Sunday"),
 ("South Asia", "INDIA WAGE STAGNATION DEBATE",
  "PM criticises industry at the FICCI centenary"),
 ("Central Asia", "MONGOLIAN PRESIDENT RESIGNS",
  "Resignation opens the way to early elections"),
 ("Middle East", "COP31 IN OVERTIME IN ANTALYA",
  "~200 nations; draft omits fossil fuels; 3rd draft due Sat"),
 ("Middle East", "TURKEY TAKES CONTROL OF SOZCU TV",
  "Istanbul media seizure"),
 ("Southeast Asia", "ICJ: MYANMAR GUILTY OF GENOCIDE  *RULING 19 NOV*",
  "ICJ 9-6; ~10,000 Rohingya killed in 2017; reactions on 21 Nov"),
 ("Southern Africa", "PHUMZILE MLAMBO-NGCUKA DIES AGED 71",
  "Ex-SA deputy president and ex-UN Women chief, Cape Town"),
 ("Southern Africa", "ANC FIGHTS TO HOLD KEY CITIES",
  "Disappointing election results in South Africa"),
 ("East Africa", "700,000 DISPLACED IN SOUTHERN ETHIOPIA",
  "Conflict displacement in the south"),
 ("East Africa", "TUNDU LISSU CONVICTED OF SEDITION",
  "Tanzanian opposition leader, Dar es Salaam"),
 ("East Africa", "UGANDA RESTRICTS GATHERINGS OVER EBOLA",
  "Kampala curbs on travel and gatherings"),
 ("West Africa", "BOAT OF FUNERAL MOURNERS CAPSIZES IN NIGERIA",
  "Bayelsa disaster on the waterways"),
 ("West Africa", "FIGHTING WIDENS IN EASTERN CONGO",
  "DRC front expands"),
 ("Global", "UN TALKS AGREE TO CONTINUE WORK ON AI WEAPONS RULES",
  "Geneva: autonomous-weapons talks extended past deadline"),
 ("Global", "UNGA PRESIDENT VISITS ROHINGYA CAMPS",
  "'The road to home began' after the ICJ ruling; visit 20 Nov"),
 ("Space", "BEPICOLOMBO ENTERS MERCURY ORBIT",
  "ESA-JAXA, 8-year trip; captured into orbit 18:24 UTC"),
 ("Space", "VOYAGER 1 NOW 24 LIGHT-HOURS FROM EARTH",
  "16.1bn miles away; its signals take a day to arrive"),
 ("Global", "CERN FINDS FIRST EVIDENCE OF ULTRA-RARE DECAY",
  "Sought for 40+ years, Geneva particle physics"),
 ("North America", "AI-ASSISTED RIEMANN PROOF CLAIMED",
  "Anthropic mathematician's claim, San Francisco"),
 ("Oceania", "NEW RESEARCH MAY REWRITE HUMAN FAMILY TREE",
  "Melbourne study rethinks the family tree"),
 ("Middle East", "NEW FOSSIL CARNIVORE FROM UAE NAMED AFTER ABU DHABI",
  "Desert fossil find"),
 ("Oceania", "SEAWEED UNSEEN FOR 90 YEARS REDISCOVERED",
  "Large underwater forests found near Lord Howe Island"),
 ("Global", "DARAXONRASIB PILL: PANCREATIC TUMOURS VANISH",
  "Cancer undetectable in 1 in 12 trial patients"),
 ("Western Europe", "PRINCESS OF WALES IN REMISSION",
  "Catherine announces it in a new documentary"),
 ("North America", "AI MAY PREDICT SUDDEN CARDIAC DEATH",
  "Berkeley method flags risk before it strikes"),
 ("Global", "MERCK CANCER DRUG WINS 2ND PHASE 3 TRIAL",
  "Gastric-cancer antibody-drug conjugate succeeds"),
 ("Oceania", "AUSTRALIA BEAT ENGLAND BY 3 WICKETS IN 1ST T20",
  "Chaudhary stars in the thriller"),
 ("Western Europe", "CANADIAN PAIR WIN SILVER AT FINLANDIA TROPHY",
  "Helsinki; Canadian speed skaters take bronze in Obihiro"),
]

REGIONS = sorted({r for r, _, _ in STORIES})
assert len(STORIES) == 82, len(STORIES)

# ---------------------------------------------------------------- heroes
def hero_war(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(32, 22, 28))
    d.polygon([(x, y + h), (x, y + h - 55), (x + 40, y + h - 80), (x + 70, y + h - 48),
               (x + 110, y + h - 92), (x + 150, y + h - 58), (x + 190, y + h - 84),
               (x + 240, y + h - 50), (x + 280, y + h - 70), (x + w, y + h - 44),
               (x + w, y + h)], fill=(58, 34, 40))
    for bx, by in [(x + 18, y + 22), (x + 120, y + 12), (x + 230, y + 30)]:
        cx, cy = bx + 23, by + 10
        for ang in range(0, 360, 30):
            import math
            ex = cx + int(24 * math.cos(math.radians(ang)))
            ey = cy + int(11 * math.sin(math.radians(ang)))
            d.line([cx, cy, ex, ey], fill=(255, 190, 80), width=2)
        d.ellipse([cx - 12, cy - 6, cx + 12, cy + 6], fill=(240, 170, 90))
    for sx in (x + 60, x + 150, x + 250):
        d.line([sx, y + 8, sx + 14, y + 58], fill=(255, 210, 120), width=2)
        d.line([sx + 14, y + 58, sx + 26, y + 20], fill=(255, 210, 120), width=2)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))

def hero_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 44))
    for i in range(6):
        gy = y + 14 + i * 18
        d.line([x + 8, gy, x + w - 8, gy], fill=(38, 62, 96), width=1)
    pts = [(x + 10 + i * 30, y + 18 + int(i * i * 1.15)) for i in range(11)]
    d.line(pts, fill=(255, 90, 70), width=4, joint="curve")
    for px, py in pts[::3]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 210, 90))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))

def hero_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 34))
    for sx, sy, sr in [(x + 30, y + 20, 1), (x + 90, y + 40, 2), (x + 180, y + 14, 1),
                       (x + 260, y + 44, 2), (x + 300, y + 18, 1), (x + 140, y + 60, 1)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    d.ellipse([x + 190, y + 18, x + 310, y + 138], fill=(196, 140, 90))
    d.ellipse([x + 210, y + 34, x + 250, y + 74], fill=(160, 105, 65))
    d.ellipse([x + 260, y + 80, x + 282, y + 102], fill=(160, 105, 65))
    d.ellipse([x + 40, y + 88, x + 150, y + 128], outline=(255, 210, 90), width=2)
    d.rectangle([x + 82, y + 96, x + 108, y + 120], fill=(200, 210, 225))
    d.polygon([(x + 108, y + 100), (x + 128, y + 92), (x + 128, y + 124), (x + 108, y + 116)],
              fill=(90, 140, 220))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 70), (-95, 68), (-80, 62), (-60, 55), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 20), (-97, 16), (-105, 20), (-117, 32),
     (-125, 42), (-150, 60), (-168, 66)],
    [(-80, 8), (-60, 8), (-50, 0), (-40, -8), (-35, -18), (-48, -28), (-58, -34),
     (-65, -40), (-70, -52), (-73, -30), (-80, -12), (-80, 8)],
    [(-10, 36), (0, 43), (-2, 48), (5, 53), (10, 57), (18, 56), (24, 60), (30, 70),
     (40, 68), (50, 68), (60, 69), (70, 72), (100, 77), (130, 72), (160, 70),
     (178, 66), (160, 60), (140, 40), (130, 33), (120, 22), (108, 10), (100, 8),
     (90, 22), (80, 8), (72, 20), (60, 25), (50, 30), (43, 12), (40, 15), (35, 28),
     (30, 36), (22, 36), (10, 37), (0, 36), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
     (48, 11), (51, 12), (44, -2), (40, -10), (35, -18), (32, -28), (25, -34),
     (18, -32), (14, -22), (12, -10), (9, 4), (-8, 4), (-17, 15)],
    [(113, -22), (130, -12), (142, -11), (150, -20), (153, -27), (147, -38),
     (140, -38), (130, -32), (120, -34), (114, -30), (113, -22)],
]
PINS = [("KYIV", 30, 50, 1, -10, -4), ("POLAND", 19, 52, 3, 0, -8),
        ("GAZA", 34, 31, 4, 0, 12), ("HORMUZ", 56, 26, 5, 12, -8), ("SINALOA", -107, 25, 8, 0, 0),
        ("HAITI", -72, 18, 9, 0, 0), ("ANTALYA", 30, 36, 58, 10, 12), ("THE HAGUE", 4, 52, 60, -14, 8),
        ("BRASILIA", -47, -15, 10, 0, 0), ("TOKYO", 139, 35, 46, 0, 0), ("DAVAO", 125, 7, 52, 0, 0)]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 232))
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=(178, 196, 158), outline=(120, 140, 110))
    for name, lon, lat, num, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (90 - lat) / 180 * h + dy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py), str(num), font=font(8, True), fill=(255, 255, 255), anchor="mm")

# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 78], fill=INK)
    d.text((16, 8), "THE WORLD", font=font(40, True), fill=(255, 255, 255))
    d.text((1008, 12), "SATURDAY, 21 NOVEMBER 2026", font=font(15, True),
           fill=(255, 210, 90), anchor="ra")
    d.text((1008, 34), "82 STORIES  \u00b7  18 REGIONS  \u00b7  MOOD: UNEASY",
           font=font(11, True), fill=(200, 210, 225), anchor="ra")
    d.text((16, 58), "One day, one front page \u2014 war, a market rout, a climate summit in overtime, Mercury at last",
           font=font(11), fill=(200, 210, 225))
    d.text((1008, 58), "Sources: One Turn \u00b7 AP \u00b7 CNN \u00b7 Reuters \u00b7 ESA \u00b7 ATP",
           font=font(9), fill=(150, 160, 175), anchor="ra")
    # heroes
    hy, hh, hw, gap = 86, 158, 322, 13
    heroes = [(hero_war, "1  KYIV UNDER FIRE", "400+ drones, 110 missiles; 8 dead"),
              (hero_market, "2  THE AI ROUT", "S&P -3.7% \u00b7 Nasdaq -5.28% \u00b7 VIX 35.9"),
              (hero_space, "3  MERCURY, AT LAST", "BepiColombo enters orbit, 18:24 UTC")]
    for i, (fn, cap, sub) in enumerate(heroes):
        x = 16 + i * (hw + gap)
        fn(d, x, hy, hw, hh - 26)
        d.rectangle([x, hy + hh - 26, x + hw, hy + hh], fill=INK)
        d.text((x + 8, hy + hh - 22), cap, font=font(10, True), fill=(255, 255, 255))
        d.text((x + 8, hy + hh - 9), sub, font=font(8), fill=(200, 210, 225))
    # market strip
    my = 252
    box(d, (16, my, 1008, my + 26), fill=(255, 255, 255), outline=MID)
    d.text((24, my + 5), "MARKETS  \u2014  S&P 6,910 -3.7%   Nasdaq -5.28%   Dow -1.93%   "
           "Nikkei -5.1%   FTSE -1.02%   Brent $89.95   Gold -4.6%   Bitcoin ~$60,100   VIX 35.9",
           font=font(10, True), fill=RED)
    # map + numbers/quote
    mapy, maph = 286, 118
    d.text((16, mapy - 2), "", font=font(10, True), fill=INK)
    box(d, (16, mapy, 648, mapy + maph), fill=(214, 228, 232), outline=MID)
    draw_map(d, 18, mapy + 2, 628, maph - 4)
    d.rectangle([22, mapy + maph - 16, 420, mapy + maph - 4], fill=(255, 255, 255))
    d.text((24, mapy + maph - 15), "WHERE IT HAPPENED \u2014 numbered pins match the brief below",
           font=font(8, True), fill=NAVY)
    bx = 660
    box(d, (bx, mapy, 1008, mapy + maph), fill=(255, 255, 255), outline=MID)
    d.text((bx + 10, mapy + 6), "BY THE NUMBERS", font=font(10, True), fill=INK)
    nums = [("400+", "drones at Ukraine"), ("110", "missiles at Ukraine"),
            ("60", "wounded, Kryvyi Rih"), ("146", "safe, Davao landing"),
            ("24", "light-hours away"), ("69%", "dengue cut, Brazil")]
    for i, (n, lab) in enumerate(nums):
        cx = bx + 10 + (i % 3) * 114
        cy = mapy + 26 + (i // 3) * 30
        d.text((cx, cy), n, font=font(13, True), fill=RED)
        d.text((cx, cy + 15), lab, font=font(7), fill=GREY)
    d.line([bx + 10, mapy + 88, 998, mapy + 88], fill=MID)
    d.text((bx + 10, mapy + 92), "QUOTE OF THE DAY \u2014 \u201cWe are close to the finish line",
           font=font(9, True), fill=NAVY)
    d.text((bx + 10, mapy + 104), "but not there yet.\u201d \u2014 Murat Kurum, COP31 president, Antalya",
           font=font(8), fill=INK)
    # featured: stories 4-15 (12) in 3 columns x 4 rows
    fy = 420
    d.text((16, fy), "THE DAY IN BRIEF \u2014 12 STORIES THAT LED THE NEWS",
           font=font(11, True), fill=INK)
    d.line([16, fy + 16, 1008, fy + 16], fill=INK, width=2)
    colw, rowh = 322, 46
    for idx in range(12):
        n = 4 + idx
        region, head, det = STORIES[n - 1]
        cx = 16 + (idx % 3) * (colw + 13)
        cy = fy + 22 + (idx // 3) * rowh
        d.text((cx, cy), f"{n}.", font=font(10, True), fill=RED)
        d.text((cx + 20, cy), fit(d, head, font(9, True), colw - 20),
               font=font(9, True), fill=INK)
        for j, ln in enumerate(wrap(d, det, font(8), colw - 20)[:2]):
            d.text((cx + 20, cy + 12 + j * 10), ln, font=font(8), fill=GREY)
        d.text((cx + 20, cy + 32), region.upper(), font=font(7, True), fill=TEAL)
    # the brief: stories 16-82 (67) in 3 columns, one line each
    by = fy + 22 + 4 * rowh + 8
    d.text((16, by), "THE BRIEF \u2014 16\u201382: EVERY OTHER STORY OF THE DAY, ONE LINE EACH",
           font=font(11, True), fill=INK)
    d.line([16, by + 16, 1008, by + 16], fill=INK, width=2)
    rest = STORIES[15:]
    per = 23
    for ci in range(3):
        chunk = rest[ci * per:(ci + 1) * per]
        cx = 16 + ci * (colw + 13)
        for ri, (region, head, det) in enumerate(chunk):
            n = 16 + ci * per + ri
            yy = by + 22 + ri * 11
            d.text((cx, yy), f"{n}.", font=font(8, True), fill=RED)
            d.text((cx + 20, yy), fit(d, head, font(8), colw - 20), font=font(8), fill=INK)
    # timeline
    ty = by + 22 + per * 11 + 8
    box(d, (16, ty, 1008, ty + 34), fill=NAVY)
    d.text((24, ty + 4), "24H UTC TIMELINE", font=font(9, True), fill=(255, 210, 90))
    d.text((24, ty + 17), "01:56 COP31 passes deadline, no deal  \u00b7  morning: Kryvyi Rih strike reported  "
           "\u00b7  afternoon: Alcaraz reaches ATP final, Turin  \u00b7  18:24 BepiColombo enters Mercury orbit  "
           "\u00b7  evening: US markets close in correction",
           font=font(9), fill=(255, 255, 255))
    # date check + footer
    dy = ty + 42
    box(d, (16, dy, 1008, dy + 30), fill=(255, 248, 220), outline=GOLD)
    dc = ("DATE CHECK \u2014 EXCLUDED AS NOT 21 NOV: Anthropic IPO debut (19 Nov; only Fri's -8.5% "
          "sell-off counts) \u00b7 ICJ Myanmar ruling (19 Nov; 21 Nov = reactions) \u00b7 APEC Shenzhen "
          "Outlook (19 Nov) \u00b7 England ODI series win (18 Nov) \u00b7 Australia-Philippines defence "
          "pact (15 Nov) \u00b7 Alcaraz-Cobolli group match (20 Nov). Dated follow-ups are flagged "
          "*19 NOV* in the brief and counted as follow-ups, not as 21 Nov events.")
    for j, ln in enumerate(wrap(d, dc, font(8), 968)):
        d.text((24, dy + 3 + j * 10), ln, font=font(8), fill=INK)
    d.text((16, dy + 36), "THE WORLD \u2014 Saturday 21 November 2026 \u00b7 82 stories \u00b7 18 regions \u00b7 "
           "Drawn from scratch with PIL; no photographs. Deterministic: same code, same pixels.",
           font=font(8), fill=GREY)
    img.save(OUT)
    print(f"stories={len(STORIES)} regions={len(REGIONS)} {sorted(REGIONS)}")
    print("saved", OUT, img.size, img.mode)

if __name__ == "__main__":
    build()
