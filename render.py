#!/usr/bin/env python3
"""Paint a one-page newspaper front page summing up 26 November 2026.

The program draws the whole front page from scratch with Pillow and
saves it as entry.png in this directory: masthead and date line, a lead
story about Pakistan's first astronaut flying to China's space station
with a flat-illustration panel, six story cards with small pictogram
panels, and a news ticker along the bottom.

Everything is drawn in code. No photographs or external artwork are
used. The output is deterministic: running the script twice produces
byte-identical PNG files.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 36

PAPER = (247, 242, 231)
PAPER_CARD = (255, 252, 244)
INK = (22, 22, 22)
RED = (139, 26, 26)
NAVY = (18, 34, 66)
SKY = (52, 110, 168)
GOLD = (184, 134, 11)
MUTED = (96, 90, 78)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    width = draw.textlength(text, font=fnt)
    draw.text((cx - width / 2, y), text, font=fnt, fill=fill)


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------------------
# Pictograms: small flat illustrations drawn inside a coloured panel.
# ---------------------------------------------------------------------------

def pic_tank(draw, x, y, w, h):
    """A tank, for the war in Ukraine."""
    draw.rectangle([x, y, x + w, y + h], fill=(112, 116, 78))
    cx = x + w // 2
    # Hull and turret.
    draw.rounded_rectangle([cx - 52, y + h - 46, cx + 52, y + h - 22],
                           radius=6, fill=(58, 62, 40))
    draw.rounded_rectangle([cx - 26, y + h - 64, cx + 26, y + h - 44],
                           radius=5, fill=(74, 78, 50))
    # Barrel.
    draw.line([(cx + 24, y + h - 56), (cx + 78, y + h - 66)],
              fill=(58, 62, 40), width=6)
    # Wheels.
    for i in range(5):
        wx = cx - 40 + i * 20
        draw.ellipse([wx - 7, y + h - 20, wx + 7, y + h - 6],
                     fill=(38, 40, 26))
    # A small flag on the turret.
    draw.line([(cx - 8, y + h - 64), (cx - 8, y + h - 88)],
              fill=(38, 40, 26), width=3)
    draw.polygon([(cx - 8, y + h - 88), (cx + 14, y + h - 82),
                  (cx - 8, y + h - 76)], fill=(214, 178, 58))


def pic_shirt(draw, x, y, w, h):
    """A garment worker's shirt, for the Bangladesh pay rise."""
    draw.rectangle([x, y, x + w, y + h], fill=(44, 110, 112))
    cx = x + w // 2
    # Shirt body and sleeves.
    draw.polygon([(cx - 26, y + 18), (cx - 58, y + 34), (cx - 46, y + 62),
                  (cx - 34, y + 52), (cx - 34, y + h - 14),
                  (cx + 34, y + h - 14), (cx + 34, y + 52),
                  (cx + 46, y + 62), (cx + 58, y + 34),
                  (cx + 26, y + 18)],
                 fill=(250, 246, 236), outline=(30, 30, 30), width=2)
    # Collar.
    draw.polygon([(cx - 26, y + 18), (cx, y + 34), (cx + 26, y + 18)],
                 fill=(214, 178, 58))
    # Buttons and a stitched hem.
    for i in range(3):
        by = y + 46 + i * 16
        draw.ellipse([cx - 3, by - 3, cx + 3, by + 3], fill=(30, 30, 30))
    draw.line([(cx - 34, y + h - 22), (cx + 34, y + h - 22)],
              fill=(214, 178, 58), width=2)


def pic_dove(draw, x, y, w, h):
    """A dove with an olive branch, for ten years of peace in Colombia."""
    draw.rectangle([x, y, x + w, y + h], fill=(126, 164, 196))
    cx = x + w // 2
    cy = y + h // 2
    # Olive branch.
    draw.line([(cx - 70, y + h - 18), (cx + 20, cy + 18)],
              fill=(46, 96, 52), width=3)
    for i in range(4):
        lx = cx - 60 + i * 18
        ly = y + h - 22 - i * 9
        draw.ellipse([lx - 7, ly - 4, lx + 7, ly + 4], fill=(62, 122, 66))
    # Dove body, wing and head.
    draw.ellipse([cx - 52, cy - 16, cx + 34, cy + 22], fill=(250, 250, 248))
    draw.ellipse([cx - 34, cy - 12, cx + 6, cy + 14], fill=(228, 228, 222))
    draw.ellipse([cx + 22, cy - 30, cx + 52, cy - 2], fill=(250, 250, 248))
    draw.polygon([(cx + 50, cy - 18), (cx + 66, cy - 12), (cx + 50, cy - 8)],
                 fill=(214, 138, 44))
    draw.ellipse([cx + 36, cy - 24, cx + 42, cy - 18], fill=(30, 30, 30))
    # Tail feathers.
    draw.polygon([(cx - 50, cy + 2), (cx - 84, cy + 26), (cx - 48, cy + 22)],
                 fill=(238, 238, 234))


