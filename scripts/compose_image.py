"""パネルごとに個別画像を生成する (1080x1080px)"""
import sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent))
from fetch_irasutoya import fetch as _fetch

CANVAS_W, CANVAS_H = 1080, 1080
TITLE_H  = 110
TEXT_H   = 210
PAD      = 12

BG_COLOR       = "#FFF8F0"
PANEL_BG       = "#FFFFFF"
TEXT_BOX_BG    = "#F0F7FF"
TEXT_COLOR     = "#333333"
PLACEHOLDER_BG = "#F0F0F0"
PLACEHOLDER_FG = "#AAAAAA"
CATEGORY_COLOR = {"賃貸": "#2D6A4F", "売買": "#C1440E"}

ROOT       = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "output"


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothM.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(text: str, font, max_w: int, draw: ImageDraw.ImageDraw) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        test = cur + ch
        if draw.textbbox((0, 0), test, font=font)[2] > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def _load_image(keyword: str, max_w: int, max_h: int) -> Image.Image:
    path = _fetch(keyword)
    if path:
        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            return img
        except Exception:
            pass
    ph = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    d.rounded_rectangle([0, 0, max_w - 1, max_h - 1], radius=10,
                         fill=PLACEHOLDER_BG, outline="#CCCCCC", width=1)
    d.text((max_w // 2, max_h // 2), keyword[:12], font=_get_font(18),
           fill=PLACEHOLDER_FG, anchor="mm")
    return ph


def _compose_panel(story: dict, episode_num: int, panel: dict,
                   panel_idx: int, total: int, output_path: str) -> None:
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG_COLOR)
    draw   = ImageDraw.Draw(canvas)

    # ── タイトルバー ──────────────────────────────────────
    cat   = story.get("category", "賃貸")
    color = CATEGORY_COLOR.get(cat, "#2D6A4F")
    draw.rectangle([0, 0, CANVAS_W, TITLE_H], fill=color)

    badge_font = _get_font(20)
    draw.rounded_rectangle([12, 16, 78, 44], radius=8, fill="white")
    draw.text((45, 30), cat, font=badge_font, fill=color, anchor="mm")

    draw.text((CANVAS_W // 2, 38),
              "不動産あるある", font=_get_font(34), fill="white", anchor="mm")
    draw.text((CANVAS_W // 2, 78),
              f"#{episode_num:02d}「{story['title']}」{panel_idx}/{total}",
              font=_get_font(22), fill="#D8EED8", anchor="mm")

    # ── イラストエリア ────────────────────────────────────
    illust_y = TITLE_H + PAD
    illust_h = CANVAS_H - TITLE_H - PAD * 3 - TEXT_H
    illust_w = CANVAS_W - PAD * 2

    img = _load_image(panel.get("image", ""), illust_w, illust_h)
    paste_x = PAD + (illust_w - img.width) // 2
    paste_y = illust_y + (illust_h - img.height) // 2
    if img.mode == "RGBA":
        canvas.paste(img, (paste_x, paste_y), img)
    else:
        canvas.paste(img, (paste_x, paste_y))

    # ── テキストボックス ──────────────────────────────────
    tx = PAD
    ty = CANVAS_H - PAD - TEXT_H
    tw = CANVAS_W - PAD * 2
    draw.rounded_rectangle([tx, ty, tx + tw, ty + TEXT_H], radius=14, fill=TEXT_BOX_BG)

    font  = _get_font(42)
    lines = _wrap(panel.get("text", ""), font, tw - 40, draw)
    lh    = 54
    total_h = len(lines) * lh
    start_y = ty + max(14, (TEXT_H - total_h) // 2)
    for i, line in enumerate(lines):
        draw.text((CANVAS_W // 2, start_y + i * lh), line,
                  font=font, fill=TEXT_COLOR, anchor="mm")

    canvas.save(output_path, "PNG")


def compose(story: dict, episode_num: int, output_dir: str | None = None) -> list[str]:
    """4枚の個別パネル画像を生成してパスのリストを返す"""
    out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    out_dir.mkdir(exist_ok=True)

    panels = story["panels"][:4]
    paths  = []
    for i, panel in enumerate(panels, 1):
        path = str(out_dir / f"episode_{episode_num:03d}_panel{i}.png")
        print(f"  🎨 パネル {i}/{len(panels)}: {panel.get('image', '')[:20]}")
        _compose_panel(story, episode_num, panel, i, len(panels), path)
        paths.append(path)

    return paths


if __name__ == "__main__":
    import json, sys as _sys
    stories = json.loads((ROOT / "content" / "stories.json").read_text(encoding="utf-8"))
    idx = int(_sys.argv[1]) if len(_sys.argv) > 1 else 0
    story = stories[idx % len(stories)]
    paths = compose(story, idx + 1)
    for p in paths:
        print(f"生成完了: {p}")
