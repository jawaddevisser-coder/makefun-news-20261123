#!/usr/bin/env python3
"""Draw "The World Tonight" — a one-day world news poster for Monday 23 November 2026.

Deterministic Pillow drawing: same input always produces the same PNG bytes.
Style: evening bulletin — deep navy, gold rules, red lead banner, six story cards
with simple pictogram icons drawn from primitives. No external images, no fonts
beyond the DejaVu family shipped with the system.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (15, 29, 51)        # background
PANEL = (27, 47, 77)       # card background
PANEL_EDGE = (58, 84, 120) # card border
CREAM = (244, 239, 230)    # headline text
MUTED = (196, 208, 224)    # body text
FAINT = (140, 156, 178)    # footer text
GOLD = (217, 164, 65)      # rules and date
RED = (203, 60, 48)        # lead accent
TEAL = (46, 160, 150)
GREEN = (76, 170, 90)
BLUE = (70, 130, 200)
ORANGE = (214, 130, 44)
PURPLE = (150, 110, 190)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
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
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------- pictograms, drawn in dark navy on a solid accent disc ----------
def icon_building(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    # two building blocks, one cracked
    d.rectangle([cx - 22, cy - 8, cx - 2, cy + 20], fill=NAVY)
    d.rectangle([cx + 2, cy - 18, cx + 22, cy + 20], fill=NAVY)
    d.line([(cx - 2, cy - 18), (cx + 6, cy - 8), (cx - 1, cy + 2), (cx + 8, cy + 12)],
           fill=PANEL, width=2)
    for wx in (-17, -7):
        d.rectangle([wx + cx - 4, cy - 2, wx + cx + 2, cy + 4], fill=PANEL)
    for wx in (8, 16):
        d.rectangle([wx + cx - 3, cy - 12, wx + cx + 3, cy - 6], fill=PANEL)


def icon_ship(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    d.polygon([(cx - 24, cy + 4), (cx + 24, cy + 4), (cx + 16, cy + 18), (cx - 16, cy + 18)],
              fill=NAVY)
    d.rectangle([cx - 2, cy - 20, cx + 2, cy + 4], fill=NAVY)
    d.polygon([(cx + 2, cy - 20), (cx + 16, cy - 8), (cx + 2, cy - 8)], fill=NAVY)
    d.arc([cx - 28, cy + 20, cx - 4, cy + 30], 0, 180, fill=NAVY, width=3)
    d.arc([cx + 4, cy + 20, cx + 28, cy + 30], 0, 180, fill=NAVY, width=3)


def icon_bars(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    bars = [(-20, 8), (-7, -2), (6, -12)]
    for bx, top in bars:
        d.rectangle([cx + bx, cy + top, cx + bx + 9, cy + 18], fill=NAVY)
    d.line([(cx - 24, cy - 14), (cx - 4, cy - 20), (cx + 24, cy - 26)], fill=NAVY, width=3)
    d.polygon([(cx + 24, cy - 26), (cx + 14, cy - 26), (cx + 24, cy - 16)], fill=NAVY)


def icon_candles(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    for cx0, top, bot, wick_t, wick_b in [(-18, -6, 8, -16, 16), (-2, -14, 2, -22, 12), (14, -2, 12, -12, 20)]:
        d.line([(cx + cx0 + 4, cy + wick_t), (cx + cx0 + 4, cy + wick_b)], fill=NAVY, width=2)
        d.rectangle([cx + cx0, cy + top, cx + cx0 + 8, cy + bot], fill=NAVY)


def icon_train(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    d.rounded_rectangle([cx - 24, cy - 16, cx + 24, cy + 12], radius=6, fill=NAVY)
    d.rectangle([cx - 18, cy - 10, cx - 4, cy + 0], fill=PANEL)
    d.rectangle([cx + 4, cy - 10, cx + 18, cy + 0], fill=PANEL)
    d.ellipse([cx - 14, cy + 10, cx - 4, cy + 20], fill=NAVY)
    d.ellipse([cx + 4, cy + 10, cx + 14, cy + 20], fill=NAVY)
    d.line([(cx - 28, cy + 24), (cx + 28, cy + 24)], fill=NAVY, width=3)


def icon_note(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    d.ellipse([cx - 16, cy + 8, cx - 2, cy + 20], fill=NAVY)
    d.rectangle([cx - 4, cy - 20, cx + 0, cy + 14], fill=NAVY)
    d.polygon([(cx - 4, cy - 20), (cx + 16, cy - 12), (cx + 16, cy - 2), (cx - 4, cy - 10)],
              fill=NAVY)


ICONS = {
    "building": icon_building,
    "ship": icon_ship,
    "bars": icon_bars,
    "candles": icon_candles,
    "train": icon_train,
    "note": icon_note,
}

# ---------- stories: (kicker, accent, icon, headline, summary) ----------
LEAD = ("UKRAINE", RED, "building",
        "15 KILLED IN OVERNIGHT STRIKES",
        "Russian drones hit homes in the Kyiv region; a block of flats collapses "
        "in Dymer, killing 11, as rescuers dig for survivors.")

CARDS = [
    ("LIBYA", TEAL, "ship",
     "KYIV SAYS IT SANK A RUSSIAN WARSHIP",
     "Zelenskyy says seven sea drones sank the corvette Merkury at Benghazi."),
    ("SOUTH KOREA", GREEN, "bars",
     "KOREA'S EXPORTS MORE THAN DOUBLE",
     "Nov 1-20 exports hit a record $77.4bn, up 101%, as chips nearly quadruple."),
    ("MARKETS", BLUE, "candles",
     "WALL ST REBOUNDS AFTER ROUT",
     "S&P futures jump 2.2% and Nasdaq 3% early Monday after last week's tech rout."),
    ("INDIA", ORANGE, "train",
     "MODI AND NEPAL PM UNVEIL TRAIN",
     "Balen Shah gets a ceremonial welcome in Delhi; 100-minute talks, then a new train."),
]

BOTTOM = ("AUSTRALIA", PURPLE, "note",
          "MOLLY MELDRUM, 83, DIES",
          "Australian music legend behind Countdown \u2014 champion of AC/DC and "
          "Kylie Minogue \u2014 dies in Melbourne after a long illness.")


def kicker_tag(d, x, y, text, accent):
    f = font(SANS_B, 15)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 18, y + 24], radius=4, fill=accent)
    d.text((x + 9, y + 4), text, font=f, fill=(255, 255, 255))


def story_card(d, x, y, w, h, kicker, accent, icon, headline, summary,
               head_size=27, body_size=17):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL,
                        outline=PANEL_EDGE, width=1)
    kicker_tag(d, x + 16, y + 14, kicker, accent)
    ICONS[icon](d, x + w - 40, y + 40, 26, accent)
    hf = font(SERIF_B, head_size)
    lines = wrap(d, headline, hf, w - 110)
    draw_lines(d, x + 16, y + 48, lines[:2], hf, CREAM, head_size + 6)
    bf = font(SANS, body_size)
    blines = wrap(d, summary, bf, w - 32)
    draw_lines(d, x + 16, y + 48 + min(len(lines), 2) * (head_size + 6) + 8,
               blines[:2], bf, MUTED, body_size + 6)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # gold hairline frame
    d.rectangle([14, 14, W - 15, H - 15], outline=GOLD, width=2)

    # masthead
    title_f = font(SERIF_B, 56)
    title = "THE WORLD TONIGHT"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 34), title, font=title_f, fill=CREAM)
    date_f = font(SANS_B, 25)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 106), date, font=date_f, fill=GOLD)
    sub_f = font(SANS, 16)
    sub = "SIX STORIES FROM AROUND THE WORLD"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 138), sub, font=sub_f, fill=FAINT)
    d.line([(36, 164), (W - 36, 164)], fill=GOLD, width=2)

    # lead story
    lx, ly, lw, lh = 36, 180, W - 72, 146
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=PANEL,
                        outline=PANEL_EDGE, width=1)
    d.rectangle([lx, ly + 6, lx + 8, ly + lh - 6], fill=RED)
    kicker_tag(d, lx + 24, ly + 12, LEAD[0], RED)
    ICONS[LEAD[2]](d, lx + lw - 46, ly + 44, 30, RED)
    hf = font(SERIF_B, 33)
    lines = wrap(d, LEAD[3], hf, lw - 140)
    draw_lines(d, lx + 24, ly + 44, lines[:1], hf, CREAM, 40)
    bf = font(SANS, 19)
    blines = wrap(d, LEAD[4], bf, lw - 140)
    draw_lines(d, lx + 24, ly + 44 + 40 + 6, blines[:2], bf, MUTED, 25)

    # 2 x 2 grid
    gx, gy = 36, 340
    cw, ch, gap = 468, 190, 14
    for i, (kicker, accent, icon, headline, summary) in enumerate(CARDS):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        story_card(d, cx, cy, cw, ch, kicker, accent, icon, headline, summary)

    # bottom wide card (obituary)
    bx, by, bw, bh = 36, 748, W - 72, 150
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=PANEL,
                        outline=PANEL_EDGE, width=1)
    kicker_tag(d, bx + 16, by + 14, BOTTOM[0], PURPLE)
    ICONS[BOTTOM[2]](d, bx + bw - 46, by + 52, 30, PURPLE)
    hf = font(SERIF_B, 30)
    d.text((bx + 16, by + 48), BOTTOM[3], font=hf, fill=CREAM)
    bf = font(SANS, 19)
    blines = wrap(d, BOTTOM[4], bf, bw - 150)
    draw_lines(d, bx + 16, by + 48 + 38 + 8, blines[:2], bf, MUTED, 25)

    # footer
    d.line([(36, 914), (W - 36, 914)], fill=GOLD, width=1)
    ff = font(SANS, 15)
    src = "Sources: Reuters  ·  Al Jazeera  ·  Korea JoongAng Daily  ·  IANS  ·  AAP"
    sw = d.textlength(src, font=ff)
    d.text(((W - sw) / 2, 930), src, font=ff, fill=FAINT)
    note = "All six stories happened or were first reported on Monday 23 November 2026."
    nw = d.textlength(note, font=ff)
    d.text(((W - nw) / 2, 954), note, font=ff, fill=FAINT)
    foot_f = font(SANS_B, 14)
    foot = "THE WORLD TONIGHT  ·  MONDAY 23 NOVEMBER 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 986), foot, font=foot_f, fill=GOLD)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
