---
name: academic-pdf-translator
description: Translate academic PDF papers into Chinese while preserving the original PDF layout using PDFMathTranslate-next/BabelDOC or classic pdf2zh. Use for single PDFs, folders of PDFs, page-range trial translations, bilingual/monolingual output, and terminology-aware translation in biomedical, bioinformatics, AI, large-language-model, RAG, agent, and knowledge-graph literature.
---

# Academic PDF Translator

Use this skill when the user wants layout-preserving PDF translation, especially for academic papers. Prefer `pdf2zh_next` because it uses the newer BabelDOC pipeline; fall back to classic `pdf2zh` only if the next-generation command is unavailable or fails.

## Core Workflow

1. Identify whether the user gave a single PDF, a folder, or a keyword that should be resolved to PDFs.
2. If the user has not chosen an output location, use a nearby folder named `中文翻译版`.
3. Ask for explicit permission before installing translation software. Do not install dependencies silently.
4. Before translating, run the helper doctor:
   ```bash
   python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py doctor
   ```
5. If `pdf2zh_next` is installed, use the helper with `--backend next`. If only `pdf2zh` is installed, use `--backend classic`; the helper passes `--babeldoc` by default so classic `pdf2zh` still uses the newer BabelDOC backend when available.
6. For DeepSeek, support two API-key modes:
   - Simple chat mode: if the user prefers convenience and explicitly accepts entering the key in chat, ask them to paste the key in the conversation, then use it only for the current translation run. Do not save it to disk.
   - Safer hidden-input mode: if the user prefers privacy, run the helper with `--ask-key` in an interactive TTY so the key is hidden.
   Never write API keys into skill files, prompts, glossaries, logs, generated PDFs, or persistent config.
7. For a new paper type or unclear quality, first run a page trial such as `--pages 1-3`. Render or open the result before running the full PDF/folder.
8. After translation, verify that output PDFs exist, page counts are plausible, and a rendered page has no severe text overlap, blank pages, or broken glyphs.

## Helper Script

Use `scripts/translate_academic_pdf.py` instead of hand-writing long `pdf2zh` commands. It bundles the default prompt and glossary automatically.

Common commands:

```bash
# Check installation and show install guidance.
python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py doctor

# Translate one PDF with DeepSeek. If no key is set, prompt for hidden input.
python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py translate paper.pdf --output ./中文翻译版 --ask-key

# Trial translate pages 1-3.
python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py translate paper.pdf --pages 1-3 --output ./中文翻译版 --ask-key

# Translate every PDF in a folder.
python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py translate ./英文PDF文件夹 --output ./中文翻译版 --ask-key

# Use OpenAI instead of DeepSeek when the user requests it.
python ~/.codex/skills/academic-pdf-translator/scripts/translate_academic_pdf.py translate paper.pdf --service openai --ask-key
```

The helper does not install anything. If it reports missing tools, ask the user whether to install `uv`/`pdf2zh-next` before proceeding.

## Installation Guidance

Recommend this route on macOS:

```bash
# Install uv if needed.
python3 -m pip install --user uv

# Install the newer PDFMathTranslate-next CLI.
uv tool install --python 3.12 pdf2zh-next

# Confirm.
pdf2zh_next --help
```

If `uv` is unavailable or unsuitable, use a project-local virtual environment and install `pdf2zh` there. Avoid Docker unless the user explicitly wants it; Docker consumes much more disk space.

## API Key Handling

For the simplest user experience, Codex may ask the user to paste the DeepSeek API key in chat after clearly warning that chat entry is less private than hidden terminal input. Use that key only in memory for the current translation command and never save it.

For the safer mode, use `--ask-key`. The script calls `getpass` so the key is hidden in the terminal and used only for the current process. When Codex runs this helper and no environment key is available, start the command in an interactive TTY and tell the user to paste the key into the terminal prompt.

If using chat mode, avoid printing the full shell command with the key. Prefer setting the key in the subprocess environment from Codex runtime state rather than embedding it in command-line arguments.

If the user later wants convenience, they may set an environment variable:

```bash
export DEEPSEEK_API_KEY="..."
export DEEPSEEK_MODEL="deepseek-chat"
```

Do not ask the user to paste an API key into normal chat unless they explicitly accept that risk.

## Output Expectations

The BabelDOC backend usually creates monolingual and bilingual translated PDFs in the output directory. Preserve both unless the user requests only one:

- monolingual Chinese PDF for reading
- bilingual PDF for checking against the original

If the output filenames are not ideal, rename copies after generation rather than modifying the translated PDF contents.

## Customization

The default resources are:

- `references/biomed_academic_prompt.txt`: system prompt for academic Chinese translation.
- `references/glossary_biomed_ai_kg.csv`: glossary covering biomedical, bioinformatics, AI, LLM, RAG, agent, and knowledge graph terminology.

When the user requests a terminology change, update the glossary first. If the request is about style, update the prompt.
