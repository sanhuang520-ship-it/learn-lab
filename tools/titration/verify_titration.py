#!/usr/bin/env python3
"""强酸强碱滴定的 pH 计算与指示剂选择（高中化学层级）。

范围界定：
- 只做**强酸滴强碱 / 强碱滴强酸**（完全电离），弱酸弱碱要用电离平衡常数，不在这一课
- 25 ℃、Kw = 1.0×10⁻¹⁴
- 忽略活度系数与温度变化，这是教材的标准简化

依据（人教版选择性必修一 水溶液中的离子反应与平衡）：
  水的离子积       Kw = c(H⁺)·c(OH⁻) = 1.0×10⁻¹⁴（25 ℃）
  pH               = −lg c(H⁺)
  强酸强碱恰好中和  溶液呈中性，pH = 7
  突跃范围         强酸强碱滴定约 pH 4~10（±0.1% 相对误差处）
"""
import math

KW = 1.0e-14

def ph_from_h(h):
    return -math.log10(h)

def titrate(c_acid, v_acid_mL, c_base, v_base_mL):
    """强碱滴强酸：返回该点的 pH。体积单位 mL，浓度 mol/L。"""
    n_acid = c_acid * v_acid_mL / 1000.0
    n_base = c_base * v_base_mL / 1000.0
    v_tot = (v_acid_mL + v_base_mL) / 1000.0
    if v_tot <= 0:
        return None
    diff = n_acid - n_base
    if abs(diff) < 1e-15:                 # 恰好中和
        return 7.0
    if diff > 0:                          # 酸过量
        return ph_from_h(diff / v_tot)
    oh = -diff / v_tot                    # 碱过量
    return 14.0 - ph_from_h(oh)

# 常用指示剂的变色范围与滴定终点颜色（人教版）
INDICATORS = [
    {'id':'phenolphthalein', 'name':'酚酞',   'lo':8.2, 'hi':10.0,
     'colorLo':'无色', 'colorHi':'浅红',
     'note':'变色范围 8.2~10.0。**强碱滴强酸**常用它：终点由无色变浅红，且半分钟不褪色。'},
    {'id':'methyl_orange',   'name':'甲基橙', 'lo':3.1, 'hi':4.4,
     'colorLo':'红',   'colorHi':'黄',
     'note':'变色范围 3.1~4.4。**强酸滴强碱**常用它：终点由黄变橙。注意橙色是过渡色。'},
    {'id':'litmus',          'name':'石蕊',   'lo':5.0, 'hi':8.0,
     'colorLo':'红',   'colorHi':'蓝',
     'note':'变色范围 5.0~8.0，**变色不明显、范围太宽**，所以滴定一般不用石蕊。'},
]

def jump_range(c=0.1, v=20.0):
    """突跃范围：从相对误差 −0.1% 到 +0.1% 对应的 pH 区间。"""
    v_eq = v                       # 等浓度时体积相等
    lo = titrate(c, v, c, v_eq*0.999)
    hi = titrate(c, v, c, v_eq*1.001)
    return lo, hi

