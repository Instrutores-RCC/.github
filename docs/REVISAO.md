# Modelo de code review

Quem revisa: time `revisores` (o CODEOWNERS chama sozinho). Prazo: PR pequeno no mesmo dia, PR grande em até 2 dias.

## Ordem da revisão

Pare no primeiro item que falhar e peça mudança.

1. **Spec.** O PR atende o "Pronto quando" da spec? Faz só o item do `tasks.md` que diz fazer?
2. **Segurança.** Algum segredo no diff? Toda escrita passa por validação de nick? Escreve na planilha viva? Mostra dado de pessoa real?
3. **Correção.** Casos de borda: lista vazia, nick com espaço ou acento, data no fim do mês, planilha fora do ar, duplo clique no botão.
4. **Testes.** Tem teste novo para o que mudou? Teste com data usa data fixa?
5. **Tela.** Celular primeiro (390 px), cor só por token do `DESIGN.md`, asset novo registrado.
6. **Leitura.** Nomes dizem o que é? Dá pra entender sem o autor explicar?

## Prefixos de comentário

| Prefixo | Significa | Bloqueia? |
|---|---|---|
| `bloqueia:` | erro, falha de segurança ou foge da spec | sim |
| `pergunta:` | não entendi; responda antes do merge | não |
| `sugestao:` | jeito melhor, o autor decide | não |
| `detalhe:` | nome, espaço, vírgula | não |
| `elogio:` | ficou bom, faça assim de novo | não |

Exemplo: `bloqueia: o doPost grava antes de conferir o nick (linha 42). Mover a checagem pra antes do appendRow.`

## Veredito

- **Aprovar**: nenhum `bloqueia:` em aberto.
- **Pedir mudanças**: pelo menos um `bloqueia:`. Diga o que destrava.
- **Comentar**: só perguntas ou sugestões, sem decidir ainda.

Revisor não reescreve o PR do outro. Sugere com bloco `suggestion` ou pede a mudança.
