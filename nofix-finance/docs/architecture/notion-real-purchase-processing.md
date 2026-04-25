# Nofix Finance, Processamento de Compras Reais do Notion

## Objetivo

Ler compras reais cadastradas na base Compras no Cartão e processá-las automaticamente pelo Nofix.

## Etapas

1. Buscar compras na base Compras no Cartão.
2. Identificar compras aptas para processamento.
3. Extrair os campos necessários.
4. Aplicar a engine de parcelamento.
5. Criar parcelas no Notion.
6. Atualizar limite do cartão correspondente.
7. Evitar duplicidade.

## Requisito funcional importante

A base Compras no Cartão precisa ter dados mínimos consistentes:
- descrição
- valor total
- data da compra
- número de parcelas
- cartão vinculado ou identificável

## Estratégia inicial

Na primeira versão, o script pode usar um cartão padrão configurado enquanto a relação direta com o cadastro de cartões ainda não estiver completa.

## Evolução seguinte

- ler relação nativa entre compra e cartão
- marcar compra como processada
- criar vínculo entre compra e parcelas
