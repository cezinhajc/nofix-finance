# Nofix Finance, Modelagem de Cartão de Crédito no Notion

## Objetivo

Criar uma estrutura inicial para registrar cartões, compras e parcelas no Notion, preparando a automação futura do Nofix.

## Bases propostas

### 1. Cartões
Cadastro dos cartões de crédito.

Propriedades sugeridas:
- Nome do cartão (title)
- Banco (rich_text)
- Bandeira (select)
- Limite total (number)
- Limite disponível (number)
- Dia de fechamento (number)
- Dia de vencimento (number)
- Titular (rich_text)
- Ativo? (checkbox)
- Observações (rich_text)

### 2. Compras no Cartão
Registro da compra principal.

Propriedades sugeridas:
- Descrição (title)
- Cartão (relação futura)
- Valor total (number)
- Data da compra (date)
- Parcelado? (checkbox)
- Número de parcelas (number)
- Valor da parcela (number)
- Primeira fatura (date)
- Status (select: Aberta, Faturada, Quitada, Cancelada)
- Observações (rich_text)

### 3. Parcelas do Cartão
Registro granular das parcelas.

Propriedades sugeridas:
- Parcela (title)
- Compra mãe (relação futura)
- Número da parcela (number)
- Valor da parcela (number)
- Competência (date)
- Vencimento (date)
- Status (select: Aberta, Faturada, Paga, Cancelada)
- Lançamento gerado? (checkbox)
- Observações (rich_text)

## Observação

Nesta primeira fase, a modelagem será estrutural.
As relações automáticas, o cálculo de limite e a geração de parcelas por automação ficarão para a próxima etapa do Nofix.
