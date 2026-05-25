from pathlib import Path
import requests


def fetch_source_file(task: dict, refs, root: Path):
    out_dir = root / "output" / "files"
    out_dir.mkdir(parents=True, exist_ok=True)

    link = str(task.get("doi_or_link", "")).strip()
    if not link.startswith("http"):
        return None

    safe_name = f"{task.get('task_id','task')}.pdf"
    out_file = out_dir / safe_name
    if out_file.exists():
        return out_file

    try:
        r = requests.get(link, timeout=20)
        if r.status_code == 200 and r.content:
            out_file.write_bytes(r.content)
            return out_file
    except Exception:
        return None
    return None
