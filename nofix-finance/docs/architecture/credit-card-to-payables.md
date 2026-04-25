# Nofix Finance, Integração de Parcelas de Cartão com Contas a Pagar

## Objetivo

Transformar parcelas de cartão em obrigações operacionais na base Contas a Pagar, para que o financeiro acompanhe vencimentos futuros.

## Regra inicial

Para cada parcela gerada no cartão:
- criar uma conta a pagar correspondente
- status inicial: Prevista
- tipo da conta: Variável
- vencimento igual ao da parcela
- valor previsto igual ao valor da parcela
- observação contendo referência da parcela

## Regras de proteção

- não criar conta a pagar duplicada para a mesma parcela
- usar um identificador derivado da parcela para idempotência

## Evolução futura

- vincular conta a pagar à parcela por relação nativa no Notion
- marcar pagamento da fatura e refletir em lote nas parcelas
- gerar lançamentos automáticos após quitação
