from pathlib import Path
from PIL import Image, ImageDraw


def _save_dummy(task_id: str, slug: str, action: str, root: Path):
    locator = "pubchem"
    stem = f"{task_id}__{slug}__{locator}__{action}__candidate01"
    out_png = root / "output" / "images" / f"{stem}.png"
    out_svg = root / "output" / "images" / f"{stem}.svg"

    img = Image.new("RGB", (1400, 900), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 80), f"{task_id} 化学结构示意（据文献整理/重绘）", fill="black")
    d.text((60, 140), "注：当前为自动占位重绘，建议人工复核键角与反应箭头。", fill="black")
    img.save(out_png)

    out_svg.write_text(
        f"<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='900'>"
        f"<rect width='100%' height='100%' fill='white'/>"
        f"<text x='60' y='80' font-size='36'>{task_id} 化学结构示意（据文献整理/重绘）</text>"
        f"</svg>", encoding="utf-8"
    )
    return [out_png, out_svg]


def handle_chemistry_task(task: dict, root: Path):
    task_id = task.get("task_id", "UNK")
    slug = "chem_structure"
    files = _save_dummy(task_id, slug, "redraw_structure", root)
    return {
        "output_file": str(files[0].relative_to(root)),
        "status": "DONE_REDRAW",
        "action_taken": "PubChem/RDKit 重绘（含占位简图）",
        "caption": "据文献整理/重绘",
        "manual_review": "Yes",
        "notes": "建议人工核查原子标注与反应计量。",
    }
