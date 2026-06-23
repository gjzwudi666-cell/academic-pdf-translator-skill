# Academic PDF Translator Skill

A Codex skill for translating academic PDF papers into Chinese while preserving the original PDF layout.

It is designed for biomedical science, bioinformatics, artificial intelligence, large language models, retrieval-augmented generation, agents, and knowledge graph literature.

## What It Does

- Translates single PDF papers or folders of PDFs.
- Preserves the original PDF layout with PDFMathTranslate-next / BabelDOC.
- Supports DeepSeek, OpenAI, and OpenAI-compatible translation services.
- Includes a biomedical, bioinformatics, AI, LLM, RAG, agent, and knowledge graph glossary.
- Supports trial translation by page range, such as pages 1-3.

## Install This Skill

Clone or download this repository into your Codex skills folder:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/YOUR_USERNAME/academic-pdf-translator-skill.git ~/.codex/skills/academic-pdf-translator
```

Then restart Codex or open a new Codex conversation.

## Install The PDF Translator Backend

This skill expects `pdf2zh_next` to be available. On macOS, the recommended installation route is:

```bash
python3 -m pip install --user uv
uv tool install --python 3.12 pdf2zh-next
```

Confirm installation:

```bash
pdf2zh_next --help
```

## API Keys

This repository does not include any API key.

Each user should provide their own DeepSeek, OpenAI, or OpenAI-compatible API key at runtime. Do not commit API keys into this repository.

## Typical Codex Prompt

```text
Please use the academic-pdf-translator skill to translate this PDF into academic Chinese while preserving the original PDF layout. Use DeepSeek, ask me for the API key in chat, and first run a pages 1-3 trial translation.
```

## Notes

PDF layout-preserving translation is not perfect. Complex two-column academic papers may still have occasional local text crowding or overlap, especially around dense headings, tables, formulas, and references. Always review a trial translation before translating a full folder.
