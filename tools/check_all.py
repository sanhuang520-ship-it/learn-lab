#!/usr/bin/env python3
"""一次跑完全站所有内容校验。CI 和本地都用这一个入口。

    python3 tools/check_all.py

分两部分：

**A. 各科目的内容校验** —— 化学方程式配平、电子排布规律、摩尔计算答案、
   安全条目依据、遗传比例。这些各自的脚本在对应子目录里。

**B. 页面与源数据是否同步** —— 这一项比 A 更容易出问题：
   几个页面的题库是**内嵌在 HTML 里**的（为了免请求、离线可用），
   改了 tools/ 下的源数据却忘了重新生成页面，校验会全绿但线上还是旧的。
   所以这里逐条比对页面里内嵌的条目数与源文件是否一致。
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 子目录, 脚本, 参数
CHECKS = [
    ('化学方程式配平',   'flashcards',      'check_equations.py',  ['cards.json']),
    ('核外电子排布',     'electron-shells', 'verify_shells.py',    ['elements.json']),
    ('实验安全条目',     'lab-safety',      'check_items.py',      ['items.json']),
    ('遗传分离比例',     'mendel',          'verify_genetics.py',  []),
    ('细胞器条目',       'organelles',      'verify_cells.py',     ['organelles.json']),
    ('电路求解',         'circuit',         'verify_circuit.py',   []),
]

# 页面, 页面内计数用的正则, 源文件, 源文件里的条目数
SYNC = [
    ('chemistry/flashcards/index.html',      r'"id":\s*"',   'tools/flashcards/cards.json',      None),
    ('chemistry/electron-shells/index.html', r'"sym":\s*"',  'tools/electron-shells/elements.json', None),
    ('chemistry/lab-safety/index.html',      r'"id":\s*"',   'tools/lab-safety/items.json',      None),
]


def run(label, sub, script, args):
    d = ROOT / 'tools' / sub
    p = subprocess.run([sys.executable, script] + args, cwd=d,
                       capture_output=True, text=True)
    ok = p.returncode == 0
    tail = (p.stdout + p.stderr).strip().splitlines()
    print(f"  {'✅' if ok else '❌'} {label:<18} {tail[-1].strip() if tail else ''}")
    if not ok:
        for line in tail[-12:]:
            print(f"       {line}")
    return ok


def run_mole():
    """摩尔那套要先生成再校验。"""
    d = ROOT / 'tools' / 'mole'
    g = subprocess.run([sys.executable, 'gen.py'], cwd=d, capture_output=True, text=True)
    if g.returncode != 0:
        print('  ❌ 摩尔计算题        生成失败')
        print((g.stdout + g.stderr).strip()[-500:])
        return False
    v = subprocess.run([sys.executable, 'verify.py', 'problems.json'], cwd=d,
                       capture_output=True, text=True)
    ok = v.returncode == 0
    tail = (v.stdout + v.stderr).strip().splitlines()
    print(f"  {'✅' if ok else '❌'} {'摩尔计算题':<18} {tail[-1].strip() if tail else ''}")
    if not ok:
        for line in tail[-12:]:
            print(f"       {line}")
    (d / 'problems.json').unlink(missing_ok=True)
    return ok


def check_sync():
    """页面内嵌的条目数必须与源数据一致。"""
    ok = True
    for page, pat, src, _ in SYNC:
        pg, sf = ROOT / page, ROOT / src
        if not pg.exists() or not sf.exists():
            print(f'  ❌ 找不到 {page} 或 {src}'); ok = False; continue
        n_page = len(re.findall(pat, pg.read_text(encoding='utf-8')))
        n_src = len(json.loads(sf.read_text(encoding='utf-8')))
        good = n_page == n_src
        ok &= good
        print(f"  {'✅' if good else '❌'} {Path(page).parent.name:<18} "
              f"页面内嵌 {n_page} 条 / 源数据 {n_src} 条"
              f"{'' if good else '  ← 改了数据没重新生成页面？'}")
    return ok


def check_pages():
    """每个已发布页面的基本元数据。这几项漏了不会报错，只会静静地少掉。"""
    need = [('canonical', r'rel="canonical"'),
            ('og:image',  r'property="og:image"'),
            ('twitter',   r'name="twitter:card"'),
            ('JSON-LD',   r'application/ld\+json'),
            ('doctype',   r'^\s*<!DOCTYPE html>'),
            ('lang',      r'<html[^>]*\slang=')]
    pages = sorted(p for p in ROOT.rglob('index.html')
                   if '.git' not in p.parts and 'node_modules' not in p.parts)
    ok = True
    for p in pages:
        body = p.read_text(encoding='utf-8')
        missing = [n for n, r in need if not re.search(r, body, re.M)]
        h1 = len(re.findall(r'<h1[\s>]', body))
        rel = p.relative_to(ROOT).parent.as_posix() or '(首页)'
        if missing or h1 != 1:
            ok = False
            note = ('缺 ' + '/'.join(missing)) if missing else ''
            note += (f'  h1={h1}（应为 1）' if h1 != 1 else '')
            print(f'  ❌ {rel:<28} {note}')
    if ok:
        print(f'  ✅ {"全部页面":<18} {len(pages)} 页元数据齐全，各 1 个 h1')
    return ok


def main():
    print('\n─── A. 内容校验 ───')
    results = [run(*c) for c in CHECKS]
    results.append(run_mole())

    print('\n─── B. 页面与源数据是否同步 ───')
    results.append(check_sync())

    print('\n─── C. 页面元数据 ───')
    results.append(check_pages())

    bad = results.count(False)
    print(f"\n{'全部通过 ✅' if not bad else f'有 {bad} 项未通过 ❌'}\n")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
