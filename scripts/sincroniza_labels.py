"""Aplica labels.json em todos os repositórios da organização.

Uso:
    python scripts/sincroniza_labels.py            # mostra o que faria
    python scripts/sincroniza_labels.py --aplicar  # faz
    python scripts/sincroniza_labels.py --aplicar --repo central-do-src

Cria ou atualiza as labels da lista. Para cada label antiga em "migrar", põe as
novas nas issues e PRs que tinham a antiga e só então apaga a antiga.
Precisa do gh logado com acesso de escrita aos repositórios.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ORG = "Instrutores-RCC"
RAIZ = Path(__file__).resolve().parent.parent


def gh(*args, capturar=True):
    r = subprocess.run(["gh", *args], capture_output=capturar, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def repos():
    saida = gh("repo", "list", ORG, "--limit", "200", "--no-archived", "--json", "name", "--jq", ".[].name")
    return [n for n in saida.split() if n]


def labels_atuais(repo):
    saida = gh("label", "list", "-R", f"{ORG}/{repo}", "--limit", "200", "--json", "name", "--jq", ".[].name")
    return set(l for l in saida.splitlines() if l)


def itens_com_label(repo, label):
    # Issues e PRs do repositório com o label. O endpoint de issues devolve os dois e usa o limite
    # normal da API; a busca (search/issues) exige is:issue ou is:pull-request e para em 30 por minuto.
    saida = gh("api", "--paginate", "-X", "GET", f"repos/{ORG}/{repo}/issues", "-f", "state=all",
               "-f", f"labels={label}", "-f", "per_page=100", "--jq", ".[].number")
    return [int(n) for n in saida.split() if n]


def sincroniza(repo, cfg, aplicar):
    alvo = f"{ORG}/{repo}"
    atuais = labels_atuais(repo)
    print(f"== {alvo}")
    for l in cfg["labels"]:
        acao = "atualiza" if l["name"] in atuais else "cria"
        print(f"  {acao}: {l['name']}")
        if aplicar:
            gh("label", "create", l["name"], "-R", alvo, "--color", l["color"],
               "--description", l["description"], "--force")
    novas = {l["name"] for l in cfg["labels"]}
    for velha, destino in cfg["migrar"].items():
        if velha not in atuais or velha in novas:
            continue
        numeros = itens_com_label(repo, velha)
        print(f"  migra '{velha}' -> {destino or '(nada)'} em {len(numeros)} itens, depois apaga")
        if not aplicar:
            continue
        for n in numeros:
            if destino:
                gh("api", "-X", "POST", f"repos/{alvo}/issues/{n}/labels",
                   *sum((["-f", f"labels[]={d}"] for d in destino), []))
        gh("label", "delete", velha, "-R", alvo, "--yes")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--repo", action="append")
    a = p.parse_args()
    cfg = json.loads((RAIZ / "labels.json").read_text(encoding="utf-8"))
    for repo in a.repo or repos():
        sincroniza(repo, cfg, a.aplicar)
    if not a.aplicar:
        print("\n(simulação; rode com --aplicar)")


if __name__ == "__main__":
    sys.exit(main())
