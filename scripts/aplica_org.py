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
    ("aprendizes-dev", "desenvolvimento", "Aprendizes de Desenvolvimento"),
]

# permissão de cada time em TODO repositório
PERM_GERAL = {
    "instrutores": "pull",
    "lideranca": "triage",
    "lider-dev": "admin",
    "revisores": "maintain",
    "desenvolvedores": "push",
    "designers": "push",
    "aprendizes-dev": "triage",
}

# tópicos por repositório; tópico setor-<x> dá triage ao time setor-<x>
TOPICOS = {
    "central-do-src": ["rcc", "instrutores", "setor-src", "apps-script", "forum", "html"],
    "quadro-advertencias-src": ["rcc", "instrutores", "setor-src", "apps-script", "forum"],
    "ouvidoria-ins": ["rcc", "instrutores", "ouvidoria", "forum", "html"],
    ".github": ["rcc", "instrutores"],
    "modelo-projeto": ["rcc", "instrutores", "modelo"],
}


def gh(*args, ok404=False, corpo=None):
    if corpo is not None:
        args = (*args, "--input", "-")
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True, encoding="utf-8",
                       input=json.dumps(corpo) if corpo is not None else None)
    if r.returncode != 0:
        if ok404 and "404" in r.stderr:
            return None
        raise RuntimeError(f"gh api {' '.join(args)}: {r.stderr.strip()}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def protecao(repo):
    """Regra da main (docs/APROVACAO-PR.md). Admin (lider-dev) pode furar em emergência."""
    check = "valida" if repo == ".github" else "padrao / segredos"
    return {
        "required_status_checks": {"strict": False, "contexts": [check]},
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "require_code_owner_reviews": True,
            "dismiss_stale_reviews": True,
        },
        "restrictions": None,
        "required_conversation_resolution": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }


def protege(repo, faz):
    print("  main protegida: PR, 1 aprovação do CODEOWNERS, check verde, sem force push")
    if not faz:
        return
    try:
        gh("-X", "PUT", f"repos/{ORG}/{repo}/branches/main/protection", corpo=protecao(repo))
    except RuntimeError as e:
        if "Upgrade to GitHub Pro" in str(e) or "403" in str(e):
            print("  AVISO: plano free não protege repositório privado; a regra vale só por CODEOWNERS e pela ação push-direto")
        elif "Branch not found" in str(e) or "404" in str(e):
            print("  AVISO: repositório sem main ainda, pulando")
        else:
            raise


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
        print("  merge: só squash, apaga branch depois")
        if faz:
            gh("-X", "PATCH", f"repos/{ORG}/{repo}", "-F", "allow_squash_merge=true",
               "-F", "allow_merge_commit=false", "-F", "allow_rebase_merge=false",
               "-F", "delete_branch_on_merge=true")
        protege(repo, faz)

    if not faz:
        print("\n(simulação; rode com --aplicar)")


if __name__ == "__main__":
    sys.exit(main())
