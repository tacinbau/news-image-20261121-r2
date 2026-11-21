#!/usr/bin/env python3
"""THE WORLD — Saturday, 21 November 2026.
One image summarising the day's world news. 97 stories, 50+ regions.

Deterministic: stdlib + Pillow only, no randomness, no clock, no network.
Run twice -> identical entry.png (same md5).

SOURCES (all editions dated Saturday 21 November 2026):
  - One Turn world-news edition, Sat 21 Nov 2026, updated 12:04 PM ET
    (49 stories + 15 in brief, from 863 headlines)
  - Kilambi News, Saturday 21 November 2026 politics feed
  - TFI Online, Saturday, November 21, 2026 (NYT digest)
  - WW6RAG Daily Brief, Saturday, November 21, 2026
  - Naked Capitalism Links 11/21/2026
  - Ken Radio Substack, Saturday, November 21, 2026
  - Apprised.news Good News, 21 November 2026
  - USA Daily News, November 21, 2026

DATE CHECK — items from OTHER dates explicitly EXCLUDED (not counted):
  - EU-Indonesia trade & investment agreements (Fri 20 Nov)
  - Shenzhen trilateral summit SIGNING itself (Fri 20 Nov; only the
    Sat 21 Nov reactions / White House news conference are counted)
  - Anthropic IPO debut (Thu 19 Nov; only the Fri slump as reported
    in Sat 21 Nov editions is counted)
  - Italy general strike (Fri 20 Nov)
  - Medvedev beats Tiafoe, ATP Finals (Fri 20 Nov)
  - Harry Kane ankle injury report (Fri 20 Nov)
  - Bayern-Cologne draw (Fri 20 Nov)
  - Las Vegas GP practice rain-out (Thu 19 Nov)
  - ICJ Myanmar genocide ruling: carried as a lead item in the
    Sat 21 Nov editions (One Turn, Naked Capitalism links 11/21)
  - COP31: summit passed its Friday deadline; the overtime itself
    is the Sat 21 Nov story.
Every story below appears in a source edition dated 21 November 2026.
"""

import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (18, 18, 18)
PAPER = (247, 243, 234)
RED = (178, 34, 34)
BLUE = (24, 62, 120)
GREY = (96, 92, 84)
RULE = (18, 18, 18)
LIGHT_RULE = (180, 172, 158)

# region -> colour (fixed, deterministic palette)
PALETTE = [
    (178, 34, 34), (24, 62, 120), (14, 110, 70), (128, 64, 12),
    (96, 32, 128), (10, 96, 110), (150, 20, 60), (60, 60, 60),
]


def region_colour(region):
    return PALETTE[sum(region.encode()) % len(PALETTE)]


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)             # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731

