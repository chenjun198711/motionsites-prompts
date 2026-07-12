import json
import os

def generate_markdown():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(base_dir, "motionsites_all_prompts.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    with open(os.path.join(base_dir, "motionsites_prompts_report.md"), "w", encoding="utf-8") as f:
        f.write("# MotionSites 提示词一键提取报告\n\n")
        f.write(f"从 MotionSites 网站提取的 **{len(data)}** 个提示词汇总及详细内容。\n\n")

        f.write("## 提示词汇总表\n\n")
        f.write("| 序号 | 标题 | 分类 | 平台 | 权限类型 | 提示词预览 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")

        for i, item in enumerate(data, 1):
            title = item.get("title", "N/A")
            category = item.get("category", "N/A")
            platform = "App" if item.get("platform") == "app" else "Website"
            is_free = "✅ 免费" if item.get("is_free") else "💎 Premium"
            prompt_raw = item.get("prompt_text", "")
            prompt_preview = prompt_raw.replace("\n", " ")
            if len(prompt_preview) > 60:
                prompt_preview = prompt_preview[:57] + "..."
            f.write(f"| {i} | {title} | {category} | {platform} | {is_free} | {prompt_preview} |\n")

        f.write("\n\n## 详细提示词内容\n\n")
        for item in data:
            title = item.get("title", "N/A")
            category = item.get("category", "N/A")
            platform = "App" if item.get("platform") == "app" else "Website"
            is_free = "免费" if item.get("is_free") else "Premium"
            prompt_text = item.get("prompt_text", "")

            f.write(f"### 🚀 {title}\n")
            f.write(f"- **所属分类**: {category}\n")
            f.write(f"- **平台**: {platform}\n")
            f.write(f"- **访问权限**: {is_free}\n")
            f.write("- **完整提示词**:\n\n")
            f.write(f"```text\n{prompt_text}\n```\n\n")
            f.write("---\n\n")

    print(f"Report generated at {os.path.join(base_dir, 'motionsites_prompts_report.md')}")

if __name__ == "__main__":
    generate_markdown()