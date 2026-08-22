#!/usr/bin/env python3
"""溶解度数据与换算校验。

溶解度的定义（人教版九年级下册 第九单元 溶液）：
  在**一定温度**下，某固体物质在 **100 g 溶剂**里达到**饱和状态**时所溶解的**质量**（g）。
四个要素缺一不可，这也是判断题最爱考的地方。

由溶解度 S 求饱和溶液的溶质质量分数：
  w = S / (100 + S) × 100%      ← 分母是「溶液」质量，不是溶剂
"""
import json, sys

def mass_fraction(S):
    """饱和溶液的溶质质量分数（%）。"""
    return S / (100 + S) * 100

def main(path):
    d = json.load(open(path, encoding='utf-8'))
    subs = d['substances']
    bad = 0
    temps = [0,10,20,30,40,50,60,70,80,90,100]

    for s in subs:
        p = f"[{s['id']}]"
        for k in ('name','formula','color','trend','points','note'):
            if not s.get(k):
                print(f'  ❌ {p} 缺字段 {k}'); bad += 1
        pts = s['points']
        # 温度点必须齐全
        missing = [t for t in temps if str(t) not in pts]
        if missing:
            print(f'  ❌ {p} 缺温度点 {missing}'); bad += 1
            continue
        vals = [pts[str(t)] for t in temps]
        if any(v <= 0 for v in vals):
            print(f'  ❌ {p} 有非正的溶解度'); bad += 1
        # 单调性必须与 trend 一致
        inc = all(vals[i] <= vals[i+1] for i in range(len(vals)-1))
        dec = all(vals[i] >= vals[i+1] for i in range(len(vals)-1))
        if s['trend'] == '下降':
            if not dec:
                print(f"  ❌ {p} 标为下降但数据不是单调递减"); bad += 1
        else:
            if not inc:
                print(f"  ❌ {p} 标为{s['trend']}但数据不是单调递增"); bad += 1

    # 关键考点：20 ℃ 时 NaCl 约 36 g，属于「易溶」（>10 g）
    nacl = next(s for s in subs if s['id'] == 'nacl')
    if not (35 <= nacl['points']['20'] <= 37):
        print('  ❌ 20 ℃ 氯化钠溶解度应在 36 g 左右'); bad += 1

    # 关键考点：氢氧化钙微溶（20 ℃ 在 0.01~1 g 之间）
    ca = next(s for s in subs if s['id'] == 'caoh2')
    if not (0.01 <= ca['points']['20'] <= 1):
        print('  ❌ 20 ℃ 氢氧化钙应属微溶（0.01~1 g）'); bad += 1

    # 质量分数换算的边界性质
    print('\n─── 饱和溶液溶质质量分数 w = S/(100+S) ───')
    for S, want_lt in ((36.0, 100), (110.0, 100), (0.165, 1)):
        w = mass_fraction(S)
        if not (0 < w < want_lt):
            bad += 1; print(f'  ❌ S={S} 算出 w={w}，超出合理范围')
        print(f'  S = {S:>7} g  →  w = {w:.2f}%')
    # w 必须恒小于 100%，且随 S 单调递增
    ws = [mass_fraction(S) for S in range(1, 500)]
    if any(w >= 100 for w in ws):
        bad += 1; print('  ❌ 存在 w ≥ 100% 的情况')
    if any(ws[i] >= ws[i+1] for i in range(len(ws)-1)):
        bad += 1; print('  ❌ w 不随 S 单调递增')
    print('  w 恒 < 100% 且随 S 单调递增 ✅')

    print('\n─── 结晶方法判定（依据溶解度随温度变化的陡缓）───')
    for s in subs:
        v0, v100 = s['points']['0'], s['points']['100']
        ratio = v100 / v0
        method = '蒸发结晶' if ratio < 1.5 else '降温结晶'
        if s['id'] == 'caoh2':
            method = '（溶解度随温度下降，不适用一般结晶讨论）'
        print(f"  {s['name']:<8} 0℃ {v0:>6} → 100℃ {v100:>6}  倍数 {ratio:>5.2f}  → {method}")

    print(f"\n  共 {len(subs)} 种物质，问题 {bad} 处")
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