# (region, headline) — each headline <= ~62 chars so it fits one line
# in a 490px column at 10px together with its number + region tag.
SECTIONS = [
    ("WAR & POLITICS", [
        ("UKRAINE", "Russian missile hits Kryvyi Rih: 2 killed, 60 hurt"),
        ("UKRAINE", "Russia fires 400+ drones, 110 missiles at Ukraine"),
        ("POLAND", "Russian missiles and drone land in Poland"),
        ("POLAND", "Warsaw seeks more NATO air defences"),
        ("RUSSIA", "Ukraine hits 3 Russian missile platforms"),
        ("RUSSIA", "Drones set cargo ship ablaze in Gulf of Finland"),
        ("UKRAINE", "Russian strike kills 3 water workers in Kyiv"),
        ("FRANCE", "Paris calls UN meeting on strikes in Kyiv"),
        ("SAUDI ARABIA", "Houthis strike power plant, port in Jazan"),
        ("SAUDI ARABIA", "Houthi strike hits Riyadh tower; no injuries"),
        ("HORMUZ", "Tanker hit by projectiles, catches fire"),
        ("GAZA", "Israeli strike kills 3 in aid vehicle"),
        ("GAZA", "22,000+ Palestinian children killed, ministry says"),
        ("HAITI", "Salvadoran troops fight gangs, lose soldiers"),
        ("DR CONGO", "Fighting widens in the east"),
        ("ETHIOPIA", "700,000 displaced; Eritrea masses troops"),
        ("IRAQ", "Army enters Kata'ib Hezbollah stronghold"),
        ("TURKEY", "COP31 talks run past deadline on fossil fuels"),
        ("USA", "Trump defends Putin ties after Shenzhen summit"),
        ("CHINA", "Trump, Xi, Putin hail 'momentous' summit"),
        ("UK", "Burnham signs three post-Brexit deals with EU"),
        ("DENMARK", "Expels Russian attache over plot to kill rapper"),
        ("DENMARK", "Parliament ratifies US Greenland deal 109-0"),
        ("SPAIN", "Snap election set for Nov 29; banking tax eyed"),
        ("BRAZIL", "Bolsonaro hospitalised with intestinal blockage"),
        ("MONGOLIA", "President Khurelsukh resigns; snap polls loom"),
        ("NEPAL", "PM Balendra Shah to visit India Nov 22-23"),
        ("SOUTH KOREA", "Ruling party moves to impeach chief justice"),
        ("ESTONIA", "To close border crossings with Russia"),
        ("TURKEY", "Authorities take control of Sozcu TV"),
        ("TANZANIA", "Opposition leader Lissu convicted of sedition"),
        ("SOMALIA", "Expels UAE ambassador over sovereignty"),
        ("SOUTH AFRICA", "Mlambo-Ngcuka dies aged 71"),
    ]),
    ("MARKETS & MONEY", [
        ("USA", "S&P 500 falls 3.7% to 6,910 in AI sell-off"),
        ("JAPAN", "Nikkei drops 5.1% as AI rout spreads in Asia"),
        ("MARKETS", "Bitcoin falls to $55,830, then recovers"),
        ("MARKETS", "Gold drops 4.6%; Brent crude holds near $90"),
        ("USA", "Anthropic slumps 8% a day after $2tn debut"),
        ("USA", "SEC probes Nvidia accounting; shares fall ~14%"),
        ("ARGENTINA", "Country risk tops 1,000 points"),
        ("KENYA", "Onshore crude drilling begins in Turkana"),
        ("JAPAN", "Saudi Arabia, Japan agree oil stockpile deal"),
        ("USA", "Hyperscalers sold $284bn of bonds this year"),
        ("USA", "Trump signs Common Cents Act, ends penny"),
        ("USA", "Trump threatens tax on firms building AI hubs abroad"),
        ("USA", "Trump weighs new strikes on Iran"),
        ("USA", "White House fires National Cyber Director"),
        ("MEXICO", "Forces capture FBI most-wanted cartel boss"),
    ]),
    ("JUSTICE & DISASTER", [
        ("USA", "FBI crime database, USDA system reportedly hacked"),
        ("USA", "CISA orders patches as hackers exploit VMware flaw"),
        ("USA", "Man convicted of starting deadly Palisades fire"),
        ("USA", "Man jailed 19 years over plot to kill Sikh leader"),
        ("FRANCE", "Police sentenced over racist beating of Zecler"),
        ("PERU", "Magnitude 6.7 quake shakes central Junin"),
        ("TIMOR-LESTE", "Magnitude 6.8 quake offshore; no tsunami"),
        ("NIGERIA", "Boat of funeral mourners capsizes in Bayelsa"),
        ("IRAQ", "Fire at Basra power station kills 4, injures 30"),
        ("USA", "US loses measles elimination status"),
        ("UGANDA", "Gatherings restricted over Ebola"),
        ("NETHERLANDS", "ICJ: Myanmar responsible for Rohingya genocide"),
        ("MYANMAR", "Junta calls ICJ genocide ruling 'unfair'"),
        ("SWITZERLAND", "UN agrees draft autonomous weapons rules by 2028"),
        ("EU", "Disburses EUR 7.9bn to Ukraine, largest payment"),
        ("EU", "Costa proposes 3% digital tax on big tech"),
        ("CHINA", "Japan sidelined as ties with Beijing hit low"),
    ]),
    ("SCIENCE & HEALTH", [
        ("MERCURY", "BepiColombo reaches Mercury orbit after 8 years"),
        ("SWITZERLAND", "CERN finds first evidence of ultra-rare decay"),
        ("SPACE", "Voyager 1 now 24 light-hours from Earth"),
        ("USA", "Mathematician claims AI-assisted Riemann proof"),
        ("JAPAN", "Pilotless air taxi carries a passenger"),
        ("AUSTRALIA", "Taung Child study may rewrite human family tree"),
        ("USA", "Blue sucker fish found to live over 100 years"),
        ("GERMANY", "Record X-ray laser flashes beat atomic gaps"),
        ("ANTARCTICA", "Ancient mountain ranges found under the ice"),
        ("UAE", "New fossil carnivore named after Abu Dhabi"),
        ("USA", "Google launches Gemini 4 Neon vs Claude, GPT-6.2"),
        ("SPACE", "ESA's Hera reaches Didymos after DART impact"),
        ("UK", "Pill makes pancreatic tumours vanish in 1 in 12"),
        ("BRAZIL", "Mosquitoes cut dengue cases by 69%"),
        ("UK", "Princess of Wales announces she is in remission"),
        ("USA", "AI method may predict sudden cardiac death"),
    ]),
    ("CULTURE & SPORT", [
        ("USA", "Verstappen takes Las Vegas GP pole"),
        ("ITALY", "Alcaraz beats Shelton, reaches ATP Finals final"),
        ("ENGLAND", "England beat New Zealand by record margin"),
        ("SCOTLAND", "Scotland beat Japan 11 tries to nil"),
        ("USA", "Harden passes Kobe on NBA 50-point games list"),
        ("USA", "Olivia Rodrigo's album debuts at No. 1"),
        ("JAPAN", "BTS win five awards at MAMA in Osaka"),
        ("MOROCCO", "Cotillard opens Marrakech Film Festival"),
        ("SOUTH KOREA", "Choi Min-jeong wins third straight World title"),
        ("FINLAND", "Canadian pair wins silver at Finlandia Trophy"),
        ("USA", "Sterling eyes title after UFC win in Qatar"),
        ("INDIA", "Modi opens bridge named after Nitish Kumar"),
        ("INDIA", "Pakistan minister attends SCO forum in Delhi"),
        ("VIETNAM", "Abolishes death penalty for drug trafficking"),
        ("VIETNAM", "Law speeds land expropriation for projects"),
        ("FIJI", "Tropical Fiji declares El Nino drought 'crisis'"),
    ]),
]

