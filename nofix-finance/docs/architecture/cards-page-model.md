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

## Campos novos

### Valor total da fatura
Tipo sugerido:
- number

Uso:
- armazenar o valor consolidado da fatura atual do cartão
- pode vir da API ou preenchimento manual

### Competência da fatura
Tipo sugerido:
- rich_text

Uso:
- indicar o mês/competência da fatura atual

### Valor a pagar
Tipo sugerido:
- number

Uso:
- informar o valor efetivo esperado para pagamento

### Origem do cartão
Tipo sugerido:
- select: API, Manual

Uso:
- distinguir cartões sincronizados de cartões cadastrados manualmente
