from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def make_contact_sheet(manifest, root: Path):
    out_pdf = root / "output" / "contact_sheet" / "contact_sheet.pdf"
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(out_pdf) as pdf:
        for _, row in manifest.iterrows():
            fig = plt.figure(figsize=(11.7, 8.3))
            plt.axis("off")
            text = (
                f"task_id: {row.get('task_id','')}\n"
                f"recommended: {row.get('recommended_image','')}\n"
                f"file: {row.get('output_file','')}\n"
                f"status: {row.get('status','')}\n"
                f"caption: {row.get('caption','')}\n"
                f"manual_review: {row.get('manual_review','')}"
            )
            plt.text(0.05, 0.9, text, fontsize=12, va="top")
            pdf.savefig(fig)
            plt.close(fig)
