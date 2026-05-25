import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from fetch_sources import fetch_source_file
from redraw_chemistry import handle_chemistry_task
from draw_diagrams import handle_self_draw_task
from extract_pdf_figures import handle_extract_task
from make_contact_sheet import make_contact_sheet

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "input"
OUTPUT = ROOT / "output"
IMAGES = OUTPUT / "images"
PLACEHOLDERS = OUTPUT / "placeholders"

MANIFEST_COLUMNS = [
    "task_id", "ppt_page", "guide_label", "recommended_image", "output_file",
    "status", "source_refs", "doi_or_link", "source_locator", "action_taken",
    "caption", "manual_review", "notes"
]

CHEM_TASKS = {"P01-A", "P02-A", "P02-B"}
SELF_DRAW_TASKS = {"P01-B", "P03-A", "P04-A", "P05-B", "P07-C", "P08-A", "P08-B", "P09-A"}
EXTRACT_TASKS = {"P03-B", "P04-B", "P06-A", "P06-B", "P07-A", "P07-B", "P09-B"}


def slugify(text: str) -> str:
    keep = [c.lower() if c.isalnum() else "_" for c in str(text)]
    s = "".join(keep)
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")[:80] or "task"


def load_tasks() -> pd.DataFrame:
    csv_file = INPUT / "image_tasks_for_codex.csv"
    json_file = INPUT / "image_tasks_for_codex.json"
    if csv_file.exists():
        return pd.read_csv(csv_file)
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def make_placeholder(task: Dict, reason: str) -> str:
    task_id = task.get("task_id", "UNKNOWN")
    short_slug = slugify(task.get("recommended_image", "missing"))
    locator = slugify(task.get("source_locator", "no_source"))
    fn = f"{task_id}__{short_slug}__{locator}__MISSING_NEEDS_REVIEW.txt"
    p = PLACEHOLDERS / fn
    p.write_text(
        f"task_id: {task_id}\n"
        f"recommended_image: {task.get('recommended_image','')}\n"
        f"source_refs: {task.get('source_refs','')}\n"
        f"doi_or_link: {task.get('doi_or_link','')}\n"
        f"source_locator: {task.get('source_locator','')}\n"
        f"failure_reason: {reason}\n"
        "next_step: 人工确认来源链接、图号或替代重绘方案。\n",
        encoding="utf-8",
    )
    return str(p.relative_to(ROOT))


def main():
    OUTPUT.mkdir(exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    PLACEHOLDERS.mkdir(parents=True, exist_ok=True)

    tasks = load_tasks()
    refs = pd.read_csv(INPUT / "references.csv") if (INPUT / "references.csv").exists() else pd.DataFrame()
    rows: List[Dict] = []

    for _, task_row in tasks.iterrows():
        task = task_row.to_dict()
        task_id = str(task.get("task_id", ""))
        base = {c: task.get(c, "") for c in MANIFEST_COLUMNS}
        base["manual_review"] = "No"

        try:
            fetch_source_file(task, refs, ROOT)
            if task_id in CHEM_TASKS:
                result = handle_chemistry_task(task, ROOT)
            elif task_id in SELF_DRAW_TASKS:
                result = handle_self_draw_task(task, ROOT)
            elif task_id in EXTRACT_TASKS:
                result = handle_extract_task(task, ROOT)
            else:
                result = {"status": "CANDIDATE_NEEDS_REVIEW", "manual_review": "Yes", "notes": "未分类任务，需人工处理", "output_file": ""}

            base.update(result)
            if not base.get("output_file"):
                base["output_file"] = make_placeholder(task, base.get("notes", "No output generated"))
                base["status"] = "MISSING_NEEDS_REVIEW"
                base["manual_review"] = "Yes"
        except Exception as e:
            base["status"] = "MISSING_NEEDS_REVIEW"
            base["manual_review"] = "Yes"
            base["notes"] = f"Pipeline error: {e}"
            base["output_file"] = make_placeholder(task, str(e))

        if not base.get("caption"):
            base["caption"] = "据文献整理/重绘"
        rows.append(base)

    manifest = pd.DataFrame(rows, columns=MANIFEST_COLUMNS)
    manifest.to_csv(OUTPUT / "manifest.csv", index=False)
    manifest.to_excel(OUTPUT / "manifest.xlsx", index=False)
    make_contact_sheet(manifest, ROOT)
    print("Pipeline complete.")


if __name__ == "__main__":
    main()
