# 🏗️ 建筑工程 AI 文档自动生成工作流

> Codex + GitHub + Markdown + Word 一体化解决方案

## 概述

本项目为建筑行业提供一站式的 AI 驱动文档自动生成工作流，涵盖施工方案、安全交底、质量验收、监理月报等核心文档类型。

## 架构

```
AA-repo/
├── templates/           # 行业标准文档模板
│   ├── construction/    # 施工方案模板
│   ├── safety/          # 安全交底模板
│   ├── quality/         # 质量验收模板
│   ├── contract/        # 施工合同模板
│   └── report/          # 监理报告模板
├── skills/              # Codex Skill 定义
│   ├── construction-doc-gen/
│   ├── safety-inspection/
│   └── quality-audit/
├── scripts/             # 自动化脚本
│   ├── md-to-docx.py    # Markdown → Word 转换
│   └── generate-sample.py
├── actions/             # GitHub Actions 配置
├── examples/            # 示例项目文档
├── plugin.json          # 插件清单
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install python-docx markdown jinja2
```

### 2. 生成文档

```bash
# 从模板生成施工方案
python scripts/generate-sample.py \
  --template templates/construction/construction-plan.md \
  --output examples/project-a/construction-plan.md \
  --project "我的工程项目"

# 转换为 Word
python scripts/md-to-docx.py \
  --input examples/project-a/construction-plan.md \
  --output examples/project-a/construction-plan.docx
```

### 3. 使用 Codex Skill

在 Codex 中直接调用：

```
> 生成施工方案
> 文档类型：construction-plan
> 项目名称：XX大厦
> 地点：北京市朝阳区
```

Codex 会自动加载对应模板，填充数据，并输出标准化文档。

## 支持的文档类型

| 文档类型 | 模板路径 | 适用标准 |
|----------|----------|----------|
| 施工方案 | `templates/construction/construction-plan.md` | GB 50300-2013 |
| 安全交底 | `templates/safety/safety-disclosure.md` | JGJ 59-2011 |
| 质量验收 | `templates/quality/quality-inspection.md` | GB 50204-2015 |
| 施工合同 | `templates/contract/construction-contract.md` | GF-2017-0201 |
| 监理月报 | `templates/report/supervision-monthly.md` | GB/T 50319 |

## GitHub Actions

推送模板或脚本变更时自动触发验证：

```yaml
name: Build Construction Documents
on:
  push:
    paths: ['templates/**', 'scripts/**']
  workflow_dispatch:
```

手动触发生成示例文档：

```bash
gh workflow run build-docs.yml \
  -f project_name="我的项目"
```

## 技术栈

- **模板引擎**: Jinja2 (可选) / 原生 Markdown 占位符
- **文档转换**: python-docx
- **CI/CD**: GitHub Actions
- **AI 集成**: Codex CLI + Skill 系统

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

*Built with ❤️ for the Chinese construction industry*
