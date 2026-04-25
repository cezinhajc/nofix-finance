# Nofix Finance, Modelagem da página Cartões

## Objetivo

Transformar a base Cartões em uma visão consolidada por cartão, suportando dois cenários:
- cartões sincronizados por API, como a Pierre
- cartões cadastrados manualmente

## Requisitos da base Cartões

Cada cartão deve consolidar:
- nome do cartão
- banco
- bandeira
- limite total
- limite disponível
- mês de competência
- valor total da fatura
- quanto será pago
- observações operacionais

## Estratégia de uso

### Cartões por API
- cartão é atualizado por integração
- valor total da fatura vem da API
- limite total e limite disponível podem ser atualizados automaticamente

### Cartões manuais
- cartão pode ser criado sem API
- valor total da fatura pode ser informado manualmente
- compras podem ser lançadas no Notion e consolidadas por operação interna

## Campo novo

### Valor total da fatura
Tipo sugerido:
- number

Uso:
- armazenar o valor consolidado da fatura atual do cartão
- pode vir da API ou preenchimento manual

## Evolução futura

Também faz sentido incluir depois:
- Competência da fatura
- Valor a pagar
- Fonte do cartão (API ou Manual)
