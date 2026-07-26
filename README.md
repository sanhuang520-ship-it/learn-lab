# 学习实验室 · Learn Lab

把课本做成可以玩的实验台。全部是纯前端单页，打开即用 —— 不用注册、不用下载、手机也能玩。

🔗 **在线访问**：https://sanhuang520-ship-it.github.io/learn-lab/

## 已上线

| 页面 | 路径 | 说明 |
|---|---|---|
| 元素周期表 | [`chemistry/periodic-table/`](chemistry/periodic-table/) | 118 元素详情 · 实拍照片 · 焰色反应 · 发现时间轴 · 化合物侦探小游戏 |
| 核时 Atomic Clock | [`chemistry/atomic-clock/`](chemistry/atomic-clock/) | 可播放的恒星核合成课：看氢一步步烧成铁；也可当叙事时钟 |
| 元素番茄 | [`chemistry/pomodoro/`](chemistry/pomodoro/) | 一颗星的一生 = 一个番茄钟，专注 25 分钟看星球演化 |
| 配平大挑战 | 外链 | 粉笔手写风化学配平游戏，托管在 Cloudflare Pages |

## 目录结构

```
learn-lab/
├── index.html              # 学习站首页（卡片式导航，LIVE 数量由脚本自动统计）
├── chemistry/
│   ├── periodic-table/index.html
│   ├── atomic-clock/index.html
│   └── pomodoro/index.html
├── ROADMAP.md              # 每日开发计划
└── .nojekyll               # 关闭 Jekyll 处理，保证下划线开头的文件也能访问
```

## 加一个新页面

1. 在对应学科目录下新建 `学科/页面名/index.html`（单文件，自带样式和脚本）。
2. 在页面顶部加返回链接：

   ```html
   <a class="ll-back" href="../../">← 学习实验室</a>
   ```

3. 在根 `index.html` 的对应分区里复制一张卡片，改 `--accent`、图标、标题、描述、标签。
   带 `<span class="badge live">LIVE</span>` 的卡片会被自动计入首页"已上线 N 个"。
4. 提交推送，GitHub Pages 自动发布。

## 约定

- **单文件优先**：一个页面一个 `index.html`，样式脚本内联，方便单独分享和存档。
- **无采集无广告**：不接任何统计、不发外部请求（字体和图片 CDN 除外）。
- **移动端必须能用**：所有页面在 375px 宽下要可正常操作。
- **配色沿用**：深空底 `#07090f`、磷光青 `#5eead4`、琥珀 `#f5b942`、紫 `#a78bfa`，字体 Orbitron + Noto Sans SC + JetBrains Mono。

## 说明

`chemistry/periodic-table/` 是 [periodic-table](https://github.com/sanhuang520-ship-it/periodic-table) 仓库的副本，
额外加了返回学习实验室的导航项。后续以本仓库为准，原仓库计划改为跳转。