def main():
    bad = 0
    print('─── 关键点 pH（0.1 mol/L NaOH 滴 20.00 mL 0.1 mol/L HCl）───')
    pts = [(0.0,'滴入前'), (10.0,'半中和'), (19.98,'−0.1%'),
           (20.0,'恰好中和'), (20.02,'+0.1%'), (40.0,'碱过量一倍')]
    for vb, label in pts:
        p = titrate(0.1, 20.0, 0.1, vb)
        print(f'  {label:<12} V(碱)={vb:>6} mL   pH = {p:.2f}')

    # ① 滴入前只有 0.1 mol/L HCl，pH 应为 1
    p0 = titrate(0.1, 20.0, 0.1, 0.0)
    if abs(p0 - 1.0) > 1e-6:
        bad += 1; print(f'  ❌ 滴入前 pH 应为 1，算得 {p0}')
    # ② 恰好中和必须是 7
    peq = titrate(0.1, 20.0, 0.1, 20.0)
    if abs(peq - 7.0) > 1e-9:
        bad += 1; print(f'  ❌ 恰好中和 pH 应为 7，算得 {peq}')
    # ③ pH 必须随碱量单调递增
    vals = [titrate(0.1, 20.0, 0.1, v/100) for v in range(0, 4001)]
    if any(vals[i] > vals[i+1] + 1e-9 for i in range(len(vals)-1)):
        bad += 1; print('  ❌ pH 不是随碱量单调递增')
    else:
        print('\n  pH 随碱量单调递增（0~40 mL 每 0.01 mL 检查）✅')

    # ④ 突跃范围应约为 4~10
    lo, hi = jump_range()
    print(f'\n─── 突跃范围（±0.1% 相对误差）───')
    print(f'  −0.1% → pH {lo:.2f}    +0.1% → pH {hi:.2f}')
    if not (3.5 <= lo <= 4.5 and 9.5 <= hi <= 10.5):
        bad += 1; print(f'  ❌ 突跃范围应约为 4~10，算得 {lo:.2f}~{hi:.2f}')
    else:
        print('  与教材「强酸强碱滴定突跃约 pH 4~10」一致 ✅')

    # ⑤ 指示剂能否用于该滴定
    #
    # ⚠️ 判据不是「变色范围完全落在突跃内」—— 我第一版这么写，结果
    #    石蕊(5.0~8.0)完全落在突跃 4.30~9.70 内被判为最优，而酚酞、甲基橙被判不合格，
    #    这与化学事实相反。
    #
    # 正确判据（人教版选择性必修一）：
    #   a) 变色范围与突跃范围**有重叠** —— 这样颜色变化才发生在 ±0.1% 误差之内
    #   b) 变色要**灵敏、明显** —— 石蕊在 5~8 之间由红渐变到蓝，过渡色难以判断终点，
    #      所以尽管范围落在突跃内，滴定仍不用它
    print(f'\n─── 指示剂能否用于强酸强碱滴定 ───')
    def overlaps(ind):
        return ind['hi'] > lo and ind['lo'] < hi
    for ind in INDICATORS:
        ok_range = overlaps(ind)
        width = ind['hi'] - ind['lo']
        sharp = width <= 2.0          # 变色范围窄 → 终点明显
        verdict = '可用' if (ok_range and sharp) else (
            '范围与突跃重叠但变色不明显，不用' if ok_range else '不可用')
        print(f"  {ind['name']:<6} {ind['lo']}~{ind['hi']:<5} 宽度 {width:>3.1f}  → {verdict}")

    ph = next(i for i in INDICATORS if i['id']=='phenolphthalein')
    mo = next(i for i in INDICATORS if i['id']=='methyl_orange')
    li = next(i for i in INDICATORS if i['id']=='litmus')
    # 酚酞与甲基橙都必须判为可用
    for ind in (ph, mo):
        if not (overlaps(ind) and (ind['hi']-ind['lo']) <= 2.0):
            bad += 1; print(f"  ❌ {ind['name']} 应判为可用")
    # 石蕊必须被排除，理由是变色范围过宽
    if (li['hi']-li['lo']) <= 2.0:
        bad += 1; print('  ❌ 石蕊的变色范围应明显宽于酚酞/甲基橙（这是它不适用的量化理由）')
    # 酚酞的变色起点、甲基橙的变色终点都必须落在突跃内（终点可判的实际依据）
    if not (lo <= ph['lo'] <= hi):
        bad += 1; print('  ❌ 酚酞变色起点 8.2 应落在突跃范围内')
    if not (lo <= mo['hi'] <= hi):
        bad += 1; print('  ❌ 甲基橙变色终点 4.4 应落在突跃范围内')

    print(f'\n  问题 {bad} 处')
    return 1 if bad else 0

if __name__ == '__main__':
    raise SystemExit(main())
