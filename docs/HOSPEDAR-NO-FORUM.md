# Página HTML no fórum com CSS e JS hospedados

Como colocar uma página grande no fórum (Forumotion, **Módulos > Páginas HTML**) sem bater no limite de tamanho. Primeiro uso: Central do SRC, em 05/11/2026. Serve para qualquer projeto dos Instrutores que vira página no fórum.

## O problema

O fórum guarda a página inteira num campo de texto e não serve arquivo solto. A maior página que já funcionou tinha 82 mil caracteres. A Central minificada dava 130 mil e o fórum recusou salvar.

## O padrão

```
fórum (página HTML, uns 4 mil caracteres)
  markup + configuração (URL do Apps Script) + carregador
        │
        ├─ 1º  instrutores-rcc.github.io/forum-assets/<projeto>/<projeto>.<versão>.css|js   (GitHub Pages)
        ├─ 2º  cdn.jsdelivr.net/gh/Instrutores-RCC/forum-assets@<projeto>-<versão>/...      (reserva)
        └─ os dois falharam: "A <página> está fora do ar. Tente de novo em alguns minutos."
```

1. **Repositório público só com o que o build gera.** [`forum-assets`](https://github.com/Instrutores-RCC/forum-assets), uma pasta por projeto, branch única `gh-pages`. O código-fonte continua no repositório privado do projeto. Público porque, no plano gratuito, o GitHub Pages só serve repositório público.
2. **A versão vai no nome do arquivo.** Os 10 primeiros caracteres do hash do conteúdo (`central.a93c431591.js`). Arquivo publicado nunca muda. Versão nova é arquivo novo, então nenhum cache mostra versão velha misturada com nova.
3. **Uma tag por versão** (`central-a93c431591`). É o endereço da reserva no jsDelivr. Nunca aponte o jsDelivr para a branch: ele guarda branch em cache por dias.
4. **Impressão digital (SRI).** O html do fórum leva o `sha384` de cada arquivo no atributo `integrity`, com `crossOrigin='anonymous'`. Se alguém trocar o arquivo daquela versão, em qualquer um dos dois endereços, o navegador não roda. O Pages e o jsDelivr mandam `Access-Control-Allow-Origin: *`, que o SRI exige.
5. **Configuração fica no fórum, nunca no repositório público.** A URL `/exec` do Apps Script vai no html colado (`window.CENTRAL_API = "..."`). O JS público só lê essa variável. Nenhum id de planilha, script ou implantação entra no `forum-assets`.
6. **Página escondida até o CSS chegar.** Um `<style id="...-carregando">body{visibility:hidden}</style>` que o carregador tira depois que o CSS carrega, ou quando mostra o aviso. Sem isso aparece o markup cru por um instante.
7. **Ordem:** CSS primeiro, depois JS. Cada um tenta o Pages e, se falhar (rede, 404 ou impressão digital errada), a reserva.

## Como publicar uma versão

O script do projeto faz tudo. Na Central:

```bash
python3 ferramentas/monta_forum.py --publicar
```

1. Minifica CSS e JS (esbuild via `npx`).
2. Calcula a versão e grava `<projeto>.<versão>.css|js` num clone do `forum-assets`.
3. Faz commit, cria a tag `<projeto>-<versão>` e manda as duas para o GitHub.
4. Gera o html do fórum com a configuração, os dois endereços e as impressões digitais.

Rodar de novo sem mudar nada não sobe nada. Publique só depois que a PR entrou na `main` do projeto. `--hospedado` monta sem subir, para conferir antes.

## Como o admin atualiza

Cada versão gera um html novo. O admin abre a página no painel do fórum, apaga tudo e cola o html novo. Os arquivos das versões antigas continuam no ar, então a página que estava colada segue funcionando até a troca.

## Teste antes de mandar para o fórum

Sirva a pasta de saída em `127.0.0.1` e abra quatro cópias do html:

| Cópia | Mudança | Esperado |
|---|---|---|
| normal | nenhuma | CSS e JS do Pages |
| reserva | primeiro endereço trocado por um que não existe | CSS e JS do jsDelivr |
| adulterada | uma letra do `sha384` do JS trocada | JS recusado nos dois endereços, aviso de fora do ar |
| fora do ar | os dois endereços trocados | aviso de fora do ar |

## Quando não usar

Se o projeto cabe em menos de 82 mil caracteres, deixe tudo dentro do html. É uma peça a menos. Para páginas entre 82 mil e uns 200 mil, a Central tem um segundo modo: CSS e JS minificados, compactados (deflate + base64) e descompactados no navegador com `DecompressionStream`. Ficou em 54 mil caracteres, mas não funciona em navegador anterior a 2023 e cada mudança pede colar tudo de novo do mesmo jeito.

## Reaproveitar num projeto novo

1. Copie a parte hospedada do `ferramentas/monta_forum.py` da Central (funções `hospedar` e `publicar`, `CARREGADOR_HOSPEDADO`).
2. Troque `PROJETO` pelo nome da pasta nova no `forum-assets` e o id do elemento de carregamento.
3. Troque a variável de configuração (`CENTRAL_API`) por uma com o nome do projeto.
4. Rode os quatro testes da tabela acima antes de mandar o html para o admin.
