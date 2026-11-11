# Manutenção e continuidade

A organização não depende de uma pessoa. Se qualquer dev sair, nada para.

## Regras de continuidade

1. **Sempre 2 donos (Owner) ou mais**, e um deles é a conta do departamento `instrutoresrcc`.
2. A senha e o 2FA da `instrutoresrcc` ficam com a Liderança dos Instrutores (L.INS e VL.INS), não com um dev. Códigos de recuperação guardados pela Liderança.
3. `lider-dev` tem sempre **2 pessoas ou mais**. Se ficar com 1, a primeira tarefa é promover um revisor.
4. Acesso só por time. Ninguém tem permissão individual em repositório.
5. Repositório pessoal não guarda projeto do departamento: projeto vivo mora na organização.
6. Token de automação mora na conta `instrutoresrcc`, nunca na conta pessoal de um dev.

## Quando alguém sai

| Passo | Quem | Onde |
|---|---|---|
| Tirar dos times | lider-dev | People → membro → Remove from organization |
| Conferir se era dono de algo no CODEOWNERS | lider-dev | `.github/CODEOWNERS` dos repos |
| Passar issues abertas para outra pessoa | revisores | filtro `assignee:<usuario>` |
| Atualizar a tabela "Quem é quem" | lider-dev | `docs/CARGOS.md` |
| Se era `lider-dev`: trocar a senha do token de automação se ele tinha acesso | Liderança INS | conta `instrutoresrcc` |

## Quando alguém entra

1. Pede pelo fórum, informando nick RCC e usuário GitHub.
2. `lider-dev` convida para a organização direto no time certo (Aprendiz começa em `aprendizes-dev`).
3. Adiciona a linha em `docs/CARGOS.md`.

## O que roda sozinho

| O quê | Como |
|---|---|
| Labels iguais em todos os repositórios | Ação `Sincroniza labels`: roda ao mudar `labels.json` e todo dia 1º |
| Conferência das regras desta página | Ação `Saúde da organização`: toda segunda; abre a issue "Saúde da organização" se algo saiu da regra e fecha quando volta |
| Lembrete da revisão trimestral | Ação `Revisão trimestral`: abre a issue com o checklist em jan, abr, jul e out |
| Checagem de segredo, testes e rótulos em todo PR | Workflow reutilizável `pr-padrao.yml`, chamado por `.github/workflows/pr.yml` de cada repositório |
| Issue marcada `estado:em-revisao` quando o PR que a fecha abre | Mesmo `pr-padrao.yml` (job `rotulos`) |
| Aviso de commit direto na `main` | Mesmo `pr-padrao.yml` (job `push-direto`) abre issue |
| Regras de merge e proteção da `main` reaplicadas | Ação `Saúde da organização` roda `aplica_org.py --aplicar` toda segunda |
| Validação deste repositório | Ação `Valida configuração`: scripts, `labels.json` e formulários abrem sem erro |
| Ações sempre atualizadas | Dependabot abre PR mensal quando uma ação usada fica velha |
| Templates de issue e PR | Herdados deste repositório `.github` por todos os repositórios |
| Alerta de dependência | Dependabot ligado por padrão em repositório novo |
| Estrutura de repositório novo | Criar a partir do modelo `modelo-projeto` |

## Revisão trimestral (15 minutos, lider-dev)

Em janeiro, abril, julho e outubro:

- [ ] Ação `Sincroniza labels` está verde.
- [ ] Token `ORG_TOKEN` não vence nos próximos 90 dias (Settings → Secrets).
- [ ] Ainda há 2 donos e 2 pessoas em `lider-dev`.
- [ ] Ninguém inativo há 6 meses nos times (se tiver, tirar).
- [ ] Alertas do Dependabot zerados ou com issue aberta.
- [ ] Repositório parado há 1 ano: arquivar (Settings → Archive).

## Token de automação

As ações de labels e de saúde precisam de um token com acesso de administração aos repositórios.

1. Entrar na conta `instrutoresrcc`.
2. Settings → Developer settings → Fine-grained tokens → Generate.
3. Dono: `Instrutores-RCC`; repositórios: todos; permissões de repositório: Administration (leitura e escrita), Contents (leitura), Issues (leitura e escrita), Metadata (leitura); permissões da organização: Members (leitura). Validade: 1 ano.
4. Neste repositório: Settings → Secrets and variables → Actions → `ORG_TOKEN`.
5. Anotar a data de vencimento na issue fixada "Vencimento do token".

Sem o token essas duas ações falham e manda e-mail; nada mais quebra. Dá para rodar na mão: `python scripts/sincroniza_labels.py --aplicar`.

## Recriar tudo do zero

Se a organização for bagunçada, este repositório reconstrói a estrutura:

```bash
python scripts/aplica_org.py --aplicar
python scripts/sincroniza_labels.py --aplicar
```

Os dois scripts só usam Python e `gh`, sem dependência extra, e podem rodar de novo sem estragar nada.
