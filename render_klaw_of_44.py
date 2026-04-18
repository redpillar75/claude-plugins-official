"""
KLAW OF 44 – RED PILLAR  |  Motion Graphics Video Renderer
Generates a 1920×1080 MP4 at 60 fps using Pillow + imageio (or OpenCV).

Install deps:
    pip install Pillow imageio imageio-ffmpeg numpy
"""

import math
import random
import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ─── Constants ────────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 60
TOTAL  = 10 * FPS   # 10-second clip (600 frames)
OUTPUT = "klaw_of_44.mp4"

# ─── Palette (R, G, B) ───────────────────────────────────────────
BG      = (0,   0,   8)
RED     = (255, 0,   51)
RED_DIM = (136, 0,   34)
BLUE    = (0,   119, 255)
BLU_DIM = (0,   51,  136)
PURPLE  = (136, 0,   255)
PUR_DIM = (68,  0,   136)
GOLD    = (255, 215, 0)
GOLD_D  = (153, 102, 0)
WHITE   = (255, 255, 255)
CYAN    = (0,   204, 255)

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out(v):
    v = max(0.0, min(1.0, v))
    return 1.0 - (1.0 - v) ** 2

def phase(t, start, end):
    return max(0.0, min(1.0, (t - start) / max(end - start, 1)))

def blend_colors(c1, c2, alpha):
    return tuple(int(a + (b - a) * alpha) for a, b in zip(c1, c2))

def add_alpha(color, a):
    return (*color, int(a * 255))

# ─── Glow helper (Gaussian blur on a temp layer) ─────────────────
def draw_glow_text(draw_base, img_base, text, xy, font, color, glow_radius=30, glow_alpha=0.7):
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td  = ImageDraw.Draw(tmp)
    td.text(xy, text, font=font, fill=add_alpha(color, 1.0), anchor="mm")
    blurred = tmp.filter(ImageFilter.GaussianBlur(radius=glow_radius))
    # composite glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.paste(blurred, (0, 0))
    # tint glow with color
    img_base.alpha_composite(glow, dest=(0, 0))
    # sharp text on top
    draw_base.text(xy, text, font=font, fill=add_alpha(color, 1.0), anchor="mm")

def draw_outline_text(draw, text, xy, font, stroke_color, stroke_width=4, alpha=1.0):
    draw.text(xy, text, font=font, fill=add_alpha(stroke_color, alpha),
              stroke_width=stroke_width, stroke_fill=add_alpha(stroke_color, alpha),
              anchor="mm")

# ─── Grid ─────────────────────────────────────────────────────────
def draw_grid(draw, alpha):
    if alpha <= 0.02:
        return
    vp_y  = H // 2
    cx    = W // 2
    space = 80
    color = (*BLU_DIM, int(alpha * 60))
    # horizon horizontal lines
    for row in range(1, 15):
        y = vp_y + row * space
        if y > H:
            break
        a = int(alpha * (row / 15) * 80)
        draw.line([(0, y), (W, y)], fill=(*BLUE, a), width=1)
    # vertical perspective lines
    for col in range(-14, 15):
        bx = cx + col * space
        draw.line([(cx, vp_y), (bx, H)], fill=(*BLUE, int(alpha * 40)), width=1)

# ─── Arc helper ───────────────────────────────────────────────────
def draw_arc(draw, cx, cy, r, start_deg, end_deg, color, alpha, width=2):
    if alpha <= 0.02 or r <= 0:
        return
    bbox = [cx - r, cy - r, cx + r, cy + r]
    draw.arc(bbox, start=start_deg, end=end_deg,
             fill=(*color, int(alpha * 255)), width=width)

# ─── Hex ring ─────────────────────────────────────────────────────
def draw_hex_ring(draw, cx, cy, r, color, alpha, width=2):
    if alpha <= 0.02 or r <= 0:
        return
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    draw.line(pts, fill=(*color, int(alpha * 255)), width=width)

# ─── Corner brackets ──────────────────────────────────────────────
def draw_corners(draw, alpha):
    if alpha <= 0.02:
        return
    c = (*GOLD, int(alpha * 255))
    pad, blen, w = 40, 80, 3
    corners = [
        (pad, pad, 1, 1),
        (W - pad, pad, -1, 1),
        (pad, H - pad, 1, -1),
        (W - pad, H - pad, -1, -1),
    ]
    for (x, y, dx, dy) in corners:
        draw.line([(x, y + dy * blen), (x, y), (x + dx * blen, y)], fill=c, width=w)

# ─── Divider ──────────────────────────────────────────────────────
def draw_divider(img, y_pos, alpha):
    if alpha <= 0.02:
        return
    tmp  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td   = ImageDraw.Draw(tmp)
    # draw a thin gold line
    td.line([(0, y_pos), (W, y_pos)], fill=(*GOLD, int(alpha * 220)), width=2)
    blurred = tmp.filter(ImageFilter.GaussianBlur(radius=6))
    img.alpha_composite(blurred)

# ─── Scanlines ───────────────────────────────────────────────────
def draw_scanlines(draw):
    for y in range(0, H, 4):
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, 16), width=2)

# ─── Load / create fonts ──────────────────────────────────────────
def load_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/liberation/LiberationMono-Bold.ttf", size)
        except Exception:
            return ImageFont.load_default()

FONT_LG  = load_font(180)
FONT_MD  = load_font(90)
FONT_SM  = load_font(28)
FONT_XS  = load_font(14)