def pic_flag(draw, x, y, w, h):
    """A flag crossed out, for North Korea shutting Switzerland's office."""
    draw.rectangle([x, y, x + w, y + h], fill=(188, 176, 152))
    cx = x + w // 2
    cy = y + h // 2
    # Flag pole and flag.
    draw.line([(cx - 20, y + 14), (cx - 20, y + h - 12)],
              fill=(60, 52, 44), width=4)
    draw.rectangle([cx - 20, y + 18, cx + 46, y + 48], fill=(178, 42, 42))
    draw.rectangle([cx - 20, y + 48, cx + 46, y + 52], fill=(250, 246, 236))
    # A small building (the office) at the base.
    draw.rectangle([cx - 52, cy + 12, cx + 52, y + h - 12],
                   fill=(96, 88, 76))
    for i in range(3):
        wx = cx - 40 + i * 30
        draw.rectangle([wx, cy + 22, wx + 16, cy + 38], fill=(247, 242, 231))
    # Red prohibition circle over the flag.
    draw.ellipse([cx - 46, y + 4, cx + 72, y + 74],
                 outline=(178, 42, 42), width=6)
    draw.line([(cx - 36, y + 14), (cx + 62, y + 64)],
              fill=(178, 42, 42), width=6)


def pic_turkey(draw, x, y, w, h):
    """A turkey, for Thanksgiving in the United States."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 106, 44))
    cx = x + w // 2
    cy = y + h // 2 + 8
    # Tail fan.
    for angle in (-52, -26, 0, 26, 52):
        rad = math.radians(angle - 90)
        tx = cx + 44 * math.cos(rad)
        ty = cy - 6 + 44 * math.sin(rad)
        draw.ellipse([tx - 16, ty - 26, tx + 16, ty + 26],
                     fill=(122, 66, 28), outline=(214, 178, 58), width=2)
    # Body and head.
    draw.ellipse([cx - 30, cy - 16, cx + 30, cy + 30], fill=(96, 58, 30))
    draw.ellipse([cx - 12, cy - 40, cx + 16, cy - 12], fill=(122, 76, 38))
    draw.polygon([(cx + 14, cy - 28), (cx + 26, cy - 24), (cx + 14, cy - 20)],
                 fill=(214, 138, 44))
    draw.ellipse([cx + 2, cy - 34, cx + 8, cy - 28], fill=(30, 30, 30))
    # Wattle.
    draw.ellipse([cx + 8, cy - 20, cx + 16, cy - 8], fill=(178, 42, 42))


def pic_chess(draw, x, y, w, h):
    """A chess king, for Gukesh defending his world title."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 84, 62))
    cx = x + w // 2
    # Cross on top of the crown.
    draw.rectangle([cx - 4, y + 12, cx + 4, y + 34], fill=(240, 232, 214))
    draw.rectangle([cx - 12, y + 18, cx + 12, y + 26], fill=(240, 232, 214))
    # Crown, stem and base.
    draw.polygon([(cx - 16, y + 34), (cx - 24, y + 50), (cx + 24, y + 50),
                  (cx + 16, y + 34)], fill=(240, 232, 214))
    draw.rectangle([cx - 10, y + 50, cx + 10, y + 66], fill=(240, 232, 214))
    draw.polygon([(cx - 22, y + 66), (cx + 22, y + 66), (cx + 30, y + 84),
                  (cx - 30, y + 84)], fill=(240, 232, 214))
    draw.rectangle([cx - 34, y + 84, cx + 34, y + 92], fill=(214, 178, 58))
    # A pawn beside the king.
    draw.ellipse([cx + 44, y + 58, cx + 62, y + 76], fill=(214, 178, 58))
    draw.rectangle([cx + 48, y + 76, cx + 58, y + 88], fill=(214, 178, 58))
    draw.rectangle([cx + 42, y + 88, cx + 64, y + 92], fill=(214, 178, 58))


# ---------------------------------------------------------------------------
# Lead illustration: rocket, space station and the curve of the Earth.
# ---------------------------------------------------------------------------

