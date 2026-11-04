# Labels

Fonte única: `labels.json`. Para aplicar em todos os repositórios: `python scripts/sincroniza_labels.py`.

Toda issue tem **um `tipo:`**, **um `setor:`** e **um `estado:`**. `prioridade:` e `area:` são opcionais.

| Grupo | Labels | Quem põe |
|---|---|---|
| `tipo:` | bug, funcionalidade, melhoria, docs, arte, seguranca, tarefa | o formulário, ou quem abriu |
| `setor:` | src, ssi, da, ouvidoria, lideranca, ministerio | quem triou |
| `estado:` | precisa-spec, aguarda-setor, pronto-pra-dev, em-andamento, em-revisao, bloqueado | revisores e líder do setor |
| `prioridade:` | alta, media, baixa | lider-dev com o setor |
| `area:` | forum, apps-script, planilha, design, assets, testes | dev |
| outras | good first issue, duplicate, wontfix | qualquer um com triage |

## Caminho do `estado:`

`aguarda-setor` (setor aprova) → `precisa-spec` (dev escreve a spec) → `pronto-pra-dev` → `em-andamento` (branch aberto) → `em-revisao` (PR aberto) → fechada pelo merge. `bloqueado` em qualquer ponto, com comentário dizendo o quê.
