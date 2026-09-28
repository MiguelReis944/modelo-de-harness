#!/usr/bin/env python3
"""Create and inspect the canonical documents in harness projects."""

import argparse
import os
import shutil
import stat
from pathlib import Path


DOCS = ("prd.md", "architecture.md", "rules.md", "design.md", "tasks.md", "memory.md")
MARKER = "<!-- project-docs-routing -->"
POINTER = """<!-- project-docs-routing -->
## Documentação do projeto

Leia sempre `docs/rules.md` e `docs/memory.md` antes de trabalhar neste projeto.
Leia `docs/prd.md` para escopo e requisitos; `docs/architecture.md` para código, dados, APIs e implantação; `docs/design.md` para interface, experiência de uso e fluxos de CLI; e `docs/tasks.md` para backlog e planejamento.
"""


def reject_reparse_points(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    for component in reversed((absolute, *absolute.parents)):
        try:
            details = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(details.st_mode) or (
            getattr(details, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        ):
            raise ValueError(
                f"caminho atravessa link simbólico ou ponto de nova análise: {component}; "
                "use diretórios e arquivos reais"
            )


def init(project: Path) -> None:
    reject_reparse_points(project)
    if not project.is_dir():
        raise ValueError(f"diretório de projeto ausente: {project}")

    templates = Path(__file__).resolve().parent.parent / "templates" / "project-docs"
    docs = project / "docs"
    reject_reparse_points(docs)
    if docs.exists() and not docs.is_dir():
        raise ValueError(f"docs/ não é diretório: {docs}")
    for filename in DOCS:
        destination = docs / filename
        reject_reparse_points(destination)
        if destination.exists() and not destination.is_file():
            raise ValueError(f"documento não é arquivo regular: {destination}")

    agents = project / "AGENTS.md"
    reject_reparse_points(agents)
    if agents.exists() and not agents.is_file():
        raise ValueError(f"AGENTS.md não é arquivo regular: {agents}")

    docs.mkdir(exist_ok=True)
    for filename in DOCS:
        source = templates / filename
        destination = docs / filename
        if destination.exists():
            print(f"preservado: {destination}")
        else:
            with source.open("rb") as input_file, destination.open("xb") as output_file:
                shutil.copyfileobj(input_file, output_file)
            print(f"criado: {destination}")

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
        with agents.open("x", encoding="utf-8") as output:
            output.write("# Instruções do projeto\n\n" + POINTER)
        print(f"criado: {agents}")


def check(workspace: Path) -> int:
    if not workspace.exists() and not workspace.is_symlink():
        print("documentação dos projetos: completa (workspace ausente)")
        return 0
    if not workspace.is_dir():
        raise ValueError(f"workspace não é diretório: {workspace}")

    missing_any = False
    for project in sorted((entry for entry in workspace.iterdir() if entry.is_dir() and not entry.is_symlink()), key=lambda p: p.name.casefold()):
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