# ─── Particle system ─────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, angle, speed, color, life):
        self.x, self.y = x, y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life  = life
        self.maxLife = life
        self.size = random.uniform(1.5, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.vx *= 0.97
        self.life -= 1
        return self.life > 0

    def draw(self, draw):
        a = self.life / self.maxLife
        r = max(1, int(self.size * a))
        c = (*self.color, int(a * 200))
        bbox = [self.x - r, self.y - r, self.x + r, self.y + r]
        draw.ellipse(bbox, fill=c)

def make_burst(x, y, count, colors, particles):
    for i in range(count):
        angle = (math.pi * 2 * i) / count + random.uniform(-0.3, 0.3)
        speed = random.uniform(2, 10)
        color = random.choice(colors)
        life  = random.randint(40, 90)
        particles.append(Particle(x, y, angle, speed, color, life))

# ─── Render a single frame ────────────────────────────────────────
def render_frame(t, particles):
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2

    # ---- Grid
    draw_grid(draw, ease_out(phase(t, 0, 60)) * 0.5)

    # ---- Energy arcs (3 rings)
    p1 = ease_out(phase(t, 20, 80))
    for i, (r, col) in enumerate(zip([300, 250, 200], [PURPLE, BLUE, RED])):
        angle_deg = math.degrees(t * 0.02 + i * (math.pi / 1.5))
        draw_arc(draw, cx, cy, int(r * p1),
                 angle_deg % 360, (angle_deg + 234) % 360,
                 col, p1 * 0.8, 3 - i)

    # ---- Hex rings
    p2 = ease_out(phase(t, 30, 100))
    draw_hex_ring(draw, cx, cy, int(380 * p2), GOLD,   p2 * 0.7, 2)
    draw_hex_ring(draw, cx, cy, int(340 * p2), PURPLE, p2 * 0.4, 1)

    # ---- Spinning outer ring segments
    spinP = ease_out(phase(t, 80, 180))
    if spinP > 0:
        seg = 24
        for s in range(seg):
            a1 = math.degrees(math.pi * 2 / seg * s + t * 0.008)
            a2 = a1 + 360 / seg * 0.6
            col = [GOLD, RED, BLUE][s % 3]
            draw_arc(draw, cx, cy, 440, a1 % 360, a2 % 360, col, spinP * 0.6, 2)
        # counter-spin inner
        for s in range(16):
            a1 = math.degrees(math.pi * 2 / 16 * s - t * 0.012)
            a2 = a1 + 360 / 16 * 0.4
            draw_arc(draw, cx, cy, 400, a1 % 360, a2 % 360, PURPLE, spinP * 0.5, 1)

    # ---- Particles
    alive = []
    for p in particles:
        if p.update():
            p.draw(draw)
            alive.append(p)
    particles.clear()
    particles.extend(alive)

    # ---- Corner brackets
    draw_corners(draw, ease_out(phase(t, 40, 100)))

    # ---- Main title  "KLAW OF 44"
    title_p = ease_out(phase(t, 50, 120))
    if title_p > 0.02:
        # glow layer
        draw_glow_text(draw, img, "KLAW OF 44", (cx, cy - 80),
                       FONT_LG, RED, glow_radius=40, glow_alpha=title_p)
        # gold outline
        draw_outline_text(draw, "KLAW OF 44", (cx, cy - 80),
                          FONT_LG, GOLD, stroke_width=4, alpha=title_p * 0.9)

    # ---- Divider
    draw_divider(img, cy + 30, ease_out(phase(t, 80, 150)))

    # ---- Sub-title "RED PILLAR"
    sub_p = ease_out(phase(t, 100, 160))
    if sub_p > 0.02:
        draw_glow_text(draw, img, "RED PILLAR", (cx, cy + 120),
                       FONT_MD, BLUE, glow_radius=25, glow_alpha=sub_p)
        draw_outline_text(draw, "RED PILLAR", (cx, cy + 120),
                          FONT_MD, GOLD, stroke_width=3, alpha=sub_p * 0.7)

    # ---- Tagline
    tag_p = ease_out(phase(t, 130, 190))
    if tag_p > 0.02:
        draw.text((cx, cy + 210),
                  "[ F U T U R E   I S   N O W ]",
                  font=FONT_SM,
                  fill=(*GOLD, int(tag_p * 220)),
                  anchor="mm")

    # ---- Scanlines
    draw_scanlines(draw)

    return img.convert("RGB")

# ─── Main entry ──────────────────────────────────────────────────
def main():
    try:
        import imageio
    except ImportError:
        print("imageio not found. Install with:  pip install imageio imageio-ffmpeg")
        sys.exit(1)

    particles = []

    print(f"Rendering {TOTAL} frames at {FPS} fps → {OUTPUT}")
    frames = []
    for t in range(TOTAL):
        # schedule bursts
        if t == 1:
            make_burst(W // 2, H // 2, 120, [RED, BLUE, PURPLE, GOLD], particles)
        if t == 30:
            make_burst(W // 2, H // 2, 80, [GOLD, WHITE], particles)
        if t > 60 and t % 90 == 0:
            sx = 200 if random.random() > 0.5 else W - 200
            make_burst(sx, H // 2, 40, [RED, GOLD, PURPLE], particles)

        frame = render_frame(t, particles)
        frames.append(np.array(frame))

        if t % 60 == 0:
            print(f"  frame {t}/{TOTAL}  ({100*t//TOTAL}%)")

    print("Encoding video…")
    writer = imageio.get_writer(OUTPUT, fps=FPS, codec="libx264",
                                 quality=8, macro_block_size=1)
    for f in frames:
        writer.append_data(f)
    writer.close()
    print(f"Done!  →  {OUTPUT}")

if __name__ == "__main__":
    main()
