# Nofix Finance, Integração inicial entre Cartão e Notion

## Objetivo

Conectar a lógica de cartão de crédito do Nofix com as bases do Notion para permitir processamento operacional.

## Fluxo inicial

1. Ler um registro da base Compras no Cartão.
2. Ler o cartão associado.
3. Aplicar a engine de parcelamento.
4. Gerar registros em Parcelas do Cartão.
5. Calcular o novo limite disponível.
6. Preparar a atualização do cartão no Notion.

## Primeira entrega

Nesta etapa, o worker fará o processamento técnico e registrará a saída.
A escrita completa e automática com relações poderá ser incrementada na sequência.

## Evolução esperada

- gravar parcelas no Notion
- atualizar limite do cartão
- gerar contas a pagar vinculadas
- impedir duplicidade de processamento

## Regra de idempotência inicial

Antes de criar parcelas, o worker deve verificar se já existem registros com o mesmo rótulo de parcela para a mesma compra processada.

Se encontrar correspondência, deve interromper a criação e sinalizar que a compra já foi processada.
