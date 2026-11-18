#!/usr/bin/env python3
"""Generates NovaOS Plymouth boot-splash artwork (run from the assets/ folder):
background.png, logo.png, logo_small.png, wordmark.png, dot.png, progress.png,
icon.png and preview_mockup.png (a picture of what the boot screen looks like)."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG_TOP = (8, 10, 22)
BG_BOTTOM = (2, 3, 8)
CYAN = (93, 234, 212)
BLUE = (109, 139, 255)
PURPLE = (176, 109, 255)
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------- background.png (1920x1080 vertical gradient) ----------
W, H = 1920, 1080
bg = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(bg)
for y in range(H):
    d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOTTOM, y / H))
bg.save("background.png")

# ---------- logo.png (512x512, transparent circular emblem) ----------
S = 512
logo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
cx, cy = S // 2, S // 2

glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([cx - 220, cy - 220, cx + 220, cy + 220], fill=(125, 249, 255, 90))
glow = glow.filter(ImageFilter.GaussianBlur(40))
logo = Image.alpha_composite(logo, glow)
d = ImageDraw.Draw(logo)

ring_r = 188
steps = 240
for i in range(steps):
    t = i / steps
    color = lerp(CYAN, PURPLE, t) if t < 0.55 else lerp(BLUE, PURPLE, (t - 0.55) / 0.45)
    d.arc([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
          360 * i / steps, 360 * (i + 1.2) / steps, fill=color + (230,), width=6)

faint_r = 205
d.ellipse([cx - faint_r, cy - faint_r, cx + faint_r, cy + faint_r], outline=(150, 200, 255, 70), width=2)


def four_point_star(draw, center, size, fill):
    x, y = center
    draw.polygon([
        (x, y - size), (x + size * 0.26, y - size * 0.20),
        (x + size, y), (x + size * 0.26, y + size * 0.20),
        (x, y + size), (x - size * 0.26, y + size * 0.20),
        (x - size, y), (x - size * 0.26, y - size * 0.20),
    ], fill=fill)


four_point_star(d, (cx, cy - 178), 30, WHITE + (255,))
four_point_star(d, (cx - 152, cy - 96), 15, (191, 233, 255, 255))
four_point_star(d, (cx + 162, cy + 86), 12, (191, 233, 255, 255))

n_w, n_h, lw = 150, 170, 26
x0, y0 = cx - n_w // 2, cy - n_h // 2 + 18
for a, b in [((x0, y0 + n_h), (x0, y0)), ((x0, y0), (x0 + n_w, y0 + n_h)), ((x0 + n_w, y0 + n_h), (x0 + n_w, y0))]:
    d.line([a, b], fill=WHITE + (255,), width=lw, joint="curve")
for (px, py) in [(x0, y0 + n_h), (x0, y0), (x0 + n_w, y0 + n_h), (x0 + n_w, y0)]:
    d.ellipse([px - lw / 2, py - lw / 2, px + lw / 2, py + lw / 2], fill=WHITE + (255,))

logo.save("logo.png")
logo.resize((240, 240), Image.LANCZOS).save("logo_small.png")
logo.resize((256, 256), Image.LANCZOS).save("icon.png")

# ---------- wordmark.png ----------
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception:
    font = font_small = ImageFont.load_default()

word = Image.new("RGBA", (520, 120), (0, 0, 0, 0))
wd = ImageDraw.Draw(word)
bb = wd.textbbox((0, 0), "NovaOS", font=font)
wd.text(((520 - (bb[2] - bb[0])) / 2, 6), "NovaOS", font=font, fill=WHITE + (255,))
sub = "Debian GNU/Linux"
bb2 = wd.textbbox((0, 0), sub, font=font_small)
wd.text(((520 - (bb2[2] - bb2[0])) / 2, 88), sub, font=font_small, fill=(160, 190, 230, 230))
word.save("wordmark.png")

# ---------- dot.png (spinner dot) and progress.png (progress bar fill) ----------
dot = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
ImageDraw.Draw(dot).ellipse([2, 2, 18, 18], fill=(255, 255, 255, 255))
dot.save("dot.png")

prog = Image.new("RGBA", (64, 4), (0, 0, 0, 0))
pd = ImageDraw.Draw(prog)
for x in range(64):
    pd.line([(x, 0), (x, 3)], fill=lerp(CYAN, PURPLE, x / 63) + (255,))
prog.save("progress.png")

# ---------- preview_mockup.png: what the boot screen looks like ----------
# Layout numbers here match config/.../novaos/novaos.script (1920x1080 screen).
m = bg.convert("RGBA")
mx, my = W // 2, H // 2
m.alpha_composite(logo.resize((260, 260), Image.LANCZOS), (mx - 130, my - 220))
m.alpha_composite(word, (mx - word.width // 2, my + 90))
ring_cy, ring_rad, n, active = my + 290, 40, 8, 2
for i in range(n):
    ang = 2 * math.pi * i / n
    dd = dot.copy()
    if i != active:
        dd.putalpha(dd.split()[3].point(lambda p: int(p * 0.3)))
    m.alpha_composite(dd, (mx + int(math.sin(ang) * ring_rad) - 10, ring_cy + int(math.cos(ang) * ring_rad) - 10))
bar_w, bar_y = 320, H - 110
track = dot.resize((bar_w, 4))
track.putalpha(track.split()[3].point(lambda p: int(p * 0.12)))
m.alpha_composite(track, (mx - bar_w // 2, bar_y))
m.alpha_composite(prog.resize((int(bar_w * 0.45), 4)), (mx - bar_w // 2, bar_y))
m.convert("RGB").save("preview_mockup.png")

print("Assets generated.")
