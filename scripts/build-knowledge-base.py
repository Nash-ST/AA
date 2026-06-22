import os
import re
from pathlib import Path
from pypdf import PdfReader

SOURCE_DIR = r"E:\建筑类\施工图集"
OUTPUT_FILE = r"C:\Users\Nong\Documents\Codex\2026-06-20\z-g\AA-repo\docs\construction-knowledge-base.md"

# 分类规则
CATEGORY_RULES = [
    (r'1[56]G101|04G101|钢筋平法|平法', '平法图集'),
    (r'GB50\d{3}|GB/T.*\d{3}', '国家标准规范'),
    (r'JGJ\d{3}', '行业规范'),
    (r'02S515|05S502|05S804|09S304|10S505|03S402|05S804|14SS706', '给排水图集'),
    (r'02J401|15J401|15J403|02J503|07CJ11|07J501|09J202|11J508|12J609|13J404|14j936|16J601|16-GB.*电梯|电梯', '建筑构造/门窗/幕墙'),
    (r'11ZJ311|05系列.*防水|防水', '防水工程'),
    (r'11ZJ401|11ZJ411|15J403', '栏杆/楼梯'),
    (r'11ZJ501|15ZJ001|15ZJ201|05J909|11ZJ901|12J003|15ZJ512|15ZTJ514|广西烟道', '建筑装修/屋面/装饰'),
    (r'12G614|04G361|10G409|挡土墙|砌体|填充墙', '结构/桩基/砌体'),
    (r'GB50016|防火|消防|12J609.*防火', '防火规范'),
    (r'55021|55034|安全|安全卫生', '安全规范'),
    (r'GB5020[234567]|GB5030[03]|GB50550|GB50608|GB50628|50210|50327|50319|50326|50496|50209', '施工质量验收规范'),
    (r'施工手册|施工工艺|编制指南|图纸会审|标准化', '施工工艺/手册'),
    (r'智能|弱电', '智能化/弱电'),
    (r'地基|基础|桩|深基坑', '地基基础'),
    (r'保温|节能|幕墙', '节能/幕墙'),
]

def categorize(name):
    for pattern, cat in CATEGORY_RULES:
        if re.search(pattern, name, re.IGNORECASE):
            return cat
    return '其他'

def extract_standard_number(name):
    m = re.search(r'(GB[5]?T?\d{4}-\d{4}|JGJ\d{4}|0\dJ\d{3}[-\d]*|1[2-5]G\d{3}[-\d]*|1[2-5]ZJ\d{3}[-\d]*)', name)
    return m.group(1) if m else ''

def extract_pages(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception:
        return '?'

print("正在扫描 PDF 文件...")
files = sorted(Path(SOURCE_DIR).glob("*.pdf"))
results = []

for f in files:
    name = f.name
    size_mb = round(f.stat().st_size / 1024 / 1024, 2)
    pages = extract_pages(str(f))
    category = categorize(name)
    standard = extract_standard_number(name)
    results.append({
        'name': name,
        'standard': standard,
        'category': category,
        'pages': pages,
        'size_mb': size_mb,
    })
    if len(results) % 20 == 0:
        print(f"  已处理 {len(results)}/{len(files)}...")

print(f"\n共处理 {len(results)} 个文件，正在生成知识库...")

# 按分类分组
from collections import defaultdict
by_cat = defaultdict(list)
for r in results:
    by_cat[r['category']].append(r)

# 生成 Markdown
lines = []
lines.append("# 建筑施工知识图谱索引")
lines.append("")
lines.append("> 自动生成于 " + Path(__file__).parent.name if hasattr(Path(__file__), 'parent') else "")
lines.append(f"> 来源：E:\\建筑类\\施工图集")
lines.append(f"> 共 **{len(results)}** 个 PDF 文件，总大小 **{round(sum(r['size_mb'] for r in results)/1024, 1)} GB**")
lines.append(f"> 涵盖 **{len(by_cat)}** 个分类")
lines.append("")
lines.append("---")
lines.append("")

# 目录
lines.append("## 📑 目录")
lines.append("")
for cat in sorted(by_cat.keys()):
    anchor = cat.lower().replace(' ', '-')
    lines.append(f"- [{cat}](#{cat})")
lines.append("")
lines.append("---")
lines.append("")

# 按分类展开
for cat in sorted(by_cat.keys()):
    items = by_cat[cat]
    lines.append(f"## {cat} ({len(items)} 个文件)")
    lines.append("")
    lines.append("| 序号 | 文件名 | 标准编号 | 页数 | 大小(MB) |")
    lines.append("|------|--------|----------|------|----------|")
    for i, item in enumerate(items, 1):
        std = item['standard'] or "-"
        pg = str(item['pages']) if item['pages'] != '?' else "?"
        lines.append(f"| {i} | {item['name']} | {std} | {pg} | {item['size_mb']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

# 统计摘要
lines.append("## 📊 统计概览")
lines.append("")
total_size = round(sum(r['size_mb'] for r in results), 2)
avg_pages = round(sum(r['pages'] for r in results if isinstance(r['pages'], int)) / max(1, sum(1 for r in results if isinstance(r['pages'], int))), 1)
lines.append(f"- **文件总数**: {len(results)}")
lines.append(f"- **总大小**: {total_size} MB ({round(total_size/1024, 1)} GB)")
lines.append(f"- **平均页数**: {avg_pages}")
lines.append(f"- **分类数**: {len(by_cat)}")
lines.append(f"- **标准编号覆盖率**: {round(sum(1 for r in results if r['standard'])/len(results)*100, 1)}%")
lines.append("")

# 全部文件列表
lines.append("## 📂 全部文件清单")
lines.append("")
lines.append("| # | 文件名 | 分类 | 标准编号 | 页数 | 大小(MB) |")
lines.append("|---|--------|------|----------|------|----------|")
for i, item in enumerate(results, 1):
    lines.append(f"| {i} | {item['name']} | {item['category']} | {item['standard'] or '-'} | {item['pages']} | {item['size_mb']} |")
lines.append("")

output = "\n".join(lines)

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✅ 知识库已生成: {OUTPUT_FILE}")
print(f"   共 {len(results)} 个文件，{len(by_cat)} 个分类")
