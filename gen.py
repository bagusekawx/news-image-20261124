#!/usr/bin/env python3
"""Render the front page of The World Today - Tuesday, 24 November 2026.

Deterministic: fixed text, fixed layout, no randomness, no timestamps.
Writes entry.png next to this file (1024x1024, under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 40
INK = (18, 18, 18)
PAPER = (247, 243, 234)
GREY = (90, 86, 78)
ACCENT = (148, 28, 28)
RULE = (40, 40, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

F_MASTHEAD = font(SERIF_BOLD, 84)
F_DATE = font(SANS_BOLD, 19)
F_KICKER = font(SANS_BOLD, 17)
F_HEADLINE = font(SERIF_BOLD, 44)
F_DECK = font(SERIF, 22)
F_BODY = font(SERIF, 16)
F_STORY_HEAD = font(SERIF_BOLD, 24)
F_STORY_BODY = font(SERIF, 15)
F_TICKER_LABEL = font(SANS_BOLD, 15)
F_TICKER_VAL = font(SERIF_BOLD, 30)
F_FOOTER = font(SANS, 14)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=1.35):
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)
    return y + width


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cw = W - 2 * MARGIN  # content width: 944

    # ---- top thin rule + dateline strip ----
    y = 28
    y = rule(d, y, width=1)
    y += 6
    d.text((MARGIN, y), "VOL. I  —  No. 328", font=F_DATE, fill=GREY)
    right = "PRICE: FREE  •  ONE-PAGE EDITION"
    d.text((W - MARGIN - d.textlength(right, font=F_DATE), y), right,
           font=F_DATE, fill=GREY)
    y += 30
    y = rule(d, y, width=1)

    # ---- masthead ----
    y += 10
    title = "The World Today"
    d.text(((W - d.textlength(title, font=F_MASTHEAD)) / 2, y), title,
           font=F_MASTHEAD, fill=INK)
    y += 96

    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, y), date,
           font=F_DATE, fill=ACCENT)
    y += 30
    y = rule(d, y, width=4)
    y = rule(d, y + 3, width=1)

    # ---- lead kicker + headline ----
    y += 10
    d.text((MARGIN, y), "LEAD STORY  •  SILICON VALLEY", font=F_KICKER,
           fill=ACCENT)
    y += 24
    y = draw_wrapped(d, MARGIN, y,
                     "HUANG IS BACK: NVIDIA REINSTATES CHIEF AFTER 11 DAYS",
                     F_HEADLINE, cw, leading=1.12)
    y += 8

    # ---- lead deck ----
    y = draw_wrapped(d, MARGIN, y,
                     "Board reverses course under pressure from Trump and "
                     "Vance as Washington clears the chip giant of any "
                     "national security risk — and the market roars.",
                     F_DECK, cw, leading=1.3)
    y += 10
    y = rule(d, y, width=1)
    y += 10

    # ---- lead body, two columns ----
    col_w = (cw - 28) // 2
    lead_left = (
        "SANTA CLARA — Jensen Huang is chief executive of Nvidia again. "
        "Eleven days after the board pushed him out, directors voted on "
        "Monday to reinstate him, ending one of the strangest episodes in "
        "the chip industry's history."
    )
    lead_right = (
        "The reversal followed intense pressure from President Donald Trump "
        "and Vice President JD Vance, and a US government review that found "
        "\"no national security risk\" in Huang's leadership. Nvidia shares "
        "soared 31–33% and the Nasdaq jumped 6%."
    )
    y_left = draw_wrapped(d, MARGIN, y, lead_left, F_BODY, col_w)
    y_right = draw_wrapped(d, MARGIN + col_w + 28, y, lead_right, F_BODY,
                           col_w)
    y = max(y_left, y_right) + 10

    # ---- markets strip ----
    y = rule(d, y, width=1)
    y += 8
    d.text((MARGIN, y), "MARKETS", font=F_KICKER, fill=ACCENT)
    y += 24
    tickers = [("NVIDIA  (NVDA)", "+31–33%"),
               ("NASDAQ COMPOSITE", "+6%"),
               ("SK HYNIX  (US LISTING)", "+20%")]
    box_w = cw // 3
    for i, (label, val) in enumerate(tickers):
        x = MARGIN + i * box_w
        d.text((x, y), label, font=F_TICKER_LABEL, fill=GREY)
        d.text((x, y + 22), val, font=F_TICKER_VAL, fill=ACCENT)
        if i:
            d.line([(x - 14, y - 2), (x - 14, y + 52)], fill=GREY, width=1)
    y += 62
    y = rule(d, y, width=1)
    y += 10

    # ---- supporting stories: 2 columns x 3 rows ----
    stories = [
        ("US Blacklists Singapore Chip Firm Megaspeed",
         "Washington adds the Singapore chipmaker to its export blacklist, "
         "escalating the semiconductor fight."),
        ("Iran Strikes Gulf Sites as US Tightens Sanctions",
         "Tehran hits targets across the Gulf as Washington squeezes its "
         "oil trade with fresh sanctions."),
        ("Russian Jets Enter South Korea Air Defence Zone",
         "Warplanes cross into Seoul's air defence identification zone, "
         "drawing a scramble of fighter jets."),
        ("Russian Drone Attack on Kyiv Region Kills 11",
         "An overnight drone barrage on the Kyiv region leaves eleven dead "
         "and homes in ruins."),
        ("Ukraine Says It Sank a Russian Warship Off Libya",
         "Kyiv claims a strike on a Russian warship in the Mediterranean, "
         "far from the front lines."),
        ("Mexico Nabs 'El Chapo Isidro'",
         "Mexican forces capture Isidro Meza Flores, the cartel boss known "
         "as \"El Chapo Isidro\"."),
    ]
    row_h = 102
    for i, (head, body) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        sy = y + row * row_h
        sy = draw_wrapped(d, x, sy, head, F_STORY_HEAD, col_w, leading=1.15)
        sy += 4
        draw_wrapped(d, x, sy, body, F_STORY_BODY, col_w, leading=1.3)
    y += 3 * row_h + 2

    # ---- footer ----
    y = rule(d, y, width=2)
    y += 8
    foot = "The World Today  •  Tuesday, 24 November 2026  •  All the news of the day, on one page."
    d.text(((W - d.textlength(foot, font=F_FOOTER)) / 2, y), foot,
           font=F_FOOTER, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
