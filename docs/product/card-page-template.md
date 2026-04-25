# Nofix Finance, Template de página de Cartão

## Objetivo

Transformar a página de cada cartão em uma tela operacional.

## Estrutura recomendada

### 1. Resumo do cartão
Exibir no topo:
- Valor total da fatura
- Valor a pagar
- Competência da fatura
- Limite total
- Limite disponível
- Origem do cartão

### 2. Compras do cartão
Linked database de Compras no Cartão filtrada pelo cartão atual.

Colunas sugeridas:
- Descrição
- Data da compra
- Valor total
- Número de parcelas
- Processada?
- Status

### 3. Parcelas do cartão
Linked database de Parcelas do Cartão filtrada pelas parcelas relacionadas ao cartão.

Colunas sugeridas:
- Parcela
- Número da parcela
- Valor da parcela
- Vencimento
- Status

### 4. Contas a pagar do cartão
Linked database de Contas a Pagar filtrada pelas parcelas/contas ligadas ao cartão.

Colunas sugeridas:
- Título
- Valor previsto
- Vencimento
- Status

### 5. Observações
Espaço para notas operacionais e detalhes da integração.

## Primeira página piloto
- XP Banking
