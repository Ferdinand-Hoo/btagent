---
name: auto-commit
description: Generates a git commit from the user's staged changes and writes a standardized commit message (Conventional Commits). Use when the user wants to create a commit from staged files, normalize commit message format, or asks to commit staged changes or write a commit message from staging area.
---

# 根据暂存区生成规范提交

根据当前暂存区（staged changes）生成一次提交，并写出符合规范的提交信息。

## 执行流程

1. **查看暂存区**
   - 运行 `git status` 确认有已暂存文件
   - 运行 `git diff --staged` 查看具体改动内容
   - 若无暂存内容，提示用户先 `git add` 再继续

2. **生成提交信息**
   - 根据 diff 内容判断变更类型与影响范围
   - 按下方「提交信息格式」写出标题与可选正文

3. **执行提交**
   - **默认行为**：只输出推荐的提交信息（标题 + 正文），**不主动执行 `git commit`**
   - **仅当用户明确要求**「帮我提交 / 直接提交」时，才执行：`git commit -m "标题" -m "正文"`（正文可选）

## 提交信息格式（Conventional Commits）

**标题（必填）**：`<type>(<scope>): <short description>`

- **type**（必填）：`feat`（新功能）、`fix`（修复）、`docs`（文档）、`style`（格式/风格）、`refactor`（重构）、`test`（测试）、`chore`（构建/工具等）
- **scope**（可选）：影响范围，如模块名、文件名，如 `auth`、`parsers`
- **short description**：一句话说明，祈使句、现在时，首字母小写，结尾不加句号

**正文（可选）**：说明动机、与上一版的差异、破坏性变更等。

**示例：**

```
feat(parsers): add HCI ACL packet parser

Parse ACL data packets from btsnoop with handle and flags.
```

```
fix(btsnoop): correct timestamp direction for incoming packets
```

```
docs: update architecture and parser-files documentation
```

```
refactor(hci): extract constants to constants module
```

## 类型选择参考

| 变更内容           | type    |
|--------------------|---------|
| 新功能、新模块     | feat    |
| Bug 修复           | fix     |
| 仅文档/注释        | docs    |
| 代码格式、空格等   | style   |
| 重构、无行为变化   | refactor|
| 测试相关           | test    |
| 构建、依赖、脚本等 | chore   |

## 注意事项

- 标题控制在约 50 字符内，正文每行约 72 字符换行
- 从 diff 推断 type/scope，不臆造；若难以判断 scope 可省略
- 若用户明确要求「只生成信息不提交」，则只输出 message，不执行 `git commit`
- **标题语言要求**：`<short description>` 一律使用 **英文**（祈使句、现在时）
- **正文语言要求**：正文一律使用 **中文** 描述变更内容与动机
- **正文结构要求**：正文采用 **分点列举** 的形式，每个要点单独一行，以 `- ` 开头，突出不同类型的改动（例如解析逻辑、时间戳处理、文档更新等）
