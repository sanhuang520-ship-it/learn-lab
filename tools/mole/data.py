#!/usr/bin/env python3
"""摩尔计算的物质表与常量。相对原子质量按人教版必修一附表（保留常见教学取值）。"""

NA = 6.02e23        # mol⁻¹
VM_STP = 22.4       # L/mol，⚠️ 只在标准状况(0 °C, 101 kPa)下、且只对气体成立

AR = {  # 相对原子质量（教学常用取值）
 'H':1, 'C':12, 'N':14, 'O':16, 'Na':23, 'Mg':24, 'Al':27, 'Si':28,
 'P':31, 'S':32, 'Cl':35.5, 'K':39, 'Ca':40, 'Fe':56, 'Cu':64, 'Zn':65,
 'Ag':108, 'Ba':137, 'He':4, 'Ne':20, 'Ar':40, 'Br':80, 'I':127,
}

# name, 化学式, 组成 {元素:个数}, 标况下是否气体, 是否由分子构成
#
# ⚠️ 最后一列很重要：NaCl / CaCO3 / NaOH / CuO / CuSO4 是**离子化合物，没有分子**。
#    对它们问「含多少个分子」是化学错误，老师会直接判错。
#    凡是问"分子数"的题，只能从 molecular=True 的物质里选。
SUBS = [
 ('水',       'H2O',   {'H':2,'O':1},          False, True),
 ('氧气',     'O2',    {'O':2},                True,  True),
 ('氢气',     'H2',    {'H':2},                True,  True),
 ('氮气',     'N2',    {'N':2},                True,  True),
 ('二氧化碳', 'CO2',   {'C':1,'O':2},          True,  True),
 ('一氧化碳', 'CO',    {'C':1,'O':1},          True,  True),
 ('氨气',     'NH3',   {'N':1,'H':3},          True,  True),
 ('氯气',     'Cl2',   {'Cl':2},               True,  True),
 ('甲烷',     'CH4',   {'C':1,'H':4},          True,  True),
 ('氯化氢',   'HCl',   {'H':1,'Cl':1},         True,  True),
 ('二氧化硫', 'SO2',   {'S':1,'O':2},          True,  True),
 ('氦气',     'He',    {'He':1},               True,  True),   # 稀有气体按单原子分子处理
 ('硫酸',     'H2SO4', {'H':2,'S':1,'O':4},    False, True),
 ('葡萄糖',   'C6H12O6',{'C':6,'H':12,'O':6},  False, True),
 ('乙醇',     'C2H6O', {'C':2,'H':6,'O':1},    False, True),
 ('氯化钠',   'NaCl',  {'Na':1,'Cl':1},        False, False),  # 离子化合物，无分子
 ('碳酸钙',   'CaCO3', {'Ca':1,'C':1,'O':3},   False, False),
 ('氢氧化钠', 'NaOH',  {'Na':1,'O':1,'H':1},   False, False),
 ('氧化铜',   'CuO',   {'Cu':1,'O':1},         False, False),
 ('硫酸铜',   'CuSO4', {'Cu':1,'S':1,'O':4},   False, False),
]

def molar_mass(comp):
    return round(sum(AR[e]*n for e, n in comp.items()), 2)

if __name__ == '__main__':
    print(f"{'物质':<10}{'化学式':<10}{'M (g/mol)':>10}   标况气体  有分子")
    print('-'*54)
    for name, f, comp, gas, mol in SUBS:
        print(f"{name:<10}{f:<10}{molar_mass(comp):>10}   {'是' if gas else '否':<8}{'是' if mol else '否'}")
