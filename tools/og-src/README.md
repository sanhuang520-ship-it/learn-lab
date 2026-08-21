# OG 卡片源文件

这里的 `.svg` 是**按页面排版画的标题卡**，不是截图 —— 那些页面没有可截的画面
（一篇长读、一套闪卡），所以做成设计卡而不是伪造一张"截图"。

改完重新导出：

```bash
rsvg-convert -w 1200 -h 630 tools/og-src/<name>.svg -o assets/og/<name>.png
# 首页预览图（800x500，两侧用页面底色补齐）
rsvg-convert -w 800 -h 420 tools/og-src/<name>.svg -o /tmp/p.png
python3 -c "
from PIL import Image
im=Image.open('/tmp/p.png').convert('RGB')
c=Image.new('RGB',(800,500),(7,9,15)); c.paste(im,(0,(500-im.height)//2))
c.save('assets/previews/<name>.webp','WEBP',quality=88,method=6)"
```

依赖 `rsvg-convert`（`brew install librsvg`）与 Pillow。

**有真实画面的页面**（元素周期表、核时、元素番茄、消化卫士）走的是另一条路：
`tools/build-og.py`，把 `assets/previews/` 里的真实截图合成进卡片模板。
