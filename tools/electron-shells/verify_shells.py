#!/usr/bin/env python3
"""核外电子排布校验（必修层级，1-20 号元素）。

规则（人教版必修第一册 / 必修第二册「原子结构」）：
  R1 每层最多 2n² 个电子（K=2, L=8, M=18, N=32）
  R2 最外层最多 8 个（K 层作最外层时最多 2 个）
  R3 次外层最多 18 个
  R4 倒数第三层最多 32 个
  R5 由内向外逐层排布：内层未满不排外层 —— 但要受 R2/R3 反过来限制
"""
CAP = [2, 8, 18, 32]          # 2n²
NAMES = ['K', 'L', 'M', 'N']

def violations(shells):
    """shells 如 [2,8,8,1]，返回违反的规则列表。"""
    v = []
    s = [x for x in shells if x > 0] or [0]
    for i, n in enumerate(s):
        if n > CAP[i]:
            v.append(f'R1 {NAMES[i]}层最多{CAP[i]}个，填了{n}个')
    last = len(s) - 1
    outer_cap = 2 if last == 0 else 8
    if s[last] > outer_cap:
        v.append(f'R2 最外层({NAMES[last]}层)最多{outer_cap}个，填了{s[last]}个')
    if last >= 1 and s[last-1] > 18:
        v.append(f'R3 次外层最多18个，填了{s[last-1]}个')
    if last >= 2 and s[last-2] > 32:
        v.append(f'R4 倒数第三层最多32个')
    # R5：内层没"排满"就不能往外层排。
    # ⚠️ 这里的"排满"有两种情况，漏掉第二种会把钾的正确排布 [2,8,8,1] 误判成违规：
    #   ① 装到了该层上限 2n²
    #   ② 装到 8 个就停 —— 因为它当时是最外层，再装就违反 R2。
    #      钾就是这样：M 层能装 18，但第 19 个电子若留在 M，最外层就成了 9 个，
    #      所以只能另起 N 层。这正是「为什么钾是 2,8,8,1 而不是 2,8,9」。
    for i in range(last):
        if s[i] == CAP[i] or s[i] == 8:
            continue
        v.append(f'R5 {NAMES[i]}层没排满({s[i]}个)就往{NAMES[i+1]}层排了')
    return v

def build(z):
    """按规则推出 Z 号元素的排布（1-20 有效）。"""
    s = []
    left = z
    i = 0
    while left > 0:
        put = min(left, CAP[i])
        s.append(put); left -= put; i += 1
        # 最外层不能超 8：超了就把多的挪到下一层
        while True:
            last = len(s) - 1
            cap_out = 2 if last == 0 else 8
            if s[last] > cap_out and left >= 0:
                over = s[last] - cap_out
                s[last] = cap_out
                s.append(over)
                continue
            break
    return s

if __name__ == '__main__':
    import json, sys
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    bad = 0
    for e in data:
        v = violations(e['shells'])
        expect = build(e['z'])
        if v:
            bad += 1; print(f"  ❌ {e['z']:>2} {e['sym']:<3} {e['shells']} 违反: {'; '.join(v)}")
        if e['shells'] != expect:
            bad += 1; print(f"  ❌ {e['z']:>2} {e['sym']:<3} 数据 {e['shells']} ≠ 规则推导 {expect}")
        if sum(e['shells']) != e['z']:
            bad += 1; print(f"  ❌ {e['z']:>2} {e['sym']:<3} 电子总数 {sum(e['shells'])} ≠ 质子数 {e['z']}")
        # 周期 = 电子层数；主族序数 = 最外层电子数
        if e['period'] != len(e['shells']):
            bad += 1; print(f"  ❌ {e['z']:>2} {e['sym']:<3} 周期 {e['period']} ≠ 电子层数 {len(e['shells'])}")
        if e.get('group') and e['group'] != e['shells'][-1]:
            bad += 1; print(f"  ❌ {e['z']:>2} {e['sym']:<3} 主族 {e['group']} ≠ 最外层 {e['shells'][-1]}")
    print(f"\n  共 {len(data)} 个元素，问题 {bad} 处")
    sys.exit(1 if bad else 0)
