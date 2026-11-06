#!/usr/bin/env python3
# Shield app icon: a Rwandan-style leaf-shaped shield with imigongo zigzags, over two crossed spears, on a dark badge.
# Drawn from geometry here (original artwork, GNU AGPL-3.0 like the rest of Shield). Needs Pillow.
#
#   python tools/rebrand/make_shield_icon.py
#
# Writes into resources/:
#   shield_badge.png (1024, macOS ICON_BIG / MSIX source), shield_icon_256.png (ICON_SMALL, Linux, in-app logo),
#   Shield.ico (Windows app), Shield_doc.ico (Windows .lynx document), Shield.icns (macOS),
#   icons/hicolor/<n>x<n>/apps/shield.png (Linux 16 ... 512), and src/ui/LogoData.h (embedded 256 px logo).
import io
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "resources"

SS = 4  # supersampling
N = 1024 * SS

# palette
PLATE_TOP, PLATE_BOTTOM = (36, 40, 56), (16, 19, 28)
TAN, TAN_DARK = (226, 190, 132), (196, 152, 92)
RIM = (74, 40, 22)
BLACK = (28, 22, 20)
TERRACOTTA = (176, 66, 38)
CREAM = (244, 230, 200)
WOOD, WOOD_DARK = (128, 78, 42), (86, 50, 26)
STEEL, STEEL_DARK, STEEL_LIGHT = (200, 208, 216), (120, 130, 142), (240, 244, 248)
BRASS = (204, 160, 72)


def s(v):
    return v * N


def rounded_plate():
    grad = Image.new("RGB", (1, 256))
    for y in range(256):
        t = y / 255
        grad.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(PLATE_TOP, PLATE_BOTTOM)))
    grad = grad.resize((N, N))
    mask = Image.new("L", (N, N), 0)
    m = s(0.055)  # macOS-style margin
    ImageDraw.Draw(mask).rounded_rectangle([m, m, N - m, N - m], radius=s(0.2), fill=255)
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    return img


def leaf(cx, top, height, width, power=0.72, steps=400):
    """Closed outline of a vesica (leaf) shape: pointed top and bottom, widest in the middle."""
    right, left = [], []
    for i in range(steps + 1):
        t = i / steps
        y = top + t * height
        half = width / 2 * math.sin(math.pi * t) ** power
        right.append((cx + half, y))
        left.append((cx - half, y))
    return right + left[::-1]


def spear(d, base, tip, shaft_w):
    (x0, y0), (x1, y1) = base, tip
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    def at(t, off=0.0):
        return (x0 + ux * t + px * off, y0 + uy * t + py * off)

    blade = 0.27 * length
    neck = length - blade
    # shaft
    d.polygon([at(0, -shaft_w / 2), at(neck, -shaft_w / 2), at(neck, shaft_w / 2), at(0, shaft_w / 2)], fill=WOOD)
    d.polygon([at(0, shaft_w * 0.12), at(neck, shaft_w * 0.12), at(neck, shaft_w / 2), at(0, shaft_w / 2)], fill=WOOD_DARK)
    # butt spike and binding
    d.polygon([at(-0.05 * length, 0), at(0, -shaft_w * 0.62), at(0.02 * length, -shaft_w * 0.62),
               at(0.02 * length, shaft_w * 0.62), at(0, shaft_w * 0.62)], fill=STEEL_DARK)
    for k in range(3):
        t = neck - 0.012 * length * (k + 1) * 1.6
        d.polygon([at(t - 0.006 * length, -shaft_w * 0.66), at(t + 0.006 * length, -shaft_w * 0.66),
                   at(t + 0.006 * length, shaft_w * 0.66), at(t - 0.006 * length, shaft_w * 0.66)], fill=BRASS)
    # leaf blade: widest a third of the way up, with a raised midrib
    bw = shaft_w * 2.3
    pts_r, pts_l = [], []
    for i in range(61):
        t = i / 60
        half = bw * (math.sin(math.pi * min(1, t * 1.25)) ** 0.8 if t < 0.4 else (1 - t) / 0.6)
        half = max(half, shaft_w * 0.35 if t < 0.05 else 0)
        pts_r.append(at(neck + t * blade, half))
        pts_l.append(at(neck + t * blade, -half))
    d.polygon(pts_r + pts_l[::-1], fill=STEEL)
    d.polygon(pts_l[::-1] + [at(neck + t * blade, 0) for t in (0.0, 1.0)][::-1], fill=STEEL_LIGHT)
    d.line([at(neck, 0), at(length, 0)], fill=STEEL_DARK, width=max(1, int(shaft_w * 0.16)))


def zigzag_band(d, y, amp, period, thick, x0, x1, fill):
    """A horizontal zigzag stripe (imigongo style) between x0 and x1."""
    top, bottom = [], []
    x = x0 - period
    i = 0
    while x <= x1 + period:
        yy = y - amp if i % 2 == 0 else y + amp
        top.append((x, yy - thick / 2))
        bottom.append((x, yy + thick / 2))
        x += period / 2
        i += 1
    d.polygon(top + bottom[::-1], fill=fill)


