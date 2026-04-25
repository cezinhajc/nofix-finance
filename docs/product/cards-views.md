# Nofix Finance, organização visual da página Cartões

## Objetivo

Deixar a base Cartões mais clara para uso diário, separando o que é essencial de controle financeiro do que é cadastro técnico.

## Colunas principais para manter visíveis

Ordem sugerida:
1. Nome do cartão
2. Origem do cartão
3. Valor total da fatura
4. Valor a pagar
5. Competência da fatura
6. Limite total
7. Limite disponível
8. Dia de fechamento
9. Ativo?

## Colunas secundárias

Podem ficar mais ao final ou ocultas quando necessário:
- Banco
- Bandeira
- Titular
- Observações

## Views recomendadas

### 1. Cartões ativos
Filtro:
- Ativo? = true

Mostrar:
- Nome do cartão
- Origem do cartão
- Valor total da fatura
- Valor a pagar
- Competência da fatura
- Limite disponível

### 2. Cartões por API
Filtro:
- Origem do cartão = API

### 3. Cartões manuais
Filtro:
- Origem do cartão = Manual

### 4. Visão completa
Sem filtro, com todas as colunas de cadastro.

## Uso recomendado

- visão padrão do dia a dia: Cartões ativos
- visão operacional/técnica: Visão completa

## Próximo passo futuro

Quando a modelagem amadurecer, vale incluir rollups e relações para consolidar total de compras por competência diretamente no cartão.
