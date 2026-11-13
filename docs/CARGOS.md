# Cargos e times

Permissão no GitHub vem do time, nunca de convite individual. Quem muda de cargo no departamento muda de time no mesmo dia.

## Cargos dos Instrutores (time pai `instrutores`)

| Time | Cargo na RCC | Acesso |
|---|---|---|
| `lideranca` | Líder `{L.INS}` e Vice-líder `{VL.INS}` | triage: rotula, fecha e prioriza issue |
| `ministerio` | Ministros `{Min.INS}` | read: lê e abre issue |
| `capacitadores` | Capacitadores `{Cap.INS}` | read |
| `avaliadores` | Avaliadores `{Av.INS}` | read |
| `estagiarios` | Estagiários `{Est.INS}` | read |

## Setores (time pai `setores`)

| Time | Setor | Acesso |
|---|---|---|
| `setor-src` | SRC, Setor de Relações Comunicativas | triage nos repositórios do SRC |
| `setor-ssi` | SSI, Setor de Segurança dos Instrutores | triage nos repositórios do SSI |
| `setor-da` | DA, Departamento de Aplicação | triage nos repositórios do DA |

O líder do setor aprova o escopo dos pedidos e tira o `estado:aguarda-setor`. Repositório de cada setor leva o tópico `setor-<sigla>`.

## Departamento de Desenvolvimento (time pai `desenvolvimento`)

Estar em qualquer time daqui = marcador `[DEV]` (Desenvolvedor da Companhia) no fórum.

| Time | Cargo | Acesso | Faz |
|---|---|---|---|
| `lider-dev` | Líder de Desenvolvimento | admin | arquitetura, cria repositório, recebe relato de segurança, segunda aprovação em PR sensível |
| `revisores` | Revisor | maintain | aprova PR, mantém labels e marcos |
| `desenvolvedores` | Desenvolvedor | write (triage no `.github`) | escreve spec, implementa, abre PR |
| `designers` | Designer | write (triage no `.github`) | assets, `DESIGN.md`, protótipos; dono de `design/` |
| `aprendizes-dev` | Aprendiz de Desenvolvimento | write nos repositórios de missão (`central-do-src`, `ouvidoria-ins`, `systemins`), triage nos outros | pega a missão, todo PR com mentor |

### Como sobe

- Aprendiz → Desenvolvedor: 3 PRs aprovados sem `bloqueia:` em aberto.
- Desenvolvedor → Revisor: 10 PRs aprovados e 5 revisões feitas acompanhadas por um revisor.
- Revisor → Líder: decisão da liderança do departamento.

## Quem é quem

Nome do WhatsApp não vale. Sempre nick da RCC.

| Nick RCC | GitHub | Times |
|---|---|---|
| JokesD | `LucasSantana-Dev` | lider-dev, revisores |
| Crebes | `carloshsnafeu` | lider-dev, revisores (convite pendente) |
| conta do departamento | `instrutoresrcc` | dona da organização |
