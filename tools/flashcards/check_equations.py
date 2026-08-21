#!/usr/bin/env python3
"""化学方程式配平校验：原子守恒 + 电荷守恒。写死在这里，用来把每张卡都跑一遍。"""
import re, sys, json
from collections import Counter

def parse_formula(f):
    """展开一个化学式（支持括号、结晶水点号），返回 Counter{元素: 个数} 与电荷。"""
    charge = 0
    m = re.search(r'\^?\(?([0-9]*)([+-])\)?$', f)
    if m and m.group(2):
        n = int(m.group(1)) if m.group(1) else 1
        charge = n if m.group(2) == '+' else -n
        f = f[:m.start()]
    atoms = Counter()
    # 结晶水 / 复合点号
    for part in f.split('·'):
        mult = 1
        pm = re.match(r'^(\d+)', part)
        if pm and not re.match(r'^\d+[+-]$', part):
            mult = int(pm.group(1)); part = part[pm.end():]
        atoms += Counter({k: v*mult for k, v in _expand(part).items()})
    return atoms, charge

def _expand(s):
    stack = [Counter()]
    i = 0
    while i < len(s):
        c = s[i]
        if c == '(':
            stack.append(Counter()); i += 1
        elif c == ')':
            grp = stack.pop(); i += 1
            n = ''
            while i < len(s) and s[i].isdigit(): n += s[i]; i += 1
            n = int(n) if n else 1
            stack[-1] += Counter({k: v*n for k, v in grp.items()})
        elif c.isupper():
            el = c; i += 1
            while i < len(s) and s[i].islower(): el += s[i]; i += 1
            n = ''
            while i < len(s) and s[i].isdigit(): n += s[i]; i += 1
            stack[-1][el] += int(n) if n else 1
        else:
            i += 1
    return stack[0]

def side(expr):
    total, charge = Counter(), 0
    # 只在两侧有空格的 + 处拆项 —— Ba(2+) 这类电荷写法里的 + 不能当分隔符
    for term in re.split(r'\s\+\s', expr.strip()):
        term = term.strip()
        if not term: continue
        coef = 1
        cm = re.match(r'^(\d+)\s*(?=[A-Z(])', term)
        if cm:
            coef = int(cm.group(1)); term = term[cm.end():].strip()
        term = re.sub(r'\s*(↑|↓|\(s\)|\(l\)|\(g\)|\(aq\))\s*', '', term)
        a, c = parse_formula(term)
        total += Counter({k: v*coef for k, v in a.items()})
        charge += c * coef
    return total, charge

def check(eq):
    for sep in ('===', '==', '=', '→'):
        if sep in eq:
            L, R = eq.split(sep, 1); break
    else:
        return False, '找不到等号'
    la, lc = side(L); ra, rc = side(R)
    errs = []
    if la != ra:
        for el in set(la) | set(ra):
            if la[el] != ra[el]:
                errs.append(f'{el}: 左{la[el]} 右{ra[el]}')
    if lc != rc:
        errs.append(f'电荷: 左{lc:+d} 右{rc:+d}')
    return (not errs), ('; '.join(errs) if errs else '守恒')

if __name__ == '__main__':
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    bad = 0
    for c in data:
        ok, msg = check(c['eq'])
        if not ok:
            bad += 1
            print(f"  ❌ [{c['id']}] {c['eq']}\n       {msg}")
    print(f"\n  共 {len(data)} 条，不守恒 {bad} 条")
    sys.exit(1 if bad else 0)
