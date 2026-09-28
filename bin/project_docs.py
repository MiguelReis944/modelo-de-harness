#!/usr/bin/env python3
"""Create and inspect the canonical documents in harness projects."""

import argparse
import shutil
from pathlib import Path


DOCS = ("prd.md", "architecture.md", "rules.md", "design.md", "tasks.md", "memory.md")
MARKER = "<!-- project-docs-routing -->"
POINTER = """<!-- project-docs-routing -->
## Documentação do projeto

Leia sempre `docs/rules.md` e `docs/memory.md` antes de trabalhar neste projeto.
Leia `docs/prd.md` para escopo e requisitos; `docs/architecture.md` para código, dados, APIs e implantação; `docs/design.md` para interface, experiência de uso e fluxos de CLI; e `docs/tasks.md` para backlog e planejamento.
"""


def init(project: Path) -> None:
    if not project.is_dir():
        raise ValueError(f"diretório de projeto ausente: {project}")

    templates = Path(__file__).resolve().parent.parent / "templates" / "project-docs"
    docs = project / "docs"
    docs.mkdir(exist_ok=True)
    for filename in DOCS:
        source = templates / filename
        destination = docs / filename
        if destination.exists():
            print(f"preservado: {destination}")
        else:
            shutil.copyfile(source, destination)
            print(f"criado: {destination}")

    agents = project / "AGENTS.md"
    if agents.exists():
        existing = agents.read_text(encoding="utf-8")
        if MARKER in existing:
            print(f"preservado: {agents}")
        else:
            separator = "" if not existing else "\n" if existing.endswith("\n") else "\n\n"
            with agents.open("a", encoding="utf-8") as output:
                output.write(separator + POINTER)
            print(f"atualizado: {agents} (ponteiro criado)")
    else:
        agents.write_text("# Instruções do projeto\n\n" + POINTER, encoding="utf-8")
        print(f"criado: {agents}")


def check(workspace: Path) -> int:
    if not workspace.is_dir():
        raise ValueError(f"diretório de workspace ausente: {workspace}")

    missing_any = False
    for project in sorted((entry for entry in workspace.iterdir() if entry.is_dir()), key=lambda p: p.name.casefold()):
        missing = [name for name in DOCS if not (project / "docs" / name).is_file()]
        if missing:
            print(f"{project.name}: faltam {', '.join('docs/' + name for name in missing)}")
            missing_any = True
    if not missing_any:
        print("documentação dos projetos: completa")
    return int(missing_any)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="cria apenas documentos ausentes").add_argument("project_path", type=Path)
    subcommands.add_parser("check", help="lista documentos ausentes por projeto").add_argument("workspace_path", type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.command == "init":
            init(arguments.project_path)
            return 0
        return check(arguments.workspace_path)
    except (OSError, ValueError) as error:
        parser.exit(2, f"project_docs: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
