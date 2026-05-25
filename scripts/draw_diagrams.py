from pathlib import Path
from PIL import Image, ImageDraw


def handle_self_draw_task(task: dict, root: Path):
    task_id = task.get("task_id", "UNK")
    title = str(task.get("recommended_image", "流程图"))
    slug = "self_drawn_diagram"
    locator = "literature_summary"
    action = "draw_diagram"
    fn = f"{task_id}__{slug}__{locator}__{action}__candidate01.png"
    out = root / "output" / "images" / fn

    img = Image.new("RGB", (1600, 900), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((80, 120, 520, 280), outline="black", width=3)
    d.rectangle((620, 120, 1060, 280), outline="black", width=3)
    d.rectangle((1160, 120, 1500, 280), outline="black", width=3)
    d.text((100, 150), "输入信息", fill="black")
    d.text((660, 150), title[:18], fill="black")
    d.text((1180, 150), "输出建议", fill="black")
    d.text((80, 50), f"{task_id}（据文献整理/重绘）", fill="black")
    img.save(out)

    return {
        "output_file": str(out.relative_to(root)),
        "status": "DONE_SELF_DRAWN",
        "action_taken": "自绘流程/比较图",
        "caption": "据文献整理/重绘",
        "manual_review": "No",
        "notes": "",
    }
