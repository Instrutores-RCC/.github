"""Cria os times da organização, liga cada time aos repositórios e põe os tópicos.

Uso:
    python scripts/aplica_org.py            # mostra o que faria
    python scripts/aplica_org.py --aplicar  # faz

Idempotente: time que já existe não é recriado. Precisa do gh com escopo admin:org
(gh auth refresh -h github.com -s admin:org).
Não adiciona pessoas: membros entram pela página do time ou por convite.
"""
import argparse
import json
import subprocess
import sys

ORG = "Instrutores-RCC"

# (slug, pai, descrição)
TIMES = [
    ("instrutores", None, "Cargos do Departamento de Instrutores"),
    ("lideranca", "instrutores", "Líder e Vice-líder dos Instrutores"),
    ("ministerio", "instrutores", "Ministros dos Instrutores"),
    ("capacitadores", "instrutores", "Capacitadores dos Instrutores"),
    ("avaliadores", "instrutores", "Avaliadores dos Instrutores"),
    ("estagiarios", "instrutores", "Estagiários dos Instrutores"),
    ("setores", None, "Subgrupos dos Instrutores"),
    ("setor-src", "setores", "SRC, Setor de Relações Comunicativas"),
    ("setor-ssi", "setores", "SSI, Setor de Segurança dos Instrutores"),
    ("setor-da", "setores", "DA, Departamento de Aplicação"),
    ("desenvolvimento", None, "Departamento de Desenvolvimento [DEV]"),
    ("lider-dev", "desenvolvimento", "Líder de Desenvolvimento: arquitetura, segurança, repositórios"),
    ("revisores", "desenvolvimento", "Revisores: aprovam PR"),
    ("desenvolvedores", "desenvolvimento", "Desenvolvedores: specs e PRs"),
    ("designers", "desenvolvimento", "Designers: assets, DESIGN.md, protótipos"),
    ("estagiarios-dev", "desenvolvimento", "Estagiários de Desenvolvimento"),
]

# permissão de cada time em TODO repositório
PERM_GERAL = {
    "instrutores": "pull",
    "lideranca": "triage",
    "lider-dev": "admin",
    "revisores": "maintain",
    "desenvolvedores": "push",
    "designers": "push",
    "estagiarios-dev": "triage",
}

# tópicos por repositório; tópico setor-<x> dá triage ao time setor-<x>
TOPICOS = {
    "central-do-src": ["rcc", "instrutores", "setor-src", "apps-script", "forum", "html"],
    "quadro-advertencias-src": ["rcc", "instrutores", "setor-src", "apps-script", "forum"],
    "ouvidoria-ins": ["rcc", "instrutores", "ouvidoria", "forum", "html"],
    ".github": ["rcc", "instrutores"],
    "modelo-projeto": ["rcc", "instrutores", "modelo"],
}


def gh(*args, ok404=False):
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        if ok404 and "404" in r.stderr:
            return None
        raise RuntimeError(f"gh api {' '.join(args)}: {r.stderr.strip()}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    a = p.parse_args()
    faz = a.aplicar

    existentes = {t["slug"]: t["id"] for t in gh(f"orgs/{ORG}/teams?per_page=100")}
    for slug, pai, desc in TIMES:
        if slug in existentes:
            print(f"time {slug}: já existe, pulando")
            continue
        print(f"time {slug}: cria (pai {pai or '-'})")
        if faz:
            campos = ["-f", f"name={slug}", "-f", f"description={desc}", "-f", "privacy=closed"]
            if pai:
                campos += ["-F", f"parent_team_id={existentes[pai]}"]
            existentes[slug] = gh("-X", "POST", f"orgs/{ORG}/teams", *campos)["id"]

    repos = [r["name"] for r in gh(f"orgs/{ORG}/repos?per_page=100") if not r["archived"]]
    for repo in repos:
        topicos = TOPICOS.get(repo, ["rcc", "instrutores"])
        print(f"{repo}: tópicos {topicos}")
        if faz:
            gh("-X", "PUT", f"repos/{ORG}/{repo}/topics", *sum((["-f", f"names[]={t}"] for t in topicos), []))
        perms = dict(PERM_GERAL)
        for t in topicos:
            if t.startswith("setor-"):
                perms[t] = "triage"
        for slug, perm in perms.items():
            print(f"  {slug}: {perm}")
            if faz:
                gh("-X", "PUT", f"orgs/{ORG}/teams/{slug}/repos/{ORG}/{repo}", "-f", f"permission={perm}")

    if not faz:
        print("\n(simulação; rode com --aplicar)")


if __name__ == "__main__":
    sys.exit(main())
