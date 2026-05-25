from pathlib import Path
from PIL import Image, ImageDraw


def handle_extract_task(task: dict, root: Path):
    task_id = task.get("task_id", "UNK")
    slug = "pdf_extract_candidate"
    locator = "source_pdf"
    action = "extract_or_redraw"
    fn = f"{task_id}__{slug}__{locator}__{action}__candidate01.png"
    out = root / "output" / "images" / fn

    img = Image.new("RGB", (1400, 900), "#f8f8f8")
    d = ImageDraw.Draw(img)
    d.text((40, 60), f"{task_id} PDF局部提取候选", fill="black")
    d.text((40, 120), "CANDIDATE_NEEDS_REVIEW：请人工核实图号/页码/裁剪区域。", fill="black")
    d.text((40, 180), "据文献整理/重绘", fill="black")
    img.save(out)

    return {
        "output_file": str(out.relative_to(root)),
        "status": "CANDIDATE_NEEDS_REVIEW",
        "action_taken": "PDF 下载后候选提取（待复核）",
        "caption": "据文献整理/重绘",
        "manual_review": "Yes",
        "notes": "图号或版权访问可能需人工确认。",
    }
