import json
from pathlib import Path

# ===== 修改这里的文件路径为你的老师的 Notebook 文件名 =====
input_file = Path("./Lab5/Lab5.ipynb")
output_file = input_file.with_stem(input_file.stem + "_escaped")

# ===== 读取并处理 =====
with open(input_file, "r", encoding="utf-8") as f:
    notebook = json.load(f)

modified = 0
for cell in notebook.get("cells", []):
    if cell.get("cell_type") == "markdown":
        new_source = []
        for line in cell.get("source", []):
            # 替换未转义的美元符号（避免重复转义）
            fixed_line = line.replace("\\$", "💲TEMP💲").replace("$", "\\$").replace("💲TEMP💲", "\\$")
            new_source.append(fixed_line)
        if new_source != cell.get("source"):
            cell["source"] = new_source
            modified += 1

# ===== 写回文件 =====
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print(f"✅ 完成！已修复 {modified} 个 Markdown 单元格。")
print(f"输出文件：{output_file}")
