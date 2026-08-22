#!/usr/bin/env python3
"""独立重算每道题的答案，不复用生成器的中间结果 —— 生成器算错了这里要能抓出来。"""
import json, re, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from data import SUBS, NA, VM_STP, molar_mass

BY_NAME = {name: (f, comp, gas, mol) for name, f, comp, gas, mol in SUBS}
IONIC = {name for name, f, c, g, m in SUBS if not m}
GASES = {name for name, f, c, g, m in SUBS if g}

def num(s):
    m = re.search(r'(\d+(?:\.\d+)?)', s)
    return float(m.group(1)) if m else None

def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1, abs(b))

def check(p):
    """返回问题列表。"""
    errs = []
    ask, ans, unit = p['ask'], p.get('ans'), p.get('unit', '')

    # 陷阱关是判断题，只查有解析
    if p['level'] == 5:
        if not p.get('sol'): errs.append('缺解析')
        if 'ok' not in p: errs.append('缺判定')
        return errs

    # ⚠️ 必须按名称长度倒序匹配：「硫酸」是「硫酸铜」的子串，
    #    按任意顺序取第一个匹配会把 CuSO4 的题当成 H2SO4 来算。
    name = next((n for n in sorted(BY_NAME, key=len, reverse=True) if n in ask), None)
    if not name:
        return ['题面里找不到已知物质']
    f, comp, gas, mol = BY_NAME[name]
    M = molar_mass(comp)

    # ① 问分子数的题不能用离子化合物
    if '分子' in ask and name in IONIC:
        errs.append(f'{name} 是离子化合物，不能问分子数')
    # ② 用 22.4 的题，物质必须是标况气体，且题面必须写明标准状况
    if '22.4' in p.get('given', '') + p.get('sol', ''):
        if name not in GASES:
            errs.append(f'{name} 标况下不是气体，不能用 22.4 L/mol')
        if '标准状况' not in ask:
            errs.append('用了 22.4 L/mol 但题面没写"标准状况"')

    # ③ 独立重算
    v = num(ask)
    if v is None:
        return errs + ['题面没有数值']
    recomputed = None
    if unit == 'mol':
        if 'g ' in ask and '×10' not in ask:      recomputed = v / M
        elif '×10²³' in ask:                       recomputed = v / 6.02
        elif ' L ' in ask:                          recomputed = v / VM_STP
    elif unit == 'g':
        if 'mol' in ask:                            recomputed = v * M
        elif ' L ' in ask:                          recomputed = v / VM_STP * M
    elif unit == 'L':
        if 'mol' in ask:                            recomputed = v * VM_STP
        elif 'g ' in ask:                           recomputed = v / M * VM_STP
    elif '×10²³' in unit:
        if 'mol' in ask:                            recomputed = v * 6.02
        elif 'g ' in ask:                           recomputed = v / M * 6.02
    if recomputed is None:
        errs.append(f'校验器认不出题型：{ask}')
    elif not close(float(ans), recomputed, 1e-3):
        errs.append(f'答案 {ans} ≠ 独立重算 {round(recomputed,4)}')
    return errs

if __name__ == '__main__':
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    total = bad = 0
    for lv, ps in sorted(data.items(), key=lambda x: int(x[0])):
        lvbad = 0
        for p in ps:
            total += 1
            e = check(p)
            if e:
                bad += 1; lvbad += 1
                if lvbad <= 3:
                    print(f"  ❌ L{lv} {p['ask'][:52]}\n       {'; '.join(e)}")
        print(f"  第 {lv} 关：{len(ps)} 题，问题 {lvbad} 条")
    print(f"\n  合计 {total} 题，问题 {bad} 条")
    sys.exit(1 if bad else 0)
