#!/usr/bin/env python3
"""按关卡生成摩尔计算题。答案一律由程序算，避免题面与答案对不上。"""
import sys, json, random
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from data import SUBS, AR, NA, VM_STP, molar_mass

NICE_N = [0.1, 0.2, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5]

def fmt(x):
    """去掉浮点尾巴：2.0 -> 2，0.50 -> 0.5"""
    r = round(x, 4)
    return str(int(r)) if abs(r - int(r)) < 1e-9 else str(r)

def sci23(n):
    """n mol 对应的粒子数，写成 a×10²³ 的形式"""
    return fmt(round(n * 6.02, 4))

def gases():      return [s for s in SUBS if s[3]]
def molecular():  return [s for s in SUBS if s[4]]          # 只有这些能问"分子数"
def gas_mol():    return [s for s in SUBS if s[3] and s[4]]

def L1(rng):
    """质量 ↔ 物质的量"""
    name, f, comp, gas, mol = rng.choice(SUBS)
    M = molar_mass(comp); n = rng.choice(NICE_N); m = round(n * M, 3)
    if rng.random() < .5:
        return dict(level=1, ask=f'{fmt(m)} g {name}（{f}）是多少 mol？',
                    given=f'M({f}) = {fmt(M)} g/mol', unit='mol', ans=n,
                    sol=f'n = m ÷ M = {fmt(m)} ÷ {fmt(M)} = {fmt(n)} mol')
    return dict(level=1, ask=f'{fmt(n)} mol {name}（{f}）的质量是多少 g？',
                given=f'M({f}) = {fmt(M)} g/mol', unit='g', ans=m,
                sol=f'm = n × M = {fmt(n)} × {fmt(M)} = {fmt(m)} g')

def L2(rng):
    """物质的量 ↔ 粒子数。⚠️ 只能用由分子构成的物质 —— 离子化合物没有分子。"""
    name, f, comp, gas, mol = rng.choice(molecular())
    n = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 1.5, 2, 3])
    if rng.random() < .5:
        return dict(level=2, ask=f'{sci23(n)}×10²³ 个 {name} 分子是多少 mol？',
                    given='N_A = 6.02×10²³ mol⁻¹', unit='mol', ans=n,
                    sol=f'n = N ÷ N_A = {sci23(n)}×10²³ ÷ 6.02×10²³ = {fmt(n)} mol')
    return dict(level=2, ask=f'{fmt(n)} mol {name} 含多少个分子？（填 a×10²³ 中的 a）',
                given='N_A = 6.02×10²³ mol⁻¹', unit='×10²³ 个', ans=round(n*6.02, 4),
                sol=f'N = n × N_A = {fmt(n)} × 6.02×10²³ = {sci23(n)}×10²³ 个')

def L3(rng):
    """物质的量 ↔ 气体体积（标况）"""
    name, f, comp, gas, mol = rng.choice(gases())
    n = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 1.5, 2, 2.5])
    V = round(n * VM_STP, 3)
    if rng.random() < .5:
        return dict(level=3, ask=f'标准状况下，{fmt(V)} L {name}（{f}）是多少 mol？',
                    given='标况下 V_m = 22.4 L/mol', unit='mol', ans=n,
                    sol=f'n = V ÷ V_m = {fmt(V)} ÷ 22.4 = {fmt(n)} mol')
    return dict(level=3, ask=f'标准状况下，{fmt(n)} mol {name}（{f}）体积是多少 L？',
                given='标况下 V_m = 22.4 L/mol', unit='L', ans=V,
                sol=f'V = n × V_m = {fmt(n)} × 22.4 = {fmt(V)} L')

