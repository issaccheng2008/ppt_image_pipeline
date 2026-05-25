# PPT 配图自动化命名规则

来源文件：`deep-research-report (1).md`

本项目用 `task_id` 作为每张图的稳定编号。`task_id` 来自文档中的 PPT 页码与局部图片指引：

- `P01-A` = 第 1 页，图片指引 A
- `P07-B` = 第 7 页，图片指引 B
- 以此类推

## 输出文件主命名格式

```text
{task_id}__{short_slug}__{source_locator}__{action}__candidateNN.{ext}
```

示例：

```text
P07-B__ionic_liquid_optimization_reuse_fig8_fig9__R13_Fig8_Fig9_pdfp9_p10__extract_specific_figures_or_redraw_chart__candidate01.png
```

这个文件名能直接看出：

1. 对应文档中的哪条图片指引：`P07-B`
2. 图片主题：`ionic_liquid_optimization_reuse_fig8_fig9`
3. 来源文献/图号/页码：`R13_Fig8_Fig9_pdfp9_p10`
4. 处理方式：`extract_specific_figures_or_redraw_chart`
5. 若同一任务有多个候选图，用 `candidate01`, `candidate02` 区分

## 找不到图片时的占位文件

如果文献无法访问、图号无法确认、PDF 下载失败或提取失败，不要中断任务。生成：

```text
{task_id}__{short_slug}__{source_locator}__MISSING_NEEDS_REVIEW.txt
```

占位文件内容建议写明：

- 原始 `task_id`
- 推荐图片主题
- 预期来源文献与 DOI/链接
- 预期图号/页码
- 失败原因
- 下一步人工建议

## Manifest 规则

Codex 最终应生成 `output/manifest.csv`，至少包含：

```text
task_id, output_file, status, source_used, source_locator, action_taken, caption, notes
```

推荐状态：

- `DONE_REDRAW`：已重绘
- `DONE_EXTRACTED`：已从 PDF/网页局部提取
- `DONE_SELF_DRAWN`：已自绘概念图/流程图/表格
- `CANDIDATE_NEEDS_REVIEW`：已生成候选图但需要人工核实
- `MISSING_NEEDS_REVIEW`：未找到或不可访问，已生成占位说明
- `SKIPPED_BY_POLICY_OR_ACCESS`：因权限/版权/访问限制跳过

## 重要约束

- 不要绕过付费墙。
- 不要批量抓取违反网站条款的图片。
- 优先重绘化学结构、反应式、流程图、统计图。
- 原图截图只用于明确允许/可访问且与任务强相关的局部图。
- 所有图片都必须在 manifest 中保留来源、处理动作和图注。
