# Academic PDF Translator Skill

面向中文读者的 Codex 文献 PDF 翻译 skill，用于把英文论文翻译成学术化、专业化的中文，并尽量保留原 PDF 的排版格式。

这个 skill 主要适合以下方向的文献阅读：

- 生物医学
- 生物信息学
- 自然语言处理
- 人工智能
- 大语言模型
- RAG
- Agent
- 知识图谱

## 这个 Skill 能做什么

- 翻译单篇 PDF 论文。
- 翻译一个文件夹里的多篇 PDF。
- 支持先试译前 1-3 页，确认版式和术语质量后再全文翻译。
- 使用 PDFMathTranslate-next / BabelDOC 尽量保留原论文版式。
- 支持 DeepSeek、OpenAI 和 OpenAI-compatible API。
- 内置生物医学、生物信息学、AI、LLM、RAG、Agent、知识图谱相关术语表。

## 最简单的安装方式

如果你不熟悉终端和命令行，可以直接在 Codex 里说：

```text
请帮我安装这个 skill：
https://github.com/gjzwudi666-cell/academic-pdf-translator-skill
```

Codex 通常会自动把这个 GitHub 仓库安装到你的 `~/.codex/skills/` 文件夹里。安装完成后，重启 Codex，或者新开一个 Codex 会话，就可以使用这个 skill。

## 手动安装方式

如果你熟悉命令行，也可以这样安装：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/gjzwudi666-cell/academic-pdf-translator-skill.git ~/.codex/skills/academic-pdf-translator
```

然后重启 Codex，或者新开一个 Codex 会话。

## 还需要安装 pdf2zh-next 吗？

需要。

这个 GitHub 仓库只是 Codex skill，本身不包含大型 PDF 翻译程序。第一次正式翻译前，Codex 会检查你的电脑是否已经安装 `pdf2zh_next`。如果没有安装，你可以让 Codex 帮你安装。

推荐你在 Codex 里说：

```text
请使用 academic-pdf-translator skill，帮我安装 pdf2zh-next，然后先用一篇 PDF 的前 1-3 页做试译。
```

如果手动安装，macOS 推荐路线是：

```bash
python3 -m pip install --user uv
uv tool install --python 3.12 pdf2zh-next
```

安装后可以用下面命令检查：

```bash
pdf2zh_next --help
```

## API Key 怎么处理？

这个仓库不包含任何 API key。

每个使用者都需要准备自己的 DeepSeek、OpenAI 或 OpenAI-compatible API key。使用 skill 翻译时，Codex 可以先提醒你输入 API key，然后只在本次翻译过程中临时使用。

适合电脑小白的使用方式是直接对 Codex 说：

```text
请使用 academic-pdf-translator skill 翻译这篇 PDF。使用 DeepSeek，并在需要 API key 时让我直接在聊天框里输入。
```

注意：把 API key 输入到聊天框比终端隐藏输入更方便，但隐私性略弱。请不要把 API key 上传到 GitHub，也不要写进 README、脚本或配置文件。

## 典型使用提示词

单篇论文试译：

```text
请使用 academic-pdf-translator skill，把这篇英文论文翻译成学术化中文 PDF，尽量保留原 PDF 排版。使用 DeepSeek，先翻译第 1-3 页让我检查版式和术语质量。
```

文件夹批量翻译：

```text
请使用 academic-pdf-translator skill，把这个文件夹里的英文 PDF 文献全部翻译成中文 PDF，输出到一个名为“中文翻译版”的文件夹中。使用 DeepSeek，并在需要时提醒我输入 API key。
```

## 重要说明

PDF 版式保留翻译不是 100% 完美的。复杂双栏论文、表格、公式、参考文献和密集标题附近，偶尔可能出现局部文字拥挤或轻微重叠。因此建议先做 1-3 页试译，确认效果后再全文翻译或批量翻译。

如果后续需要适配新的文献领域，可以继续更新提示词和术语表。
