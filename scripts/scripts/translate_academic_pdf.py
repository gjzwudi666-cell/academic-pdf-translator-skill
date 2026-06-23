#!/usr/bin/env python3
"""Wrapper for layout-preserving academic PDF translation with pdf2zh tools."""

from __future__ import annotations

import argparse
import getpass
import os
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PROMPT = SKILL_DIR / "references" / "biomed_academic_prompt.txt"
DEFAULT_GLOSSARY = SKILL_DIR / "references" / "glossary_biomed_ai_kg.csv"


def which(name: str) -> str | None:
    return shutil.which(name)


def collect_pdfs(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() != ".pdf":
            raise SystemExit(f"Input is not a PDF: {path}")
        return [path]
    if path.is_dir():
        pdfs = sorted(path.glob("*.pdf"))
        if not pdfs:
            raise SystemExit(f"No PDF files found in folder: {path}")
        return pdfs
    raise SystemExit(f"Input path does not exist: {path}")


def require_key(service: str, ask_key: bool) -> dict[str, str]:
    env_updates: dict[str, str] = {}
    service = service.lower()
    key_env = {
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "openai-compatible": "OPENAI_API_KEY",
    }.get(service)
    if not key_env:
        return env_updates
    key = os.environ.get(key_env, "").strip()
    if not key and ask_key:
        if not sys.stdin.isatty():
            raise SystemExit(
                f"Cannot securely prompt for {key_env} without an interactive terminal. "
                "Run from a TTY, or set the environment variable for this command."
            )
        key = getpass.getpass(f"Enter {key_env} for this translation run: ").strip()
    if not key:
        raise SystemExit(
            f"Missing {key_env}. Re-run with --ask-key, or set {key_env} in the environment."
        )
    env_updates[key_env] = key
    if service == "deepseek":
        env_updates["PDF2ZH_DEEPSEEK_API_KEY"] = key
        env_updates.setdefault("DEEPSEEK_MODEL", os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"))
        env_updates.setdefault("PDF2ZH_DEEPSEEK_MODEL", os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"))
    if service in {"openai", "openai-compatible"}:
        env_updates["PDF2ZH_OPENAI_API_KEY"] = key
        if os.environ.get("OPENAI_BASE_URL"):
            env_updates["PDF2ZH_OPENAI_BASE_URL"] = os.environ["OPENAI_BASE_URL"]
        if os.environ.get("OPENAI_MODEL"):
            env_updates["PDF2ZH_OPENAI_MODEL"] = os.environ["OPENAI_MODEL"]
    return env_updates


def service_arg_next(service: str) -> str:
    mapping = {
        "deepseek": "--deepseek",
        "openai": "--openai",
        "openai-compatible": "--openai-compatible",
        "siliconflow": "--siliconflow",
    }
    try:
        return mapping[service.lower()]
    except KeyError as exc:
        raise SystemExit(f"Unsupported next backend service: {service}") from exc


def command_next(pdf: Path, args: argparse.Namespace) -> list[str]:
    cmd = [
        "pdf2zh_next",
        str(pdf),
        "--output",
        str(args.output),
        service_arg_next(args.service),
        "--lang-in",
        args.lang_in,
        "--lang-out",
        args.lang_out,
        "--custom-system-prompt",
        Path(args.prompt).read_text(encoding="utf-8"),
        "--glossaries",
        str(args.glossary),
        "--watermark-output-mode",
        "no_watermark",
        "--qps",
        str(args.qps),
        "--pool-max-workers",
        str(args.pool_max_workers),
        "--report-interval",
        "5",
    ]
    if args.pages:
        cmd += ["--pages", args.pages]
    if args.no_dual:
        cmd.append("--no-dual")
    if args.no_mono:
        cmd.append("--no-mono")
    if args.enhance_compatibility:
        cmd.append("--enhance-compatibility")
    if args.only_include_translated_page and args.pages:
        cmd.append("--only-include-translated-page")
    return cmd


def command_classic(pdf: Path, args: argparse.Namespace) -> list[str]:
    service = args.service.lower()
    classic_service = "deepseek" if service == "deepseek" else service
    cmd = [
        "pdf2zh",
        str(pdf),
        "-o",
        str(args.output),
        "-li",
        args.lang_in,
        "-lo",
        args.lang_out.split("-")[0],
        "-s",
        classic_service,
        "-t",
        str(args.threads),
        "--prompt",
        str(args.prompt),
    ]
    if args.pages:
        cmd += ["-p", args.pages]
    if args.babeldoc:
        cmd.append("--babeldoc")
    if args.enhance_compatibility:
        cmd.append("--compatible")
    return cmd


def run_command(cmd: list[str], env_updates: dict[str, str], dry_run: bool) -> int:
    printable = " ".join(f'"{x}"' if " " in x else x for x in cmd)
    print(f"\n[command] {printable}\n", flush=True)
    if dry_run:
        return 0
    env = os.environ.copy()
    env.update(env_updates)
    return subprocess.call(cmd, env=env)


def doctor(_: argparse.Namespace) -> None:
    print("Academic PDF Translator doctor\n")
    print(f"pdf2zh_next: {which('pdf2zh_next') or 'not found'}")
    print(f"pdf2zh:      {which('pdf2zh') or 'not found'}")
    print(f"prompt:      {DEFAULT_PROMPT}")
    print(f"glossary:    {DEFAULT_GLOSSARY}")
    print("\nRecommended install on macOS:")
    print("  python3 -m pip install --user uv")
    print("  uv tool install --python 3.12 pdf2zh")
    print("  pdf2zh --help")
    print("\nNote: pdf2zh 1.9.x uses the newer BabelDOC backend via --babeldoc.")


def translate_cmd(args: argparse.Namespace) -> None:
    input_path = Path(args.input).expanduser().resolve()
    args.output = Path(args.output).expanduser().resolve() if args.output else input_path.parent / "中文翻译版"
    args.output.mkdir(parents=True, exist_ok=True)
    args.prompt = Path(args.prompt).expanduser().resolve()
    args.glossary = Path(args.glossary).expanduser().resolve()
    if not args.prompt.exists():
        raise SystemExit(f"Prompt file not found: {args.prompt}")
    if not args.glossary.exists():
        raise SystemExit(f"Glossary file not found: {args.glossary}")

    backend = args.backend
    if backend == "auto":
        backend = "next" if which("pdf2zh_next") else "classic" if which("pdf2zh") else "missing"
    if backend == "next" and not which("pdf2zh_next"):
        raise SystemExit("pdf2zh_next not found. Run doctor for install guidance.")
    if backend == "classic" and not which("pdf2zh"):
        raise SystemExit("pdf2zh not found. Run doctor for install guidance.")
    if backend == "missing":
        raise SystemExit("Neither pdf2zh_next nor pdf2zh was found. Run doctor for install guidance.")

    env_updates = require_key(args.service, args.ask_key)
    pdfs = collect_pdfs(input_path)
    failures = []
    for index, pdf in enumerate(pdfs, start=1):
        print(f"[{index}/{len(pdfs)}] Translating {pdf.name} with backend={backend}, service={args.service}")
        cmd = command_next(pdf, args) if backend == "next" else command_classic(pdf, args)
        code = run_command(cmd, env_updates, args.dry_run)
        if code != 0:
            failures.append((pdf, code))
            if args.stop_on_error:
                break
    if failures:
        print("\nFailures:")
        for pdf, code in failures:
            print(f"  {pdf}: exit {code}")
        raise SystemExit(1)
    print(f"\nDone. Check output folder: {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate academic PDFs with pdf2zh_next/pdf2zh.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_doc = sub.add_parser("doctor", help="Check tools and show install guidance.")
    p_doc.set_defaults(func=doctor)

    p = sub.add_parser("translate", help="Translate one PDF or a folder of PDFs.")
    p.add_argument("input", help="PDF file or folder containing PDF files.")
    p.add_argument("--output", help="Output folder. Default: input folder/中文翻译版.")
    p.add_argument("--backend", choices=["auto", "next", "classic"], default="auto")
    p.add_argument("--service", default="deepseek", help="deepseek, openai, openai-compatible, siliconflow.")
    p.add_argument("--ask-key", action="store_true", help="Prompt for API key if the env var is missing.")
    p.add_argument("--pages", help="Page range for trial translation, e.g. 1-3 or 1,3,10-20.")
    p.add_argument("--lang-in", default="en")
    p.add_argument("--lang-out", default="zh-CN")
    p.add_argument("--prompt", default=str(DEFAULT_PROMPT))
    p.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    p.add_argument("--qps", type=float, default=1.0, help="Conservative request rate for LLM services.")
    p.add_argument("--pool-max-workers", type=int, default=2)
    p.add_argument("--threads", type=int, default=2, help="Classic pdf2zh thread count.")
    p.add_argument("--no-dual", action="store_true")
    p.add_argument("--no-mono", action="store_true")
    p.add_argument("--babeldoc", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--only-include-translated-page", action="store_true")
    p.add_argument("--enhance-compatibility", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--stop-on-error", action="store_true")
    p.set_defaults(func=translate_cmd)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
