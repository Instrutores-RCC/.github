# Uso de assets

Asset = imagem, ícone, mascote, fundo, boneco, fonte ou som usado num projeto.

## Onde fica

```
design/
  assets/            o que entra no produto
    README.md        tabela de todo arquivo (obrigatória)
  gemini/            prompts, jobs e proveniência dos renders
    gen/<nome>.provenance.json
  refs/              referências (não vão pro produto)
```

Originais em tamanho cheio ficam fora do git (`.gitignore`).

## Toda imagem nova precisa de

1. **Linha no `design/assets/README.md`**: arquivo, origem (render, manual do fórum com link, autor), onde entra no produto.
2. **Aprovação** com nick, data e a frase de quem aprovou.
3. **Proveniência**, se for gerada por IA: prompt, referência e hash em `gemini/gen/<nome>.provenance.json`.

## Regras de imagem

1. **Pixel art só escala em número inteiro** (1x, 2x, 4x, 8x), vizinho mais próximo, `image-rendering: pixelated`. Nunca 1,5x.
2. Exportar nativo + `@4x` + `@8x`, fundo transparente.
3. Mascote e emblema de um setor são do setor. Reuso em outro projeto só com o ok do líder daquele setor. Mascote não é espelhado nem suavizado.
4. **Pessoa real só com consentimento escrito.** Exemplo usa boneco genérico do imager do Habbo (`figure=`), nunca `user=` de alguém.
5. Arte de terceiros só com origem e autorização registradas.
6. Página hospedada no fórum embute a imagem como data URI (o repositório é privado, não tem link público).
7. Comprima sem perder qualidade antes do commit. Ícone até 96 px, ilustração até 320 px de altura, salvo pedido na spec.
8. Sem emoji como ícone.

## Quem mexe

O time `designers` é dono de `design/` no CODEOWNERS. Qualquer dev pode propor; o merge pede aprovação de um designer.

## Pedir arte

Abra issue com o formulário "Pedido de arte ou asset".

Exemplo completo de README de assets: `central-do-src/design/assets/README.md`.
