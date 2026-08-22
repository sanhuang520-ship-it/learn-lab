#!/usr/bin/env python3
"""实验安全条目的结构校验。

⚠️ 这一页的内容原则：**不写任何原创的安全判断**。
安全内容写错会真的伤到人，所以每条都必须能指回教材或实验室通则，
`src` 字段是硬性要求，缺了就报错。
"""
import json, sys, collections

REQUIRED = ('id', 'cat', 'q', 'ok', 'why', 'src')
CATS = {'heat', 'acid', 'eye', 'smell', 'take', 'fire', 'glass'}

def main(path):
    d = json.load(open(path, encoding='utf-8'))
    bad = 0
    ids = collections.Counter(x.get('id') for x in d)
    for x in d:
        p = f"[{x.get('id','?')}]"
        for k in REQUIRED:
            if k not in x or x[k] in ('', None):
                print(f'  ❌ {p} 缺字段 {k}'); bad += 1
        if x.get('cat') not in CATS:
            print(f"  ❌ {p} 未知分类 {x.get('cat')}"); bad += 1
        if not isinstance(x.get('ok'), bool):
            print(f'  ❌ {p} ok 必须是布尔值'); bad += 1
        if ids[x.get('id')] > 1:
            print(f'  ❌ {p} id 重复'); bad += 1
        if len(x.get('why', '')) < 12:
            print(f'  ❌ {p} why 太短，说不清为什么'); bad += 1
    c = collections.Counter(x['cat'] for x in d)
    print(f"\n  分类分布：{dict(c)}")
    t = sum(1 for x in d if x['ok'])
    print(f"  正确陈述 {t} 条 / 错误陈述 {len(d)-t} 条")
    if t == 0 or t == len(d):
        print('  ❌ 全对或全错，学生能靠猜通关'); bad += 1
    print(f"  共 {len(d)} 条，问题 {bad} 处")
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
