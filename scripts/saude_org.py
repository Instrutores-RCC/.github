"""Confere se a organização continua nas regras de docs/MANUTENCAO.md.

Uso:
    python scripts/saude_org.py              # só mostra
    python scripts/saude_org.py --detalhe    # mostra também quem é (nick), só na sua máquina
    python scripts/saude_org.py --issue      # abre/atualiza a issue "Saúde da organização" no .github
                                             # e fecha quando tudo voltar ao normal

O .github é público: a issue e o log da ação levam só contagens, nunca nick de membro.
Precisa do gh com um token de dono da organização (ORG_TOKEN na ação).
"""
import argparse
import datetime as dt
import json
import subprocess
import sys

ORG = "Instrutores-RCC"
TITULO = "Saúde da organização"
REPO_ISSUE = f"{ORG}/.github"


def api(caminho, *extra, falha_ok=False):
    r = subprocess.run(["gh", "api", caminho, *extra], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        if falha_ok:
            return None
        raise RuntimeError(f"gh api {caminho}: {r.stderr.strip()}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def vencimento_token():
    r = subprocess.run(["gh", "api", "-i", "rate_limit"], capture_output=True, text=True, encoding="utf-8")
    for linha in r.stdout.splitlines():
        if linha.lower().startswith("github-authentication-token-expiration:"):
            texto = linha.split(":", 1)[1].strip()[:10]
            return dt.date.fromisoformat(texto)
    return None


def problemas():
    achados = []   # vai para a issue pública: sem nick
    pessoais = []  # com nick: só aparece com --detalhe
    org = api(f"orgs/{ORG}")
    if org.get("default_repository_permission") != "none":
        achados.append("Permissão base da organização não é `none`.")
    if org.get("members_can_create_repositories"):
        achados.append("Membros podem criar repositório (deveria ser só lider-dev/donos).")

    donos = api(f"orgs/{ORG}/members?role=admin&per_page=100")
    if len(donos) < 2:
        achados.append(f"Só {len(donos)} dono(s) na organização. Regra: 2 ou mais.")
    if "instrutoresrcc" not in {d["login"] for d in donos}:
        achados.append("A conta do departamento `instrutoresrcc` não é dona da organização.")

    sem_2fa = api(f"orgs/{ORG}/members?filter=2fa_disabled&per_page=100", falha_ok=True) or []
    if sem_2fa:
        achados.append(f"{len(sem_2fa)} membro(s) sem 2FA. Quem é: People da organização, filtro 2FA.")
        pessoais += [f"`{m['login']}` está sem 2FA." for m in sem_2fa]

    lideres = api(f"orgs/{ORG}/teams/lider-dev/members?per_page=100", falha_ok=True) or []
    if len(lideres) < 2:
        achados.append(f"Time `lider-dev` tem {len(lideres)} pessoa(s). Regra: 2 ou mais.")

    for r in api(f"orgs/{ORG}/repos?per_page=100"):
        if r["archived"] or r["name"] == ".github":
            continue
        nome = r["name"]
        if "rcc" not in r.get("topics", []):
            achados.append(f"`{nome}` sem o tópico `rcc` (rode `scripts/aplica_org.py --aplicar`).")
        if not api(f"repos/{ORG}/{nome}/contents/.github/CODEOWNERS", falha_ok=True):
            achados.append(f"`{nome}` sem `.github/CODEOWNERS`.")
        times = {t["slug"]: t["permission"] for t in api(f"repos/{ORG}/{nome}/teams", falha_ok=True) or []}
        if times.get("lider-dev") != "admin":
            achados.append(f"`{nome}` sem o time `lider-dev` como admin.")
        colab = api(f"repos/{ORG}/{nome}/collaborators?affiliation=direct&per_page=100", falha_ok=True) or []
        if colab:
            achados.append(f"`{nome}`: {len(colab)} acesso(s) individual(is) (regra: só por time). "
                           "Quem é: Settings > Collaborators and teams do repositório.")
            pessoais += [f"`{nome}`: `{c['login']}` tem acesso individual." for c in colab]
        empurrado = dt.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00"))
        if (dt.datetime.now(dt.timezone.utc) - empurrado).days > 365:
            achados.append(f"`{nome}` parado há mais de 1 ano: avaliar arquivar.")

    venc = vencimento_token()
    if venc and (venc - dt.date.today()).days < 30:
        achados.append(f"O token `ORG_TOKEN` vence em {venc.isoformat()}. Gere outro (docs/MANUTENCAO.md).")
    return achados, pessoais


def issue_aberta():
    saida = subprocess.run(
        ["gh", "issue", "list", "-R", REPO_ISSUE, "--state", "open", "--search", f'in:title "{TITULO}"',
         "--json", "number,title"], capture_output=True, text=True, encoding="utf-8").stdout
    for i in json.loads(saida or "[]"):
        if i["title"] == TITULO:
            return i["number"]
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--issue", action="store_true")
    p.add_argument("--detalhe", action="store_true", help="mostra os nicks; nunca use na ação")
    a = p.parse_args()
    if a.issue and a.detalhe:
        p.error("--detalhe não vai junto com --issue: o log da ação é público")
    achados, pessoais = problemas()
    hoje = dt.date.today().isoformat()
    corpo = f"Checagem de {hoje}.\n\n" + "\n".join(f"- [ ] {x}" for x in achados) + \
        "\n\nComo corrigir: [docs/MANUTENCAO.md](https://github.com/Instrutores-RCC/.github/blob/main/docs/MANUTENCAO.md)."
    print(corpo if achados else f"Tudo em ordem ({hoje}).")
    if a.detalhe and pessoais:
        print("\nQuem é (não publicar):\n" + "\n".join(f"- {x}" for x in pessoais))
    if not a.issue:
        return 0
    numero = issue_aberta()
    if achados and numero:
        subprocess.run(["gh", "issue", "edit", str(numero), "-R", REPO_ISSUE, "--body", corpo], check=True)
    elif achados:
        subprocess.run(["gh", "issue", "create", "-R", REPO_ISSUE, "--title", TITULO, "--body", corpo,
                        "--label", "tipo:tarefa"], check=True)
    elif numero:
        subprocess.run(["gh", "issue", "close", str(numero), "-R", REPO_ISSUE,
                        "--comment", f"Tudo em ordem em {hoje}."], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
