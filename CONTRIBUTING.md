# Como contribuir

Vale para todo repositório da organização. Cada repositório pode ter regras a mais no próprio README.

## Fluxo

1. **Pedido.** Começa numa issue (formulário "Pedido de setor" ou "Funcionalidade"). Pedido de setor só vira trabalho com a aprovação do líder do setor escrita na issue.
2. **Spec antes do código.** Cada feature tem `docs/specs/AAAA-MM-DD-nome/` com `spec.md` (o que é, por que, "Pronto quando") e `tasks.md` (passos). Decisão de arquitetura vira ADR em `docs/adr/` antes do código.
3. **Branch.** `feat/<nome-da-spec>`, `fix/<assunto>`, `docs/<assunto>`. Nunca commit direto na `main`.
4. **Um item do `tasks.md` por PR.** PR pequeno é revisado no mesmo dia.
5. **PR** com o modelo preenchido. Revisão segue `docs/REVISAO.md`, aprovação segue `docs/APROVACAO-PR.md`.
6. **Merge** por squash. O branch é apagado depois.

## Marcas que destravam dúvida

| Marca | Quando usar |
|---|---|
| `[NEEDS CLARIFICATION: ...]` | dúvida que trava; spec fica `proposed` |
| `[SUPOSIÇÃO: valor; chave na aba Configuração]` | dúvida que só o setor responde; o código lê a chave |
| `[OUT OF SCOPE: ...]` | coisa que fica de fora de propósito |

## Commits

Mensagem curta em português, no imperativo, dizendo o que muda: `escala: filtra por dia`. Sem assinatura de IA no commit.

## IA

Pode usar. Mande a IA ler a spec e o `DESIGN.md` primeiro. Não aceite código que você não sabe explicar.

## Identidade

No GitHub vale o usuário; no departamento vale o nick da RCC. O par fica em `docs/CARGOS.md`. Nome do WhatsApp não serve de identificação.
