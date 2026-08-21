#!/usr/bin/env python3
"""把 assets/previews/ 的真实截图合成 1200x630 的分享卡片（assets/og/*.png）。

为什么要这个脚本：
- 原来 index.html 的 og:image 直接指向 800x500 的 .webp。微信对 WebP 的
  分享预览支持不稳定，而且 800x500 是 1.6:1，不是分享卡要求的 1.91:1，会被裁。
- 三个化学页此前完全没有 og:image。

用的是真实页面截图，不是示意图。改完截图重跑本脚本即可。

    python3 tools/build-og.py

依赖：Pillow（读 webp）、rsvg-convert（渲染 SVG，brew install librsvg）
"""

import base64
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREVIEWS = ROOT / "assets" / "previews"
OUT = ROOT / "assets" / "og"

FONT = "PingFang SC,Hiragino Sans GB,Helvetica,sans-serif"

# 卡片配置：输出名 -> (截图, 主标题, 副标题, 背景色, 强调色, 文字色, 页脚)
CARDS = {
    # 首页卡的大标题已经是「学习实验室」，页脚改成网址，避免同一行字出现两次
    "home": ("periodic-table.webp", "学习实验室", "把课本变成可以玩的实验台",
             "#FDF6E3", "#E8792F", "#2B2118", "sanhuang520-ship-it.github.io/learn-lab"),
    "periodic-table": ("periodic-table.webp", "元素周期表", "118 个元素 · 70 张实拍 · 焰色反应",
                       "#FDF6E3", "#E8792F", "#2B2118", "学习实验室 · Learn Lab"),
    "atomic-clock": ("atomic-clock.webp", "核时", "恒星如何制造元素 · H → Fe",
                     "#0E1220", "#6EA8FF", "#F2F5FF", "学习实验室 · Learn Lab"),
    "pomodoro": ("pomodoro.webp", "元素番茄", "一颗星的一生 = 一个番茄",
                 "#141018", "#FF6B5A", "#FFF2EE", "学习实验室 · Learn Lab"),
}


def data_uri(webp: Path) -> str:
    with Image.open(webp) as im:
        buf = io.BytesIO()
        im.convert("RGB").save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def svg_for(shot: str, title: str, subtitle: str, bg: str, accent: str, fg: str, footer: str) -> str:
    uri = data_uri(PREVIEWS / shot)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
 width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <clipPath id="shot"><rect x="600" y="96" width="560" height="438" rx="18"/></clipPath>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.24"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="{bg}"/>
  <circle cx="1040" cy="120" r="380" fill="url(#glow)"/>
  <rect x="72" y="150" width="70" height="7" rx="3.5" fill="{accent}"/>
  <text x="72" y="252" font-family="{FONT}" font-size="76" font-weight="700" fill="{fg}">{title}</text>
  <text x="72" y="320" font-family="{FONT}" font-size="30" fill="{fg}" opacity="0.72">{subtitle}</text>
  <text x="72" y="536" font-family="{FONT}" font-size="24" fill="{accent}">{footer}</text>
  <g clip-path="url(#shot)">
    <image xlink:href="{uri}" x="600" y="96" width="560" height="438"
           preserveAspectRatio="xMinYMin slice"/>
  </g>
  <rect x="600" y="96" width="560" height="438" rx="18" fill="none"
        stroke="{fg}" stroke-opacity="0.14" stroke-width="2"/>
</svg>"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, cfg in CARDS.items():
        shot = PREVIEWS / cfg[0]
        if not shot.exists():
            print(f"  跳过 {name}：找不到 {shot.relative_to(ROOT)}")
            continue
        svg = svg_for(*cfg)
        dest = OUT / f"{name}.png"
        proc = subprocess.run(
            ["rsvg-convert", "-w", "1200", "-h", "630", "-o", str(dest)],
            input=svg.encode("utf-8"), capture_output=True,
        )
        if proc.returncode != 0:
            print(f"  {name} 失败: {proc.stderr.decode()[:200]}")
            return 1
        print(f"  {dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
