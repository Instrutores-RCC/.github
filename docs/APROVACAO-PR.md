# Aprovação de PR

## Regras

1. Toda mudança na `main` entra por PR. Nada de push direto.
2. **1 aprovação** de alguém do time `revisores`.
3. **2 aprovações** (uma do `lider-dev`) quando o PR mexe em: servidor (`script/`, Apps Script), `SECURITY.md`, `.github/`, acesso e permissão, ou dados de membros.
4. Autor não aprova o próprio PR.
5. Push depois da aprovação anula a aprovação. Peça de novo.
6. Todas as conversas resolvidas antes do merge.
7. Merge por **squash**. Branch apagado depois.
8. PR de `estagiarios-dev` precisa de revisor, e o `lider-dev` fica marcado.
9. Mudança que o setor vai ver (tela, texto, regra) só vai pro ar com o ok do líder do setor registrado na issue.

## Quem faz o merge

O autor, depois da aprovação. Se o autor for estagiário, o revisor que aprovou.

## Limite técnico atual

A organização está no plano gratuito. Nesse plano o GitHub não deixa travar a `main` de repositório privado (proteção de branch e rulesets pedem plano pago). Então estas regras valem por combinado: o CODEOWNERS pede a revisão, e merge sem aprovação é tratado pela liderança do departamento. Se a organização passar para o plano Team, as regras 1, 2, 4, 5, 6 e 7 viram trava automática.

O que já é automático mesmo no plano gratuito:

- Repositório público (`.github`): `main` travada de verdade. Só por PR, 1 aprovação do CODEOWNERS, aprovação cai com push novo, check `valida` verde, conversas resolvidas, sem force push e sem apagar a branch.
- Todos os repositórios: só merge squash e a branch é apagada depois do merge.
- Commit direto na `main` sem PR abre sozinho uma issue `estado:bloqueado` (job `push-direto` do `pr-padrao.yml`).
- Toda segunda a ação `Saúde da organização` reaplica estas regras com `scripts/aplica_org.py`. Se um dia o plano virar Team, a trava passa a valer nos privados sem ninguém mexer.
