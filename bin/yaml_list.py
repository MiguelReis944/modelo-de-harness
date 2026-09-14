#!/usr/bin/env python3
"""Extrai uma lista YAML simples (chave top-level -> itens escalares) sem depender de
PyYAML. Cobre a gramática restrita usada em harness.config.yaml: itens simples ou entre
aspas (simples/duplas), com '#' dentro de aspas não tratado como comentário.
Uso: yaml_list.py <key> <file>"""
import sys

# python nativo do Windows traduz \n -> \r\n no stdout por padrao; isso corromperia a
# leitura por `for s in $(...)` no bash (o \r gruda no ultimo item da linha).
sys.stdout.reconfigure(encoding="utf-8", newline="\n")


def strip_comment(line):
    out = []
    quote = None
    for c in line:
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in ("'", '"'):
            quote = c
            out.append(c)
        elif c == "#":
            break
        else:
            out.append(c)
    return "".join(out)


def unquote(item):
    item = item.strip()
    if len(item) >= 2 and item[0] == item[-1] and item[0] in ("'", '"'):
        return item[1:-1]
    return item


def main():
    key, path = sys.argv[1], sys.argv[2]
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    in_section = False
    for raw in lines:
        stripped = strip_comment(raw.rstrip("\n")).rstrip()
        if not in_section:
            if stripped == f"{key}:":
                in_section = True
            continue
        if not stripped.strip():
            continue
        if stripped[0] in (" ", "\t") and stripped.strip().startswith("- "):
            print(unquote(stripped.strip()[2:]))
        elif stripped[0] not in (" ", "\t"):
            break


if __name__ == "__main__":
    main()
