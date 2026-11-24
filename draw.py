#!/usr/bin/env python3
"""news-23 b15 front-page-dense: THE WORLD TODAY, Monday 23 November 2026.
Draws a 1024x1024 front page with 31 stories (3 hero scenes + 10 cards + 18 ALSO).
Run: python3 draw.py  -> writes entry.png next to this file (build-time only).
The graded entry point is main.py (stdlib-only); it copies entry.png to $MAKEFUN_OUTPUT_DIR.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

CREAM = (247, 242, 227)
INK = (22, 22, 22)
RED = (186, 32, 32)
NAVY = (18, 42, 76)
TEAL = (14, 90, 96)
GOLD = (172, 120, 18)
GREEN = (46, 110, 52)
BROWN = (122, 72, 20)
PURPLE = (96, 44, 130)
OLIVE = (110, 110, 40)
GREY = (96, 96, 96)
LIGHT = (238, 232, 214)
SKY = (214, 230, 238)
LAND = (168, 196, 130)

FD = "/usr/share/fonts/truetype/dejavu"


def f(path, size):
    return ImageFont.truetype(os.path.join(FD, path), size)


SERIF_B = lambda s: f("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)
SANS_B = lambda s: f("DejaVuSans-Bold.ttf", s)


def wrap(d, text, font, max_w, max_lines=None):
    """Wrap text to max_w; truncate with ellipsis if max_lines given."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "…", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def chip(d, x_right, y, label, fill):
    """Right-aligned chip; returns left edge."""
    font = SANS_B(10)
    tw = d.textlength(label, font=font)
    w = int(tw) + 12
    x0 = x_right - w
    d.rounded_rectangle([x0, y, x_right, y + 16], radius=3, fill=fill)
    d.text((x0 + 6, y + 3), label, font=font, fill=(255, 255, 255))
    return x0


def hero_scene_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 26, 54))
    # skyline bars along the bottom
    import random
    rnd = random.Random(7)
    bx = x + 8
    while bx < x + w - 14:
        bw = rnd.randint(10, 18)
        bh = rnd.randint(14, 42)
        d.rectangle([bx, y + h - 26 - bh, bx + bw, y + h - 26], fill=(38, 62, 104))
        for wy in range(3):
            d.rectangle([bx + 3, y + h - 22 - bh + wy * 9, bx + bw - 3,
                         y + h - 19 - bh + wy * 9], fill=(240, 200, 90))
        bx += bw + 4
    # big -3.3% top-left, chart kept below it
    d.text((x + 10, y + 8), "−3.3%", font=SANS_B(30), fill=(235, 60, 60))
    pts = [(x + 14, y + 62), (x + 52, y + 58), (x + 92, y + 70), (x + 132, y + 66),
           (x + 172, y + 80), (x + 212, y + 84), (x + 252, y + 92), (x + 292, y + 98)]
    d.line(pts, fill=(235, 70, 60), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(240, 200, 90),
                  outline=(255, 255, 255))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(10, 20, 44))
    d.text((x + 10, y + h - 21), "KOSPI  4,708.54  ·  −161 PTS",
           font=SANS_B(12), fill=(255, 255, 255))


def hero_scene_guterres(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    # globe, fully inside the panel, right side
    cx, cy, r = x + w - 78, y + 56, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 205, 225),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 140, 170), width=1)
    d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(90, 140, 170), width=1)
    d.line([cx - r, cy - 16, cx + r, cy - 16], fill=(90, 140, 170), width=1)
    d.line([cx - r, cy + 16, cx + r, cy + 16], fill=(90, 140, 170), width=1)
    d.ellipse([cx - 18, cy - 30, cx + 2, cy - 12], fill=(90, 170, 90))
    d.ellipse([cx - 2, cy + 6, cx + 20, cy + 26], fill=(90, 170, 90))
    # flags, left side
    for i, col in enumerate([(200, 40, 40), (240, 200, 60), (60, 160, 90)]):
        fx = x + 22 + i * 52
        d.line([fx, y + 34, fx, y + 96], fill=(255, 255, 255), width=3)
        d.polygon([(fx, y + 34), (fx + 34, y + 42), (fx, y + 52)], fill=col)
    # podium trapezoid, bottom centre, clear of the label
    d.polygon([(x + 108, y + h - 8), (x + 138, y + h - 52),
               (x + 198, y + h - 52), (x + 228, y + h - 8)], fill=(122, 72, 20))
    d.text((x + 10, y + 8), "150 DELEGATES", font=SANS_B(22), fill=(240, 200, 60))
    lab = "UN · BRIDGETOWN"
    lf = SANS_B(12)
    d.text((x + w - 10 - d.textlength(lab, font=lf), y + h - 22), lab,
           font=lf, fill=(255, 255, 255))


