#!/usr/bin/env python3
"""细胞器条目校验。

⚠️ 和实验安全页同样的原则：这一页写的是教材知识，`src` 是硬性字段。
另外专门校验「分泌蛋白的合成与运输路径」—— 这条路径的顺序是必考点，
写反了就是教错。
"""
import json, sys, collections

REQUIRED = ('id','name','en','job','detail','who','membrane','src')
MEMBRANE = {'none','single','double'}

# 分泌蛋白（如消化酶）的合成与运输路径，人教版必修一：
# 核糖体 → 内质网 → 高尔基体 → 细胞膜 → 细胞外
SECRETORY_PATH = ['ribosome','er','golgi','cellmembrane']

# 无膜细胞器（考点：核糖体和中心体没有膜）
NO_MEMBRANE = {'ribosome','centrosome'}
# 双膜细胞器（考点）
DOUBLE = {'nucleus','mitochondrion','chloroplast'}

def main(path):
    d = json.load(open(path, encoding='utf-8'))
    by = {x['id']: x for x in d}
    bad = 0
    ids = collections.Counter(x.get('id') for x in d)

    for x in d:
        p = f"[{x.get('id','?')}]"
        for k in REQUIRED:
            if not x.get(k):
                print(f'  ❌ {p} 缺字段 {k}'); bad += 1
        if x.get('membrane') not in MEMBRANE:
            print(f"  ❌ {p} membrane 取值非法：{x.get('membrane')}"); bad += 1
        if ids[x.get('id')] > 1:
            print(f'  ❌ {p} id 重复'); bad += 1
        if len(x.get('detail','')) < 30:
            print(f'  ❌ {p} detail 太短'); bad += 1

    # 膜结构分类必须和考点一致
    for i in NO_MEMBRANE:
        if i in by and by[i]['membrane'] != 'none':
            print(f'  ❌ [{i}] 应为无膜'); bad += 1
    for i in DOUBLE:
        if i in by and by[i]['membrane'] != 'double':
            print(f'  ❌ [{i}] 应为双膜'); bad += 1

    # 分泌蛋白路径上的四个环节必须都在，且都标了 link
    for i in SECRETORY_PATH:
        if i not in by:
            print(f'  ❌ 分泌蛋白路径缺少 {i}'); bad += 1
        elif by[i].get('link') != 'digestive':
            print(f'  ❌ [{i}] 在分泌蛋白路径上，link 应为 digestive'); bad += 1

    print(f"\n  路径校验：{' → '.join(by[i]['name'] for i in SECRETORY_PATH if i in by)} → 细胞外")
    print(f"  无膜 {sorted(x['name'] for x in d if x['membrane']=='none')}")
    print(f"  单膜 {sorted(x['name'] for x in d if x['membrane']=='single')}")
    print(f"  双膜 {sorted(x['name'] for x in d if x['membrane']=='double')}")
    print(f"\n  共 {len(d)} 个细胞器，问题 {bad} 处")
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