def draw_lead_panel(draw, x, y, w, h):
    # Draw on a separate panel image so the Earth curve is clipped to
    # the panel instead of spilling over the story cards below it.
    panel = Image.new("RGB", (w, h), NAVY)
    p = ImageDraw.Draw(panel)
    draw = p
    x = 0
    y = 0
    # Fixed stars, so the picture is identical on every run.
    stars = [(18, 16, 2), (70, 44, 1), (120, 12, 2), (168, 58, 1),
             (210, 22, 2), (262, 48, 1), (306, 14, 2), (348, 40, 1),
             (392, 18, 2), (40, 96, 1), (150, 108, 1), (330, 92, 1),
             (240, 130, 1), (90, 140, 2), (380, 128, 1)]
    for sx, sy, sr in stars:
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(255, 255, 255))
    # The curve of the Earth along the bottom of the panel.
    earth_cx = x + w // 2 + 90
    earth_cy = y + h + 190
    earth_r = 250
    draw.ellipse([earth_cx - earth_r, earth_cy - earth_r,
                  earth_cx + earth_r, earth_cy + earth_r],
                 fill=SKY, outline=(214, 178, 58), width=3)
    draw.ellipse([earth_cx - 150, earth_cy - 235, earth_cx - 60,
                  earth_cy - 195], fill=(62, 122, 66))
    draw.ellipse([earth_cx + 40, earth_cy - 225, earth_cx + 130,
                  earth_cy - 190], fill=(62, 122, 66))
    # Space station: central module, side modules and solar panels.
    sx = x + 24
    sy = y + 108
    draw.rectangle([sx, sy + 8, sx + 150, sy + 26], fill=(200, 204, 210))
    draw.rectangle([sx + 52, sy, sx + 98, sy + 34], fill=(224, 228, 232))
    draw.rectangle([sx - 26, sy + 10, sx, sy + 24], fill=(120, 140, 170))
    draw.rectangle([sx + 150, sy + 10, sx + 176, sy + 24],
                   fill=(120, 140, 170))
    draw.line([(sx + 30, sy + 17), (sx - 26, sy + 17)], fill=(90, 96, 110),
              width=2)
    draw.line([(sx + 120, sy + 17), (sx + 176, sy + 17)], fill=(90, 96, 110),
              width=2)
    for px in (sx - 26, sx + 150):
        draw.rectangle([px, sy - 6, px + 26, sy + 40], fill=(52, 96, 168))
        draw.line([(px + 13, sy - 6), (px + 13, sy + 40)],
                  fill=(120, 170, 220), width=1)
    # Rocket climbing past the station, tilted 30 degrees.
    rx, ry = x + w - 118, y + 26
    angle = math.radians(-30)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    def rot(px, py):
        return (rx + px * cos_a - py * sin_a,
                ry + px * sin_a + py * cos_a)

    body = [rot(px, py) for px, py in
            [(-12, 0), (12, 0), (12, 52), (-12, 52)]]
    nose = [rot(px, py) for px, py in [(-12, 0), (0, -26), (12, 0)]]
    fin_l = [rot(px, py) for px, py in [(-12, 52), (-26, 76), (-12, 66)]]
    fin_r = [rot(px, py) for px, py in [(12, 52), (26, 76), (12, 66)]]
    flame = [rot(px, py) for px, py in
             [(-8, 66), (0, 96), (8, 66)]]
    draw.polygon(flame, fill=(232, 128, 32))
    draw.polygon(fin_l, fill=(178, 42, 42))
    draw.polygon(fin_r, fill=(178, 42, 42))
    draw.polygon(body, fill=(240, 240, 238))
    draw.polygon(nose, fill=(178, 42, 42))
    window = rot(0, 22)
    draw.ellipse([window[0] - 7, window[1] - 7, window[0] + 7, window[1] + 7],
                 fill=SKY, outline=(30, 30, 30), width=2)
    # A small moon.
    draw.ellipse([x + 18, y + 22, x + 44, y + 48], fill=(232, 228, 214))
    return panel


# ---------------------------------------------------------------------------
# Story cards.
# ---------------------------------------------------------------------------

STORIES = [
    ("WAR IN UKRAINE",
     "Russia's own toll nears 500,000",
     "Moscow's data shows almost half a million lost, as the US shelves "
     "business-deal peace plans.",
     pic_tank),
    ("LABOUR · ASIA",
     "Garment workers win 36% pay rise",
     "Bangladesh raises the minimum wage for entry-level garment workers "
     "by more than a third.",
     pic_shirt),
    ("PEACE · AMERICAS",
     "Colombia marks a decade of peace",
     "Ten years on, the UN warns commitments remain unfinished; police "
     "free 20 hostages in a raid.",
     pic_dove),
    ("DIPLOMACY · ASIA",
     "North Korea shuts Switzerland's office",
     "Pyongyang tells Switzerland to close its new office, shutting a "
     "rare channel to the West.",
     pic_flag),
    ("UNITED STATES",
     "Thanksgiving under storm clouds",
     "Americans gather for Thanksgiving as a powerful storm threatens "
     "the East Coast with flooding.",
     pic_turkey),
    ("SPORT · CHESS",
     "Gukesh defends chess crown",
     "World champion D. Gukesh of India faces Uzbekistan's Javokhir "
     "Sindarov for the 2026 title.",
     pic_chess),
]


