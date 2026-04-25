# Montagem manual da página XP Banking no Notion

## Objetivo

Usar a página do cartão XP Banking como piloto de tela operacional.

## Blocos sugeridos dentro da página

### Seção 1, Resumo
Adicionar bloco de título:
- Resumo da fatura

Manter visíveis nas propriedades da página:
- Valor total da fatura
- Valor a pagar
- Competência da fatura
- Limite total
- Limite disponível
- Origem do cartão

### Seção 2, Compras do cartão
Inserir linked view da base Compras no Cartão.

Filtro sugerido:
- Cartão contém XP Banking
ou, quando a relação estiver estável:
- Cartão Rel contém esta página

### Seção 3, Parcelas do cartão
Inserir linked view da base Parcelas do Cartão.

Filtro sugerido:
- observações contém purchase_key relacionado a compras XP
ou relação nativa futura com cartão via compra

### Seção 4, Contas a pagar
Inserir linked view da base Contas a Pagar.

Filtro sugerido:
- Parcela Rel não vazio
- ou observações relacionadas às parcelas do cartão

## Observação

A melhor experiência virá quando consolidarmos todas as compras importadas com relação nativa ao cartão correto.
