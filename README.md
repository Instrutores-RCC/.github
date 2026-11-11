# .github da Instrutores-RCC

Este repositório guarda o padrão da organização inteira. O que está aqui vale para todos os repositórios sem precisar copiar nada.

Ele é público de propósito: no plano gratuito do GitHub, só repositório `.github` público empresta modelos e workflows para os privados. Por isso aqui **não entra** dado da RCC (nicks, planilhas, ids, tokens). Só regra e modelo.

## O que tem aqui

| Pasta ou arquivo | Para que serve | Quem usa |
|---|---|---|
| `profile/README.md` | Página inicial da organização no GitHub | Quem visita a org |
| `ISSUE_TEMPLATE/` | Formulários de issue: bug, pedido de setor, funcionalidade, pedido de arte, melhoria de segurança. Issue em branco desligada | Todo mundo que abre issue |
| `PULL_REQUEST_TEMPLATE.md` | Corpo padrão de PR (spec, como testar, prints, checklist) | Quem abre PR |
| `CONTRIBUTING.md` | Como trabalhar: spec antes do código, um item do `tasks.md` por PR | Devs |
| `SECURITY.md` | Como relatar falha de segurança (nunca em issue) e regras de segredo | Todo mundo |
| `CODE_OF_CONDUCT.md` | Conduta, alinhada ao CCM da RCC | Todo mundo |
| `labels.json` | Lista única de labels de todos os repositórios | Ação `Sincroniza labels` |
| `docs/` | Regras do departamento (tabela abaixo) | Devs e liderança |
| `scripts/` | Scripts que montam e conferem a organização (tabela abaixo) | Ações e `lider-dev` |
| `.github/workflows/` | Automações (tabela abaixo) | GitHub Actions |
| `.github/dependabot.yml` | Atualiza as ações usadas nos workflows, todo mês | Dependabot |

## Documentos (`docs/`)

| Arquivo | Assunto |
|---|---|
| [CARGOS.md](docs/CARGOS.md) | Times, permissões, quem é quem e como subir de cargo |
| [APROVACAO-PR.md](docs/APROVACAO-PR.md) | Quando um PR pode entrar na `main` e o que é trava automática |
| [REVISAO.md](docs/REVISAO.md) | Como revisar código: ordem, prefixos (`bloqueia:`, `sugestao:`...) e veredito |
| [LABELS.md](docs/LABELS.md) | O que cada label quer dizer |
| [ASSETS.md](docs/ASSETS.md) | Regras de imagem, pixel art, proveniência e consentimento |
| [HOSPEDAR-NO-FORUM.md](docs/HOSPEDAR-NO-FORUM.md) | Página HTML no fórum com CSS e JS no `forum-assets` (Pages, reserva no jsDelivr, SRI) |
| [MANUTENCAO.md](docs/MANUTENCAO.md) | Continuidade: quem sai, quem entra, revisão trimestral, token, recriar tudo |

## Scripts (`scripts/`)

Só Python padrão e o `gh` logado. Sem `--aplicar` eles só mostram o que fariam. Podem rodar quantas vezes quiser sem estragar nada.

| Script | Faz |
|---|---|
| `aplica_org.py` | Cria os 16 times, dá permissão por time em cada repositório, põe tópicos, fixa merge só squash e protege a `main` |
| `sincroniza_labels.py` | Deixa as labels de cada repositório iguais ao `labels.json`, migrando as antigas antes de apagar |
| `saude_org.py` | Confere as regras de continuidade e, com `--issue`, abre ou fecha a issue "Saúde da organização" (só contagens, sem nick); com `--detalhe`, mostra os nicks na tela |

```bash
python scripts/aplica_org.py              # simulação
python scripts/aplica_org.py --aplicar    # aplica
```

## Automações (`.github/workflows/`)

| Workflow | Quando roda | Faz |
|---|---|---|
| `pr-padrao.yml` | Chamado pelo `pr.yml` de cada repositório | Barra segredo e arquivo proibido no PR, roda os testes do repositório, rotula o PR pela pasta, marca a issue ligada como `estado:em-revisao`, avisa se faltar "Como testar" e abre issue se alguém mandar commit direto na `main` |
| `saude-org.yml` | Toda segunda, 12h UTC | Reaplica `aplica_org.py` e roda `saude_org.py --issue` |
| `sincroniza-labels.yml` | Ao mudar `labels.json` e todo dia 1º | Roda `sincroniza_labels.py --aplicar` |
| `revisao-trimestral.yml` | Jan, abr, jul e out | Abre a issue com o checklist da revisão trimestral |
| `valida.yml` | Todo PR e push neste repositório | Confere se scripts, `labels.json` e YAML abrem sem erro (check obrigatório da `main`) |

`saude-org` e `sincroniza-labels` precisam do segredo `ORG_TOKEN` (como criar: [MANUTENCAO.md](docs/MANUTENCAO.md#token-de-automação)). Sem ele as duas falham e mandam e-mail; o resto continua funcionando.

### Ligar o padrão num repositório

Crie `.github/workflows/pr.yml` no repositório (o `modelo-projeto` já vem com ele):

```yaml
name: PR
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  pull-requests: write
  issues: write
jobs:
  padrao:
    uses: Instrutores-RCC/.github/.github/workflows/pr-padrao.yml@main
    with:
      teste: "node testes/testa_codigo.js"   # vazio se o projeto não tem testes
```

## Repositório novo

1. `lider-dev` cria a partir do modelo: **Use this template** em `modelo-projeto`.
2. Põe o tópico do setor dono (ex.: `setor-src`) em `aplica_org.py` (`TOPICOS`).
3. Na segunda seguinte a ação de saúde aplica times, permissões e regras. Para não esperar: `python scripts/aplica_org.py --aplicar`.

## Mudar uma regra

Tudo aqui muda por PR, como qualquer código. A `main` deste repositório é travada: precisa de 1 aprovação de `lider-dev` (CODEOWNERS) e do check `valida` verde. Mudou `labels.json`, as labels de todos os repositórios se atualizam sozinhas depois do merge.