def hero_scene_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    d.text((x + 10, y + 8), "NARROWEST SINCE 2018", font=SANS_B(13), fill=INK)
    gap = "GAP 5.3"
    gf = SANS_B(16)
    d.text((x + w - 10 - d.textlength(gap, font=gf), y + 6), gap, font=gf, fill=GOLD)
    base = y + h - 30
    bars = [("US", 78.9, NAVY, 0.62), ("CHINA", 73.6, RED, 0.56),
            ("INDIA", 40.5, GOLD, 0.30)]
    bw, gapx = 62, 34
    bx = x + 28
    for name, val, col, frac in bars:
        bh = int((h - 62) * frac) + 26
        top = base - bh
        d.rectangle([bx, top, bx + bw, base], fill=col)
        vlab = f"{val}"
        vf = SANS_B(15)
        d.text((bx + bw // 2 - d.textlength(vlab, font=vf) // 2, top + 6),
               vlab, font=vf, fill=(255, 255, 255))
        nlab = name
        nf = SANS_B(12)
        d.text((bx + bw // 2 - d.textlength(nlab, font=nf) // 2, base + 6),
               nlab, font=nf, fill=INK)
        bx += bw + gapx


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    X0, X1 = 16, 1008

    # ---- masthead ----
    d.text((X0, 2), "THE WORLD TODAY", font=SERIF_B(52), fill=INK)
    date = "MONDAY 23 NOVEMBER 2026"
    df = SANS_B(19)
    d.text((X1 - d.textlength(date, font=df), 20), date, font=df, fill=GOLD)
    d.line([X0, 62, X1, 62], fill=INK, width=2)

    # ---- kicker ----
    kick = ("AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at "
            "record low  ·  Anthropic IPO $107.3B")
    d.text((X0, 68), kick, font=SANS_B(15), fill=RED)
    d.line([X0, 90, X1, 90], fill=INK, width=1)

    # ---- number strip ----
    nums = [("−3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
            ("11,762", "EBOLA CASES, DRC", BROWN), ("$450M", "SKUBAL DEAL", GREEN),
            ("$107.3B", "ANTHROPIC IPO", PURPLE)]
    cw = (X1 - X0) // 5
    for i, (v, lab, col) in enumerate(nums):
        cx = X0 + i * cw
        d.text((cx + 4, 96), v, font=SANS_B(29), fill=col)
        d.text((cx + 4, 128), lab, font=SANS_B(11), fill=INK)
        if i:
            d.line([cx, 96, cx, 140], fill=(200, 192, 172), width=1)
    d.line([X0, 146, X1, 146], fill=INK, width=1)

    # ---- region bar ----
    regs = [("ASIA-PACIFIC 6", GREEN), ("AMERICAS 9", NAVY), ("MIDDLE EAST 6", BROWN),
            ("EUROPE 5", TEAL), ("AFRICA 3", OLIVE), ("WORLD 2", GREY)]
    rw = (X1 - X0) // 6
    for i, (lab, col) in enumerate(regs):
        rx = X0 + i * rw
        d.rectangle([rx, 148, rx + rw - 2, 168], fill=col)
        rf = SANS_B(12)
        d.text((rx + (rw - 2) // 2 - d.textlength(lab, font=rf) // 2, 153),
               lab, font=rf, fill=(255, 255, 255))

    # ---- the day in numbers ----
    d.text((X0, 174), "THE DAY IN NUMBERS", font=SANS_B(13), fill=INK)
    din = ("−5.8% INTRADAY LOW   ·   165 MISSILES IN A WEEK   ·   12,000 CLEARED"
           "   ·   264 KG SEIZED   ·   2% TAX BACKED")
    d.text((X0 + 168, 174), din, font=SANS(12), fill=INK)
    d.line([X0, 192, X1, 192], fill=INK, width=1)

    # ---- heroes ----
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi −3.3% to 4,708.54, sheds 161 pts; intraday −5.8%. Samsung −3.1%, "
         "SK Hynix −2.5%.", "KOREA EXCHANGE", "REPORTED", hero_scene_kospi),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges AI safety rules at Bridgetown; 150 delegates back a risk framework.", "UNITED NATIONS", "REPORTED",
         hero_scene_guterres),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since "
         "2018. India third at 40.5.", "LOWY INSTITUTE", "REPORTED",
         hero_scene_bars),
    ]
    hw, hgap = 320, 16
    hy, scene_h = 196, 120
    for i, (num, head, body, src, chp, scene_fn) in enumerate(heroes):
        hx = X0 + i * (hw + hgap)
        scene_fn(d, hx, hy, hw, scene_h)
        d.rectangle([hx, hy, hx + hw, hy + scene_h], outline=INK, width=1)
        # headline
        lines = wrap(d, head, SANS_B(17), hw - 12, 2)
        yy = hy + scene_h + 8
        for ln in lines:
            d.text((hx + 4, yy), ln, font=SANS_B(17), fill=INK)
            yy += 20
        # body
        blines = wrap(d, body, SANS(12), hw - 12, 2)
        yy += 2
        for ln in blines:
            d.text((hx + 4, yy), ln, font=SANS(12), fill=(40, 40, 40))
            yy += 15
        # source + chip row (fixed at panel bottom, clear of the cards row)
        sy = hy + scene_h + 88
        d.text((hx + 4, sy), src, font=SANS(10), fill=GREY)
        chip(d, hx + hw - 2, sy - 2, chp, NAVY)

    # ---- 10 cards ----
    cards = [
        ("4", "AMERICAS", NAVY, "BESSENT: NVIDIA ANSWERS",
         "Treasury chief wants to know of violations over China sales.", "Reuters", "REPORTED"),
        ("5", "FBI", NAVY, "FBI PROBES NCIC HACK",
         "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED"),
        ("6", "WHITE HOUSE", BROWN, "TRUMP: IRAN STRIKES MAY RESUME",
         "President says strikes could resume in the New Year.", "Reuters", "REPORTED"),
        ("7", "MARKETS", GOLD, "US FUTURES JUMP 3%",
         "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "Bloomberg", "REPORTED"),
        ("8", "SPORT", GREEN, "SKUBAL'S $450M METS DEAL",
         "Two-time Cy Young winner, nine years — largest ever for a pitcher.", "ESPN", "REPORTED"),
        ("9", "SPORT", GREEN, "TOM JACKSON DIES AT 75",
         "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED"),
        ("10", "LEGAL", PURPLE, "STATES SUE SPACEX",
         "Ten states challenge AI safety claims.", "AP", "REPORTED"),
        ("11", "TECH", PURPLE, "ANTHROPIC IPO: $107.3B",
         "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED"),
        ("12", "EUROPE", TEAL, "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE",
         "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM"),
        ("13", "SPACE", NAVY, "RUSSIAN NUCLEAR SATELLITE",
         "Intel claims Moscow built a satellite to carry a warhead.", "Reuters", "CLAIM"),
    ]
    colw, row_h, cgap = 192, 94, 8
    cy0 = 420
    for i, (num, cat, col, head, body, src, chp) in enumerate(cards):
        r, c = divmod(i, 5)
        cx = X0 + c * (colw + cgap)
        cy = cy0 + r * (row_h + 4)
        d.rectangle([cx, cy, cx + colw, cy + row_h], fill=(255, 255, 255),
                    outline=(190, 182, 162), width=1)
        d.rectangle([cx, cy, cx + colw, cy + 18], fill=col)
        d.text((cx + 6, cy + 3), f"{num}  {cat}", font=SANS_B(10),
               fill=(255, 255, 255))
        hl = wrap(d, head, SANS_B(12), colw - 12, 3)
        yy = cy + 22
        for ln in hl:
            d.text((cx + 6, yy), ln, font=SANS_B(12), fill=INK)
            yy += 14
        bl = wrap(d, body, SANS(10), colw - 12, 2)
        for ln in bl:
            d.text((cx + 6, yy), ln, font=SANS(10), fill=(50, 50, 50))
            yy += 12
        sy = cy + row_h - 16
        d.text((cx + 6, sy), src, font=SANS(9), fill=GREY)
        chip(d, cx + colw - 4, sy - 2, chp, RED if chp == "CLAIM" else NAVY)

    # ---- map + ALSO ----
    my0, my1 = 622, 846
    d.text((X0, my0), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    d.text((516, my0), "ALSO ON MONDAY", font=SANS_B(13), fill=INK)
    d.line([X0, my0 + 18, X1, my0 + 18], fill=INK, width=1)
    mx0, mx1, mtop, mbot = 16, 500, 644, 800
    d.rectangle([mx0, mtop, mx1, mbot], fill=SKY, outline=(190, 182, 162))
    for gx in range(mx0, mx1 + 1, 24):
        d.line([gx, mtop, gx, mbot], fill=(196, 216, 226), width=1)
    for gy in range(mtop, mbot + 1, 24):
        d.line([mx0, gy, mx1, gy], fill=(196, 216, 226), width=1)
    continents = [
        [(40, 668), (110, 648), (180, 652), (200, 678), (170, 712), (120, 726),
         (70, 706), (38, 688)],
        [(215, 640), (236, 636), (242, 650), (222, 656)],
        [(150, 742), (186, 736), (202, 766), (182, 792), (160, 788), (146, 760)],
        [(250, 650), (292, 640), (312, 654), (296, 672), (260, 672), (246, 662)],
        [(255, 686), (302, 682), (316, 710), (300, 748), (276, 752), (256, 722)],
        [(316, 644), (420, 634), (472, 652), (462, 688), (402, 706), (352, 696),
         (322, 672)],
        [(420, 758), (462, 752), (468, 772), (432, 782), (416, 770)],
    ]
    for poly in continents:
        d.polygon(poly, fill=LAND, outline=(120, 150, 90))
    pins = [(1, 456, 672, "Seoul"), (2, 168, 736, "Bridgetown"),
            (3, 428, 656, "Beijing"), (4, 128, 690, "Washington"),
            (5, 142, 676, "New York"), (6, 346, 672, "Tehran"),
            (7, 105, 668, "Chicago"), (8, 62, 692, "San Francisco"),
            (9, 85, 680, "Denver"), (10, 100, 706, "Austin"),
            (11, 288, 648, "Warsaw"), (12, 308, 664, "Kyiv"),
            (13, 330, 642, "Moscow")]
    for num, px, py, _name in pins:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        lab = str(num)
        d.text((px - d.textlength(lab, font=SANS_B(10)) // 2, py - 7), lab,
               font=SANS_B(10), fill=(255, 255, 255))
    legend = ("Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · "
              "5 New York · 6 Tehran · 7 Chicago · 8 San Francisco · 9 Denver · "
              "10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow")
    ll = wrap(d, legend, SANS(10), mx1 - mx0 - 4, 2)
    ly = mbot + 6
    for ln in ll:
        d.text((mx0 + 2, ly), ln, font=SANS(10), fill=(50, 50, 50))
        ly += 13

    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: the day after pact rejected",
        "18. Benghazi: UN demands port probe",
        "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike",
        "21. West Bank settler attacks",
        "22. Iran war: no deal in sight",
        "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt",
        "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if returns",
        "28. Seoul minister quits over exam chaos",
        "29. SK Telecom −7.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    ay = mtop + 4
    for i, item in enumerate(also):
        col = 0 if i < 9 else 1
        ax = 516 + col * 248
        ayy = mtop + 4 + (i % 9) * 20
        d.text((ax, ayy), "•  " + item, font=SANS(11), fill=INK)

    # ---- DATE CHECK ----
    dy0, dy1 = 852, 946
    d.rectangle([X0, dy0, X1, dy1], outline=RED, width=2)
    d.text((X0 + 8, dy0 + 6), "DATE CHECK", font=SANS_B(14), fill=RED)
    d.text((X0 + 118, dy0 + 7),
           "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY",
           font=SANS_B(11), fill=INK)
    left = ("LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II "
            "fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact "
            "(21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)")
    ly = dy0 + 28
    for ln in wrap(d, left, SANS(11), X1 - X0 - 16, 2):
        d.text((X0 + 8, ly), ln, font=SANS(11), fill=INK)
        ly += 15
    ny = ("NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · "
          "COP32 venue not set · WHO evacuating trapped Ebola staff")
    for ln in wrap(d, ny, SANS(11), X1 - X0 - 16, 2):
        d.text((X0 + 8, ly), ln, font=SANS(11), fill=INK)
        ly += 15

    # ---- footer ----
    fy = 952
    d.text((X0, fy), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · "
                     "NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=SANS(10), fill=GREY)
    d.text((X0, fy + 14), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's "
                          "claim, not independently confirmed · ONGOING = still developing",
           font=SANS(10), fill=GREY)
    d.text((X0, fy + 28), "Scenes are drawn illustrations, not photographs.  ·  "
                          "THE WORLD TODAY — Monday 23 November 2026  ·  31 stories  ·  "
                          "6 regions", font=SANS_B(10), fill=INK)

    out = os.path.join(BASE, "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
