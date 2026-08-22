#!/usr/bin/env python3
"""一对相对性状的分离定律。人教版必修二：豌豆茎的高度，D 高茎（显性）/ d 矮茎（隐性）。"""
from collections import Counter
from fractions import Fraction

GENOS = ['DD', 'Dd', 'dd']

def gametes(g):
    """产生配子。Dd 产生 D 和 d 各占 1/2 —— 这是分离定律的核心。"""
    a, b = g[0], g[1]
    return [a, b]                     # DD→[D,D]  Dd→[D,d]  dd→[d,d]

def norm(g):
    """基因型规范化：dD 写成 Dd，显性字母在前。"""
    return ''.join(sorted(g, key=lambda c: (c != 'D', c)))

def punnett(p1, p2):
    """棋盘法：返回子代基因型的分数比例 {基因型: Fraction}。"""
    out = Counter()
    g1, g2 = gametes(p1), gametes(p2)
    for a in g1:
        for b in g2:
            out[norm(a + b)] += 1
    total = len(g1) * len(g2)
    return {k: Fraction(v, total) for k, v in sorted(out.items(),
            key=lambda x: GENOS.index(x[0]))}

def pheno(g):
    """表现型：只要有一个 D 就是高茎。"""
    return '高茎' if 'D' in g else '矮茎'

def pheno_ratio(p1, p2):
    out = Counter()
    for g, f in punnett(p1, p2).items():
        out[pheno(g)] += f
    return dict(out)

def ratio_str(d):
    """把分数字典写成最简整数比，如 3:1"""
    from math import gcd
    vals = list(d.values())
    dens = 1
    for v in vals: dens = dens * v.denominator // gcd(dens, v.denominator)
    ints = [int(v * dens) for v in vals]
    g = 0
    for i in ints: g = gcd(g, i)
    if g: ints = [i // g for i in ints]
    return ' : '.join(f'{k} {v}' for k, v in zip(d.keys(), ints))

# 教材上的标准结论，用来反查上面的算法
EXPECTED = {
 ('DD','DD'): ({'DD':1},                    {'高茎':1}),
 ('DD','Dd'): ({'DD':Fraction(1,2),'Dd':Fraction(1,2)}, {'高茎':1}),
 ('DD','dd'): ({'Dd':1},                    {'高茎':1}),
 ('Dd','Dd'): ({'DD':Fraction(1,4),'Dd':Fraction(1,2),'dd':Fraction(1,4)},
               {'高茎':Fraction(3,4),'矮茎':Fraction(1,4)}),
 ('Dd','dd'): ({'Dd':Fraction(1,2),'dd':Fraction(1,2)},
               {'高茎':Fraction(1,2),'矮茎':Fraction(1,2)}),
 ('dd','dd'): ({'dd':1},                    {'矮茎':1}),
}

if __name__ == '__main__':
    bad = 0
    print(f"{'亲本':<12}{'子代基因型':<28}{'表现型比':<18}")
    print('-'*62)
    for (a, b), (eg, ep) in EXPECTED.items():
        got_g, got_p = punnett(a, b), pheno_ratio(a, b)
        gg = {k: Fraction(v) for k, v in got_g.items()}
        ee = {k: Fraction(v) for k, v in eg.items()}
        pp = {k: Fraction(v) for k, v in got_p.items()}
        epp = {k: Fraction(v) for k, v in ep.items()}
        ok = (gg == ee and pp == epp)
        if not ok:
            bad += 1
            print(f"  ❌ {a}×{b}  算出 {gg} / {pp}  期望 {ee} / {epp}")
        gs = ' '.join(f'{k}:{v}' for k, v in got_g.items())
        print(f"{a+' × '+b:<12}{gs:<28}{ratio_str(got_p):<18}{'✅' if ok else '❌'}")
        # 反向对称性：亲本互换结果应相同
        if punnett(a, b) != punnett(b, a):
            bad += 1; print(f"  ❌ {a}×{b} 与 {b}×{a} 结果不一致")
    print(f"\n  6 种组合，问题 {bad} 处")
    raise SystemExit(1 if bad else 0)
