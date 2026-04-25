# Integração Pierre → Nofix Finance

## Objetivo

Usar a API da Pierre para importar compras de cartão de crédito do mês e refletir isso no modelo operacional do Nofix no Notion.

## Objetivos imediatos

1. Listar compras do cartão no mês atual
2. Mapear essas compras para o schema do Nofix

## Endpoints principais

### 1. Get Transactions
Uso principal:
- listar compras de cartão de crédito do mês

Filtro recomendado:
- startDate = primeiro dia do mês
- endDate = hoje
- accountType = CREDIT
- accountSubtype = CREDIT_CARD
- format = structured ou raw

Campos úteis esperados:
- id
- description
- amount
- date
- status
- account_name
- account_type
- account_subtype
- merchant
- transaction_type
- transaction_subtype

### 2. Get Installments
Uso principal:
- complementar compras parceladas
- obter cronograma de parcelas
- identificar dueDate e installmentNumber

Campos úteis esperados:
- purchaseDate
- totalAmount
- installments[].description
- installments[].amount
- installments[].installmentNumber
- installments[].totalInstallments
- installments[].dueDate
- installments[].status

### 3. Get Bill Summary
Uso principal:
- atualizar limite total
- atualizar limite disponível
- atualizar visão de fatura atual

Campos úteis esperados:
- account_id
- account_name
- credit_limit
- available_credit_limit
- closing_day
- approx_current_bill_amount

## Estratégia de ingestão

### Passo 1, compras do mês
Chamar get-transactions para trazer compras do cartão no período atual.

### Passo 2, parcelados
Chamar get-installments para enriquecer o que for parcelado.

### Passo 3, limite e fatura
Chamar get-bill-summary para atualizar dados do cartão.

## Mapeamento para o Nofix

### Cartões
Pierre -> Nofix Cartões
- account_name -> Nome do cartão
- credit_limit -> Limite total
- available_credit_limit -> Limite disponível
- closing_day -> Dia de fechamento

### Compras no Cartão
Pierre -> Nofix Compras no Cartão
- description/merchant -> Descrição
- amount ou totalAmount -> Valor total
- date/purchaseDate -> Data da compra
- installments total -> Número de parcelas
- status -> Status
- account_name -> Cartão
- id -> identificador externo futuro

### Parcelas do Cartão
Pierre Installments -> Nofix Parcelas do Cartão
- description -> Parcela
- installmentNumber -> Número da parcela
- amount -> Valor da parcela
- dueDate -> Vencimento
- status -> Status

### Contas a Pagar
Nofix gera a partir das parcelas
- Título = label da parcela
- Valor previsto = valor da parcela
- Vencimento = dueDate
- Status = Prevista/Paga conforme contexto

## Regras recomendadas

### Idempotência
- usar transaction id da Pierre para compras não parceladas
- usar combinação purchase id + installmentNumber para parceladas
- salvar external_id no Nofix futuramente

### Importação inicial
- importar apenas o mês atual
- focar primeiro em um cartão
- revisar duplicidades antes de ampliar

## Próxima etapa técnica

1. criar client Pierre no Nofix
2. testar get-transactions do mês
3. persistir compras no Notion
4. enriquecer parcelados com get-installments
5. atualizar cartão com get-bill-summary
