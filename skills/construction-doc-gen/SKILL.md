# Construction Document Generator Skill

## Overview

Generate standardized Chinese construction industry documents from project data.

## Triggers

- "生成施工方案"
- "create construction plan"
- "document:construction"

## Workflow

1. Collect project parameters from user
2. Load template from \	emplates/construction/\
3. Fill template with project data
4. Validate against GB standards checklist
5. Output Markdown document
6. Convert to Word (.docx) if requested

## Supported Document Types

| Type | Template Path | Standard |
|------|--------------|----------|
| 施工方案 | \	emplates/construction/construction-plan.md\ | GB 50300 |
| 安全交底 | \	emplates/safety/safety-disclosure.md\ | JGJ 59 |
| 质量验收 | \	emplates/quality/quality-inspection.md\ | GB 50204 |
| 施工合同 | \	emplates/contract/construction-contract.md\ | GF-2017-0201 |
| 监理月报 | \	emplates/report/supervision-monthly.md\ | GB/T 50319 |

## Output Format

- Default: Markdown (\.md\)
- Optional: Word (\.docx\) via \scripts/md-to-docx.py\

## Quality Checklist

- [ ] All GB standard references current
- [ ] Unit conversions correct (mm, m, m², m³)
- [ ] Table formatting consistent
- [ ] Sign-off sections complete