def shield_layer():
    cx, top, h, w = s(0.5), s(0.135), s(0.73), s(0.47)
    outer = leaf(cx, top, h, w)
    rim = s(0.022)
    inner = leaf(cx, top + rim * 1.6, h - rim * 3.2, w - rim * 2)

    layer = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon(outer, fill=RIM)

    face = Image.new("RGBA", (N, N), TAN + (255,))
    fd = ImageDraw.Draw(face)
    # left half slightly darker: a curved hide catching the light from the right
    fd.rectangle([0, 0, cx, N], fill=TAN_DARK)
    x0, x1 = cx - w / 2, cx + w / 2
    period, amp, thick = s(0.075), s(0.022), s(0.03)
    # imigongo bands, upper and lower, mirrored around the waist
    for k, (dy, col) in enumerate([(-0.205, BLACK), (-0.150, TERRACOTTA), (-0.095, BLACK)]):
        zigzag_band(fd, s(0.5 + dy), amp, period, thick, x0, x1, col)
        zigzag_band(fd, s(0.5 - dy), amp, period, thick, x0, x1, col)
    # waist: concentric diamonds on a cream field
    fd.rectangle([x0, s(0.5) - s(0.05), x1, s(0.5) + s(0.05)], fill=CREAM)
    for k in range(-3, 4):
        dcx = cx + k * s(0.07)
        for r, col in ((s(0.046), BLACK), (s(0.03), TERRACOTTA), (s(0.014), CREAM)):
            fd.polygon([(dcx, s(0.5) - r), (dcx + r, s(0.5)), (dcx, s(0.5) + r), (dcx - r, s(0.5))], fill=col)
    # central rib (the boss stick behind the hide)
    rib = s(0.016)
    fd.rectangle([cx - rib, 0, cx + rib, N], fill=RIM)
    fd.rectangle([cx - rib * 0.4, 0, cx + rib * 0.15, N], fill=(120, 72, 40))

    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).polygon(inner, fill=255)
    layer.paste(face, (0, 0), mask)
    return layer, outer


def soft_shadow(outline, offset, blur, alpha):
    sh = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + offset[0], y + offset[1]) for x, y in outline], fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def render(plate=True):
    img = rounded_plate() if plate else Image.new("RGBA", (N, N), (0, 0, 0, 0))
    spears = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spears)
    shaft = s(0.026)
    spear(sd, (s(0.205), s(0.875)), (s(0.835), s(0.11)), shaft)
    spear(sd, (s(0.795), s(0.875)), (s(0.165), s(0.11)), shaft)
    img = Image.alpha_composite(img, spears)
    shield, outline = shield_layer()
    img = Image.alpha_composite(img, soft_shadow(outline, (s(0.006), s(0.014)), s(0.012), 140))
    img = Image.alpha_composite(img, shield)
    return img.resize((1024, 1024), Image.LANCZOS)


def document(icon):
    """The .lynx project-file icon: a page with a folded corner and the shield on it."""
    page = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(page)
    l, t, r, b, fold = s(0.17), s(0.06), s(0.83), s(0.94), s(0.17)
    d.polygon([(l, t), (r - fold, t), (r, t + fold), (r, b), (l, b)], fill=(250, 248, 244), outline=(150, 150, 150), width=SS * 6)
    d.polygon([(r - fold, t), (r - fold, t + fold), (r, t + fold)], fill=(214, 210, 204))
    page = page.resize((1024, 1024), Image.LANCZOS)
    mark = icon.resize((620, 620), Image.LANCZOS)
    page.alpha_composite(mark, (202, 300))
    return page


def write_logo_header(png256):
    data = png256.getvalue()
    rows = [", ".join(str(b) for b in data[i:i + 24]) for i in range(0, len(data), 24)]
    text = ("#pragma once\n\n"
            "// Shield logo (shield and crossed spears on a dark badge, 256 px PNG with transparency), from\n"
            "// resources/shield_icon_256.png (tools/rebrand/make_shield_icon.py)\n\n"
            "namespace lynx::logo\n{\ninline constexpr unsigned char png256[] = {\n"
            + ",\n".join(rows) + "\n};\n} // namespace lynx::logo\n")
    (ROOT / "src/ui/LogoData.h").write_text(text, encoding="utf-8", newline="\n")


def write_splash_header():
    """The splash-screen figure (the shield and spears without the badge, cropped, 420 px tall). The array keeps
    upstream's name (pepperPng) so Splash.cpp needs no change beyond the words."""
    art = render(plate=False)
    art = art.crop(art.getbbox())
    art = art.resize((round(art.width * 420 / art.height), 420), Image.LANCZOS)
    buf = io.BytesIO()
    art.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    rows = [", ".join(str(b) for b in data[i:i + 24]) for i in range(0, len(data), 24)]
    text = ("#pragma once\n\n"
            f"// The splash-screen figure: the Shield shield and spears ({art.width}x{art.height} PNG with transparency).\n"
            "// Generated by tools/rebrand/make_shield_icon.py - do not edit by hand.\n\n"
            "namespace lynx::splashdata\n{\ninline constexpr unsigned char pepperPng[] = {\n"
            + ",\n".join(rows) + "\n};\n} // namespace lynx::splashdata\n")
    (ROOT / "src/ui/SplashData.h").write_text(text, encoding="utf-8", newline="\n")


def main():
    write_splash_header()
    icon = render()
    icon.save(RES / "shield_badge.png")
    small = icon.resize((256, 256), Image.LANCZOS)
    small.save(RES / "shield_icon_256.png")
    buf = io.BytesIO()
    small.save(buf, format="PNG")
    write_logo_header(buf)

    ico_sizes = [(n, n) for n in (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)]
    icon.save(RES / "Shield.ico", sizes=ico_sizes)
    document(icon).save(RES / "Shield_doc.ico", sizes=ico_sizes)
    icon.save(RES / "Shield.icns")

    for n in (16, 22, 24, 32, 48, 64, 128, 256, 512):
        out = RES / "icons" / "hicolor" / f"{n}x{n}" / "apps" / "shield.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        icon.resize((n, n), Image.LANCZOS).save(out)
    print("icons written to", RES)


if __name__ == "__main__":
    main()