def draw_card(draw, x, y, w, h, kicker, headline, standfirst, pic_fn):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER_CARD,
                   outline=(120, 112, 96), width=1)
    pic_h = 84
    pic_fn(draw, x + 1, y + 1, w - 2, pic_h)
    text_x = x + 12
    text_w = w - 24
    cy = y + pic_h + 8
    draw.text((text_x, cy), kicker, font=font(SANS_BOLD, 14), fill=RED)
    cy += 21
    for line in wrap_text(draw, headline, font(SERIF_BOLD, 20), text_w):
        draw.text((text_x, cy), line, font=font(SERIF_BOLD, 20), fill=INK)
        cy += 24
    cy += 3
    for line in wrap_text(draw, standfirst, font(SERIF, 14), text_w):
        draw.text((text_x, cy), line, font=font(SERIF, 14), fill=(52, 48, 42))
        cy += 18


# ---------------------------------------------------------------------------
# Front page assembly.
# ---------------------------------------------------------------------------

def build():
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    left = MARGIN
    right = WIDTH - MARGIN
    centre = WIDTH // 2

    # Masthead.
    rule(draw, left, right, 26, width=3)
    masthead = font(SERIF_BOLD, 58)
    draw_centered(draw, centre, 36, "THE WORLD IN ONE PAGE", masthead, INK)
    rule(draw, left, right, 108, width=2)

    # Date line and subtitle.
    draw_centered(draw, centre, 122, "THURSDAY, 26 NOVEMBER 2026",
                  font(SANS_BOLD, 19), INK)
    draw_centered(draw, centre, 148,
                  "The day's world news — in a single picture",
                  font(SERIF_ITALIC, 19), MUTED)

    # Lead story: text on the left, illustration on the right.
    lead_y = 182
    lead_h = 244
    lead_text_w = 520
    draw.text((left, lead_y), "SPACE · ASIA",
              font=font(SANS_BOLD, 17), fill=RED)
    lead_head = font(SERIF_BOLD, 38)
    cy = lead_y + 28
    headline = ("Pakistan's first astronaut to fly to China's "
                "space station")
    for line in wrap_text(draw, headline, lead_head, lead_text_w):
        draw.text((left, cy), line, font=lead_head, fill=INK)
        cy += 46
    cy += 6
    standfirst = ("Muhammad Zeeshan Ali will become the first foreign "
                  "astronaut to visit Tiangong, flying aboard "
                  "Shenzhou-24 — a first for Pakistan and a new "
                  "chapter for China's station.")
    for line in wrap_text(draw, standfirst, font(SERIF, 19), lead_text_w):
        draw.text((left, cy), line, font=font(SERIF, 19), fill=(52, 48, 42))
        cy += 25
    panel = draw_lead_panel(draw, left + 536, lead_y, 412, lead_h)
    image.paste(panel, (left + 536, lead_y))

    # Six story cards in two rows of three.
    card_w = 306
    card_h = 226
    gap = 16
    row1_y = 444
    row2_y = 686
    for i, (kicker, headline, standfirst, pic_fn) in enumerate(STORIES):
        col = i % 3
        row = i // 3
        cx = left + col * (card_w + gap)
        cy = row1_y if row == 0 else row2_y
        draw_card(draw, cx, cy, card_w, card_h, kicker, headline,
                  standfirst, pic_fn)

    # Bottom ticker.
    ticker_y = 930
    ticker_h = 66
    draw.rectangle([left, ticker_y, right, ticker_y + ticker_h],
                   fill=(30, 28, 26))
    ticker = ("Petrobras unveils a $122bn plan  ·  "
              "Venezuela reveals $237.5bn debt  ·  Australia–Solomon "
              "Islands security pact  ·  India marks Constitution Day  ·  "
              "US plans new tariffs  ·  Real Madrid rout PSV")
    ticker_font = font(SANS, 16)
    lead_in = "ALSO TODAY  ·  "
    lead_in_font = font(SANS_BOLD, 16)
    lines = wrap_text(draw, ticker, ticker_font,
                      right - left - 28 - draw.textlength(lead_in,
                                                          font=lead_in_font))
    ty = ticker_y + 12
    for i, line in enumerate(lines):
        if i == 0:
            # First line starts with a bold gold lead-in, measured so the
            # two segments sit side by side with no overlap.
            lead_w = draw.textlength(lead_in, font=lead_in_font)
            rest_w = draw.textlength(line, font=ticker_font)
            lx = centre - (lead_w + rest_w) / 2
            draw.text((lx, ty), lead_in, font=lead_in_font,
                      fill=(232, 196, 90))
            draw.text((lx + lead_w, ty), line, font=ticker_font,
                      fill=(247, 242, 231))
        else:
            draw_centered(draw, centre, ty, line, ticker_font,
                          (247, 242, 231))
        ty += 21

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    image.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":
    print(build())