def L4(rng):
    """跨两步换算"""
    kind = rng.choice(['m2N', 'V2m', 'm2V'])
    if kind == 'm2N':
        name, f, comp, gas, mol = rng.choice(molecular())   # 同 L2，问分子数只能用分子型
        M = molar_mass(comp); n = rng.choice([0.1, 0.25, 0.5, 1, 2])
        m = round(n * M, 3)
        return dict(level=4, ask=f'{fmt(m)} g {name}（{f}）含多少个分子？（填 a×10²³ 中的 a）',
                    given=f'M = {fmt(M)} g/mol，N_A = 6.02×10²³ mol⁻¹', unit='×10²³ 个',
                    ans=round(n*6.02, 4),
                    sol=f'先 n = {fmt(m)} ÷ {fmt(M)} = {fmt(n)} mol，再 N = {fmt(n)} × 6.02×10²³ = {sci23(n)}×10²³')
    if kind == 'V2m':
        name, f, comp, gas, mol = rng.choice(gases())
        M = molar_mass(comp); n = rng.choice([0.1, 0.25, 0.5, 1, 2])
        V = round(n * VM_STP, 3); m = round(n * M, 3)
        return dict(level=4, ask=f'标准状况下 {fmt(V)} L {name}（{f}）的质量是多少 g？',
                    given=f'V_m = 22.4 L/mol，M = {fmt(M)} g/mol', unit='g', ans=m,
                    sol=f'先 n = {fmt(V)} ÷ 22.4 = {fmt(n)} mol，再 m = {fmt(n)} × {fmt(M)} = {fmt(m)} g')
    name, f, comp, gas, mol = rng.choice(gases())
    M = molar_mass(comp); n = rng.choice([0.1, 0.25, 0.5, 1, 2])
    m = round(n * M, 3); V = round(n * VM_STP, 3)
    return dict(level=4, ask=f'{fmt(m)} g {name}（{f}）在标准状况下体积是多少 L？',
                given=f'M = {fmt(M)} g/mol，V_m = 22.4 L/mol', unit='L', ans=V,
                sol=f'先 n = {fmt(m)} ÷ {fmt(M)} = {fmt(n)} mol，再 V = {fmt(n)} × 22.4 = {fmt(V)} L')

# ── 第 5 关：陷阱判断（选择题，不是填空）
TRAPS = [
 dict(level=5, ask='常温常压下，1 mol 氧气的体积是 22.4 L。', ok=False,
      sol='22.4 L/mol 只在**标准状况**（0 °C、101 kPa）下成立。常温常压（一般指 25 °C、101 kPa）下，1 mol 气体体积约 24.5 L，不是 22.4 L。'),
 dict(level=5, ask='标准状况下，1 mol 水的体积是 22.4 L。', ok=False,
      sol='标准状况下水是**液体**，不是气体。22.4 L/mol 只适用于气体。1 mol 水约 18 g，体积约 18 mL。'),
 dict(level=5, ask='标准状况下，1 mol 任何气体的体积都约为 22.4 L。', ok=True,
      sol='对。标况下气体摩尔体积与气体种类无关，这正是阿伏加德罗定律的推论。'),
 dict(level=5, ask='1 mol 氢气含 6.02×10²³ 个氢原子。', ok=False,
      sol='1 mol H₂ 含 6.02×10²³ 个**氢分子**，而每个 H₂ 里有 2 个氢原子，所以是 1.204×10²⁴ 个氢原子。**分子和原子要分清**。'),
 dict(level=5, ask='摩尔质量的单位是 g/mol，相对分子质量没有单位。', ok=True,
      sol='对。相对分子质量是个比值，没有单位；摩尔质量有单位 g/mol。两者数值相等，别把概念混了。'),
 dict(level=5, ask='标准状况下，22.4 L 氯气的质量是 71 g。', ok=True,
      sol='对。标况下 22.4 L 即 1 mol，M(Cl₂) = 35.5 × 2 = 71 g/mol，所以质量 71 g。'),
 dict(level=5, ask='0.5 mol 硫酸（H₂SO₄）中含 1 mol 氢原子。', ok=True,
      sol='对。每个 H₂SO₄ 含 2 个 H，0.5 mol × 2 = 1 mol 氢原子。'),
 dict(level=5, ask='标准状况下 11.2 L 二氧化碳的质量是 44 g。', ok=False,
      sol='11.2 L 是 0.5 mol（11.2 ÷ 22.4），质量 = 0.5 × 44 = **22 g**，不是 44 g。44 g 对应的是 1 mol、22.4 L。'),
]

GENS = {1: L1, 2: L2, 3: L3, 4: L4}

def make(level, seed):
    rng = random.Random(seed)
    if level == 5:
        return TRAPS
    return [GENS[level](rng) for _ in range(60)]

if __name__ == '__main__':
    out = {}
    for lv in (1, 2, 3, 4):
        out[lv] = make(lv, 20260821 + lv)
    out[5] = TRAPS
    json.dump(out, open(str(__import__('pathlib').Path(__file__).resolve().parent / 'problems.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    for lv in (1,2,3,4,5):
        print(f'  第 {lv} 关：{len(out[lv])} 题')
    print('\n  抽样：')
    for lv in (1,2,3,4):
        p = out[lv][0]
        print(f"   L{lv} {p['ask']}\n       答 {fmt(p['ans'])} {p['unit']} | {p['sol']}")
