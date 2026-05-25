你要帮我实现一个 PPT 配图自动化流水线。项目目标是根据我提供的图片任务表，自动下载/读取文献、提取或重绘图片，并生成可用于 PPT 的图片资源包。
## 输入文件
我会把以下文件放在项目根目录目录中：
- `image_tasks_for_codex.xlsx`
- `image_tasks_for_codex.csv`
- `image_tasks_for_codex.json`
- `references.csv`
- `README_naming_and_manifest.md`
请优先读取 `image_tasks_for_codex.csv` 或 `image_tasks_for_codex.json`。每一行是一个配图任务，`task_id` 对应原文档的 PPT 页码与图片指引，例如 `P07-B` 表示“第 7 页，图片指引 B”。
## 总体要求
请创建一个 Python 项目，目录结构如下：
```text
ppt_image_pipeline/
  input/
    image_tasks_for_codex.csv
    image_tasks_for_codex.json
    references.csv
    pdfs/
  output/
    images/
    placeholders/
    metadata/
    contact_sheet/
    manifest.csv
    manifest.xlsx
  scripts/
    run_pipeline.py
    fetch_sources.py
    redraw_chemistry.py
    extract_pdf_figures.py
    draw_diagrams.py
    make_charts.py
    make_contact_sheet.py
  README.md
  requirements.txt
```
## 命名规则，必须严格遵守
每个输出图片文件名必须保留 `task_id`，这样我能知道它对应文档中的哪一条图片指引。
主格式：
```text
{task_id}__{short_slug}__{source_locator}__{action}__candidateNN.{ext}
```
例：
```text
P07-B__ionic_liquid_optimization_reuse_fig8_fig9__R13_Fig8_Fig9_pdfp9_p10__extract_specific_figures_or_redraw_chart__candidate01.png
```
如果找不到图、无法下载、无法确认图号、或无权限访问，必须生成占位文件，不要直接失败：
```text
{task_id}__{short_slug}__{source_locator}__MISSING_NEEDS_REVIEW.txt
```
占位文件要写清楚：`task_id`、推荐图片、来源、DOI/链接、文献位置、失败原因、人工下一步建议。
## 自动化策略
请根据 `recommended_action` 分流：
### 1. PubChem / 化学结构重绘
适用于：
- `P01-A`
- `P02-A`
- `P02-B`
要求：
- 使用 PubChem PUG-REST 获取结构数据。
- 使用 RDKit 重绘二维结构式。
- 输出 SVG 和 PNG。
- 不要截图 PubChem 页面。
- `P02-A` 需要水杨酸与阿司匹林对比。阿司匹林 CID 是 2244；水杨酸可通过 PubChem 按名称 `salicylic acid` 查询。
- `P02-B` 绘制核心反应式：水杨酸 + 乙酸酐 → 乙酰水杨酸 + 乙酸。
### 2. 自绘流程图、风险图、路线图、比较表
适用于：
- `P01-B`
- `P03-A`
- `P04-A`
- `P05-B`
- `P07-C`
- `P08-A`
- `P08-B`
- `P09-A`
要求：
- 使用 Python 生成简洁、中文可读、适合 PPT 的 SVG/PNG。
- 可以使用 matplotlib、graphviz、drawsvg、Pillow、python-pptx 或其他合适库。
- 图内文字要短，不要堆长段落。
- 必须把图注写入 manifest。
- 这些图本质上是“据文献整理/重绘”，不要声称为原文献原图。
### 3. 论文 PDF/网页局部图提取或重绘
适用于：
- `P03-B`
- `P04-B`
- `P06-A`
- `P06-B`
- `P07-A`
- `P07-B`
- `P09-B`
要求：
- 从互联网下载获取 PDF，下载到”papers“文件夹中
- 对于明确给出图号/页码的任务，优先裁取局部：
  - `P07-A`: 文献[13] Fig. 3，PDF 第 4/12 页
  - `P07-B`: 文献[13] Fig. 8，PDF 第 9/12 页；Fig. 9，PDF 第 10/12 页
  - `P06-B`: 文献[9] Scheme 1 / Table 2
  - `P04-B`: SDS 第 5/13 页、第 7/13 页的局部安全信息
- 对于图号未核实的任务，生成候选图并标记 `CANDIDATE_NEEDS_REVIEW`，或重绘简化图。
- 如果 PDF 无法访问或图找不到，生成 missing placeholder。
推荐工具：
- `requests`：下载开放资源
- `PyMuPDF` / `fitz`：PDF 页面渲染和裁剪
- `pdfplumber`：表格和文本提取
- `Pillow`：图片裁剪、拼接、格式转换
- `matplotlib`：重绘统计图
- `RDKit`：化学结构图
## Manifest 输出要求
最终生成：
```text
output/manifest.csv
output/manifest.xlsx
```
字段至少包括：
```text
task_id
ppt_page
guide_label
recommended_image
output_file
status
source_refs
doi_or_link
source_locator
action_taken
caption
manual_review
notes
```
状态枚举：
```text
DONE_REDRAW
DONE_EXTRACTED
DONE_SELF_DRAWN
CANDIDATE_NEEDS_REVIEW
MISSING_NEEDS_REVIEW
SKIPPED_BY_POLICY_OR_ACCESS
```
## Contact sheet
请生成一个总览检查文件：
```text
output/contact_sheet/contact_sheet.pdf
```
每张候选图旁边显示：
- `task_id`
- 推荐图片主题
- 文件名
- 状态
- 图注
- 是否需要人工复核
这样我可以快速检查每张图是不是对应正确。
## 失败处理
任何单个任务失败，都不能导致整个流水线停止。每个失败任务都必须：
1. 写入 manifest
2. 生成 missing placeholder
3. 在控制台日志中说明原因
4. 继续执行后面的任务
## 最重要的质量要求
1. 所有输出文件名必须能看出对应原文档的图片指引。
2. 所有重绘图必须注明“据文献整理/重绘”。
3. 不能用无来源网络图片替代文献图片。
4. 对需要核实的图，必须保留 `CANDIDATE_NEEDS_REVIEW` 或 `manual_review=Yes`。
5. 即使图片找不到，也要留下明确的占位文件和原因。
