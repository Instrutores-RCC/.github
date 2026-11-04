# Segurança

## Como relatar uma falha

**Nunca abra issue, PR ou post no fórum sobre uma falha que alguém consegue explorar.**

1. Mande MP no fórum ou mensagem privada no WhatsApp para alguém do time `lider-dev` (lista em `docs/CARGOS.md`).
2. Diga: onde está, como repetir, o que dá pra fazer com ela. Não teste em dados reais de outra pessoa.
3. Resposta em até 72 horas. A correção sai em PR com título genérico ("ajuste de validação"), e o detalhe só é contado depois de corrigido.

## Regras que valem em todo repositório

1. **Segredo não entra no git.** Id de planilha, id de implantação do Apps Script, token, senha e chave ficam em `ids.json` ou `.env`, ambos no `.gitignore`. Se vazou, avise o `lider-dev` na hora: apagar o commit não basta, o segredo é trocado.
2. **Toda escrita confere quem escreve.** No Apps Script, o `doPost` valida o nick contra a aba de acesso antes de gravar. Leitura pública (`doGet`) só devolve o que já é público no fórum.
3. **Planilha viva do setor não recebe escrita de desenvolvimento.** Desenvolvimento e teste só numa cópia. A troca para a viva é aprovada pelo líder do setor.
4. **Pessoa real só com consentimento.** Nenhum print, avatar ou nick real em asset, fixture ou exemplo sem autorização escrita da pessoa. Exemplo usa boneco genérico (`figure=`), nunca `user=` de alguém.
5. **Dado pessoal mínimo.** Guarde só o nick e o que o setor precisa. Nada de e-mail, telefone ou IP de membro em planilha ou repositório.
6. **Dependências.** Dependabot fica ligado. Alerta crítico é corrigido antes de qualquer feature.
7. **Acesso.** Permissão vem do time, nunca de convite individual por repositório. Quem sai do departamento sai dos times no mesmo dia.
