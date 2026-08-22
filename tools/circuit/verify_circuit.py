#!/usr/bin/env python3
"""串并联电路求解（初中物理层级）。

范围界定：
- 只做**纯电阻**的串联、并联、以及「一段串一段并」的混联
- 电源视为理想电源（不计内阻），导线电阻不计
- 这些都是初中电学的标准简化。真实电路有内阻，页面上会写明。

物理依据（人教版八/九年级物理 电流和电路 / 欧姆定律）：
  欧姆定律       I = U / R
  串联           R总 = R1+R2+…    I 处处相等    U总 = U1+U2+…
  并联           1/R总 = 1/R1+…   U 各支路相等   I总 = I1+I2+…
"""
from fractions import Fraction as F


def r_series(rs):
    return sum(rs)


def r_parallel(rs):
    if any(r == 0 for r in rs):
        return F(0)                      # 有一条 0 电阻支路 = 短路
    return 1 / sum(1 / F(r) for r in rs)


def solve(circuit, emf):
    """circuit 是一个块列表，块要么是 {'type':'series','r':阻值}
    要么是 {'type':'parallel','rs':[阻值,...]}。整体是这些块的串联。

    返回每块的 R / U / I，以及总量。
    """
    blocks = []
    for b in circuit:
        if b['type'] == 'series':
            blocks.append({'R': F(b['r']), 'raw': b})
        else:
            blocks.append({'R': r_parallel([F(x) for x in b['rs']]), 'raw': b})

    R_total = sum(b['R'] for b in blocks)
    if R_total == 0:
        return {'short': True, 'R': F(0), 'I': None, 'blocks': blocks}

    I = F(emf) / R_total                  # 串联电流处处相等
    for b in blocks:
        b['U'] = I * b['R']
        b['I'] = I
        if b['raw']['type'] == 'parallel':
            # 并联各支路电压相同，电流按阻值反比分配
            b['branch'] = [{'r': F(x), 'I': b['U'] / F(x) if x else None,
                            'U': b['U']} for x in b['raw']['rs']]
    return {'short': False, 'R': R_total, 'I': I, 'U': F(emf), 'blocks': blocks}


# ── 用教材上算得出的标准例题反查求解器 ──
CASES = [
    # (描述, 电路, 电源电压, 期望总电阻, 期望总电流)
    ('两个 10Ω 串联，6V',
     [{'type':'series','r':10}, {'type':'series','r':10}], 6, F(20), F(6,20)),
    ('两个 10Ω 并联，6V',
     [{'type':'parallel','rs':[10,10]}], 6, F(5), F(6,5)),
    ('6Ω 与 3Ω 并联，再串 2Ω，12V',
     [{'type':'parallel','rs':[6,3]}, {'type':'series','r':2}], 12, F(4), F(3)),
    ('三个 6Ω 并联，6V',
     [{'type':'parallel','rs':[6,6,6]}], 6, F(2), F(3)),
    ('5Ω 串 15Ω，10V',
     [{'type':'series','r':5}, {'type':'series','r':15}], 10, F(20), F(1,2)),
]

def main():
    bad = 0
    print(f"{'例题':<30}{'R总':>8}{'I总':>10}   分压/分流")
    print('-' * 74)
    for desc, cir, emf, eR, eI in CASES:
        s = solve(cir, emf)
        okR, okI = s['R'] == eR, s['I'] == eI
        if not (okR and okI):
            bad += 1
            print(f"  ❌ {desc}: R={s['R']}(期望{eR}) I={s['I']}(期望{eI})")
        # 串联分压之和 == 总电压
        u_sum = sum(b['U'] for b in s['blocks'])
        if u_sum != F(emf):
            bad += 1; print(f"  ❌ {desc}: 各段分压之和 {u_sum} ≠ 电源 {emf}")
        # 并联分流之和 == 干路电流
        for b in s['blocks']:
            if 'branch' in b:
                i_sum = sum(x['I'] for x in b['branch'])
                if i_sum != s['I']:
                    bad += 1; print(f"  ❌ {desc}: 并联分流之和 {i_sum} ≠ 干路 {s['I']}")
        detail = ' / '.join(f"{float(b['U']):.2f}V" for b in s['blocks'])
        print(f"{desc:<30}{str(s['R']):>8}{str(s['I']):>10}   {detail}  "
              f"{'✅' if okR and okI else '❌'}")

    # 短路必须被识别
    s = solve([{'type':'parallel','rs':[10, 0]}], 6)
    if not s['short']:
        bad += 1; print('  ❌ 一条支路 0Ω（短路）没有被识别')
    else:
        print(f"{'一条支路 0Ω（短路）':<30}{'—':>8}{'—':>10}   已识别为短路  ✅")

    # 并联总电阻必须小于任一支路（初中反复强调的结论）
    for rs in ([10,10],[6,3],[6,6,6],[100,1]):
        rp = r_parallel([F(x) for x in rs])
        if rp >= min(rs):
            bad += 1; print(f'  ❌ 并联 {rs} 的总电阻 {rp} 不小于最小支路')
    print(f"\n  并联总电阻恒小于任一支路：已验 4 组 ✅")
    print(f"  共 {len(CASES)} 道例题，问题 {bad} 处")
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
