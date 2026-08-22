#!/usr/bin/env python3
"""力的合成与分解（初中/高一物理）。

物理依据（人教版必修一 第三章 相互作用）：
  平行四边形定则  两个力为邻边作平行四边形，对角线即合力
  合力范围        |F₁-F₂| ≤ F ≤ F₁+F₂
  同向            F = F₁+F₂（夹角 0°，取到上限）
  反向            F = |F₁-F₂|（夹角 180°，取到下限）
  垂直            F = √(F₁²+F₂²)（夹角 90°）
"""
import math

def compose(f1, a1_deg, f2, a2_deg):
    """两个力按各自方向角合成。角度以 x 轴正方向为 0°，逆时针为正。"""
    a1, a2 = math.radians(a1_deg), math.radians(a2_deg)
    x = f1 * math.cos(a1) + f2 * math.cos(a2)
    y = f1 * math.sin(a1) + f2 * math.sin(a2)
    mag = math.hypot(x, y)
    ang = math.degrees(math.atan2(y, x)) % 360
    return {'x': x, 'y': y, 'mag': mag, 'ang': ang}

def compose_by_angle(f1, f2, theta_deg):
    """已知两力大小与**夹角**，求合力大小（余弦定理形式）。"""
    t = math.radians(theta_deg)
    return math.sqrt(f1*f1 + f2*f2 + 2*f1*f2*math.cos(t))

def resultant_range(f1, f2):
    return abs(f1 - f2), f1 + f2

def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


CASES = [
    # (描述, F1, F2, 夹角, 期望合力)
    ('3N 与 4N 垂直',        3, 4,  90, 5.0),
    ('3N 与 4N 同向',        3, 4,   0, 7.0),
    ('3N 与 4N 反向',        3, 4, 180, 1.0),
    ('5N 与 5N 夹角 60°',    5, 5,  60, 5*math.sqrt(3)),
    ('5N 与 5N 夹角 120°',   5, 5, 120, 5.0),
    ('6N 与 8N 垂直',        6, 8,  90, 10.0),
    ('两个 10N 夹角 90°',   10, 10, 90, 10*math.sqrt(2)),
]

def main():
    bad = 0
    print(f"{'例题':<24}{'合力':>12}{'期望':>12}")
    print('-'*52)
    for desc, f1, f2, th, want in CASES:
        got = compose_by_angle(f1, f2, th)
        ok = close(got, want, 1e-9)
        if not ok:
            bad += 1
            print(f'  ❌ {desc}: 算得 {got} 期望 {want}')
        # 两种算法必须一致：按夹角算 vs 按方向角合成
        v = compose(f1, 0, f2, th)
        if not close(v['mag'], got, 1e-9):
            bad += 1
            print(f"  ❌ {desc}: 两种算法不一致 {v['mag']} vs {got}")
        print(f"{desc:<24}{got:>12.4f}{want:>12.4f}   {'✅' if ok else '❌'}")

    print('\n─── 合力范围 |F₁-F₂| ≤ F ≤ F₁+F₂ ───')
    for f1, f2 in [(3,4),(5,5),(6,8),(10,1),(7,7)]:
        lo, hi = resultant_range(f1, f2)
        # 遍历 0~180 度，合力必须落在范围内，且端点取到
        vals = [compose_by_angle(f1, f2, t) for t in range(0, 181)]
        out_of_range = [v for v in vals if v < lo - 1e-9 or v > hi + 1e-9]
        if out_of_range:
            bad += 1; print(f'  ❌ {f1}N 与 {f2}N: 有 {len(out_of_range)} 个角度超出范围')
        if not close(vals[0], hi) or not close(vals[180], lo):
            bad += 1; print(f'  ❌ {f1}N 与 {f2}N: 0°/180° 没取到上下限')
        print(f'  {f1}N 与 {f2}N → 范围 [{lo}, {hi}]，'
              f'0°={vals[0]:.2f} 180°={vals[180]:.2f}  ✅')

    print('\n─── 合力随夹角单调递减（0°→180°）───')
    for f1, f2 in [(3,4),(5,5),(6,8)]:
        vals = [compose_by_angle(f1, f2, t) for t in range(0, 181)]
        mono = all(vals[i] >= vals[i+1] - 1e-9 for i in range(180))
        if not mono:
            bad += 1; print(f'  ❌ {f1}N 与 {f2}N 不是单调递减')
        else:
            print(f'  {f1}N 与 {f2}N ✅')

    print(f'\n  共 {len(CASES)} 道例题，问题 {bad} 处')
    return 1 if bad else 0

if __name__ == '__main__':
    raise SystemExit(main())