LEADS = [
    ("MISSILES LAND IN POLAND",
     "Russia fires 400+ drones and 110 missiles at Ukraine; three "
     "projectiles come down in Poland. NATO calls it a grave violation."),
    ("COP31 RUNS INTO OVERTIME",
     "Climate talks in Antalya pass their Friday deadline with no deal "
     "as fossil-fuel language is dropped from the draft text."),
    ("AI SELL-OFF SPOOKS MARKETS",
     "S&P 500 -3.7%, Nikkei -5.1%, Nasdaq -5.3%. Bitcoin falls to "
     "$55,830, its lowest since September 2024, then recovers."),
]

TICKER = ("S&P 500  6,910  -3.70%    FTSE 100  10,346  -1.02%    "
           "Nikkei  -5.06%    Brent  $89.95  +0.57%    Gold  -4.62%    "
           "Bitcoin  ~$58,000    USD  103.84")


def wrap_text(draw, text, fnt, max_w):
    """Wrap to lines that fit max_w; assert nothing is clipped."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        assert draw.textlength(ln, font=fnt) <= max_w, f"CLIPPED: {ln!r}"
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 4], fill=INK)
    title = "THE WORLD"
    tf = F_SERIF(66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    d.line([MARGIN, 96, W - MARGIN, 96], fill=RULE, width=2)
    d.line([MARGIN, 100, W - MARGIN, 100], fill=RULE, width=1)
    sub = (f"Saturday, 21 November 2026  ·  "
           f"{sum(len(s) for _, s in SECTIONS)} stories  ·  "
           f"{len({r for _, s in SECTIONS for r, _ in s})} regions  ·  "
           "World Mood: Uneasy")
    sf = F_BOLD(15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 108), sub, font=sf, fill=RED)
    d.line([MARGIN, 132, W - MARGIN, 132], fill=LIGHT_RULE, width=1)

    # ---- lead band: 3 boxes ----
    y0, y1 = 142, 222
    gap = 12
    bw = (W - 2 * MARGIN - 2 * gap) // 3
    for i, (head, body) in enumerate(LEADS):
        x0 = MARGIN + i * (bw + gap)
        x1 = x0 + bw
        d.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
        d.rectangle([x0, y0, x1, y0 + 26], fill=INK)
        hf = F_BOLD(13)
        ht = head
        assert d.textlength(ht, font=hf) <= bw - 12, f"lead head clipped: {ht}"
        d.text((x0 + 6, y0 + 6), ht, font=hf, fill=PAPER)
        bf = F_SANS(11)
        for j, ln in enumerate(wrap_text(d, body, bf, bw - 12)):
            d.text((x0 + 6, y0 + 32 + j * 14), ln, font=bf, fill=INK)

    # ---- markets ticker ----
    ty = 232
    d.rectangle([MARGIN, ty, W - MARGIN, ty + 22], fill=(232, 226, 210))
    tk = F_BOLD(11)
    assert d.textlength(TICKER, font=tk) <= W - 2 * MARGIN - 12, "ticker clipped"
    d.text((MARGIN + 6, ty + 5), TICKER, font=tk, fill=INK)

    # ---- story columns (2 columns) ----
    col_w = (W - 2 * MARGIN - 16) // 2
    col_x = [MARGIN, MARGIN + col_w + 16]
    top = 268
    bottom = 978
    story_f = F_SANS(10)
    tag_f = F_BOLD(10)
    num_f = F_BOLD(10)
    sec_f = F_BOLD(13)
    line_h = 12.5

    # split sections: col 0 = WAR & POLITICS + MARKETS & MONEY (48)
    # col 1 = JUSTICE & DISASTER + SCIENCE & HEALTH + CULTURE & SPORT (49)
    col_sections = [SECTIONS[:2], SECTIONS[2:]]
    n = 0
    for ci, sections in enumerate(col_sections):
        x = col_x[ci]
        y = top
        for sec_title, stories in sections:
            d.text((x, y), sec_title, font=sec_f, fill=RED)
            d.line([x, y + 16, x + col_w, y + 16], fill=RED, width=1)
            y += 21
            for region, headline in stories:
                n += 1
                num = f"{n:02d}"
                prefix = f"{num}  {region} — "
                full = prefix + headline
                # wrap against col_w - 14: the bold region tag draws
                # slightly wider than the regular font used for wrapping
                lines = wrap_text(d, full, story_f, col_w - 14)
                # re-draw with coloured region tag on first line
                assert y + len(lines) * line_h <= bottom, (
                    f"OVERFLOW col {ci} at story {n}")
                # draw first line with styling: number (bold ink),
                # region tag (bold, coloured), then " — " + headline.
                # NOTE: wrap_text joins words with single spaces, so the
                # wrapped prefix is f"{num} {region} — " (one space).
                first = lines[0]
                wrapped_prefix = f"{num} {region} — "
                assert first.startswith(wrapped_prefix), (
                    f"wrap split prefix: {first!r}")
                rest1 = first[len(wrapped_prefix):]
                d.text((x, y), num, font=num_f, fill=INK)
                nx = x + d.textlength(num + " ", font=num_f)
                d.text((nx, y), region, font=tag_f,
                       fill=region_colour(region))
                rx = nx + d.textlength(region, font=tag_f)
                d.text((rx, y), " — " + rest1, font=story_f, fill=INK)
                drawn_w = (rx - x) + d.textlength(" — " + rest1,
                                                  font=story_f)
                assert drawn_w <= col_w, f"drawn line too wide: {first!r}"
                for j, ln in enumerate(lines[1:], start=1):
                    d.text((x, y + j * line_h), ln, font=story_f, fill=INK)
                y += len(lines) * line_h
            y += 6

    # ---- footer ----
    d.line([MARGIN, 990, W - MARGIN, 990], fill=RULE, width=1)
    foot = ("Sources: AP · Reuters · BBC · CNN · One Turn (21 Nov 2026 ed.) · Kilambi · "
            "TFI · WW6RAG — every story dated Saturday 21 November 2026.")
    ff = F_SANS(10)
    assert d.textlength(foot, font=ff) <= W - 2 * MARGIN, "footer clipped"
    d.text((MARGIN, 996), foot, font=ff, fill=GREY)
    d.text((MARGIN, 1009), "World Television Day  ·  Built with Python stdlib + Pillow — deterministic build",
           font=ff, fill=GREY)
    return img


def main():
    total = sum(len(s) for _, s in SECTIONS)
    regions = {r for _, s in SECTIONS for r, _ in s}
    assert total >= 90, f"only {total} stories"
    assert len(regions) >= 20, f"only {len(regions)} regions"
    img = draw()
    assert img.size == (1024, 1024) and img.mode == "RGB"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print(f"stories={total} regions={len(regions)} md5={md5} size={img.size}")


if __name__ == "__main__":
    main()
