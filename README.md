# PPT Image Pipeline

根据 `input/image_tasks_for_codex.csv` 或 `input/image_tasks_for_codex.json` 自动生成 PPT 配图资源与清单。

## 运行

```bash
python scripts/run_pipeline.py
```

输出位于 `output/`：
- `images/`：候选图/重绘图
- `placeholders/`：缺失占位文件
- `files/`：下载的 PDF/网页资源
- `manifest.csv` / `manifest.xlsx`：任务执行清单
- `contact_sheet/contact_sheet.pdf`：总览检查
