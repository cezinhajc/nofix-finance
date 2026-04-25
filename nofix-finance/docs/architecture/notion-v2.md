# Nofix Finance, Evolução do Schema Notion v2

## Novas bases operacionais

Para tornar o Nofix utilizável como financeiro operacional, a estrutura deve incluir duas bases adicionais:

- Contas a Pagar
- Contas a Receber

A base Lançamentos continua existindo como livro consolidado do realizado.

## Princípio de modelagem

- Contas a Pagar: obrigações financeiras
- Contas a Receber: receitas previstas
- Lançamentos: histórico realizado e conciliado

## Contas a Pagar

Propriedades sugeridas:
- Título (title)
- Entidade
- Tipo da conta (Fixa, Variável)
- Status (Prevista, Paga, Vencida, Cancelada)
- Categoria
- Fornecedor
- Valor previsto
- Valor pago
- Competência
- Vencimento
- Data de pagamento
- Conta bancária
- Forma de pagamento
- Recorrente?
- Periodicidade
- Centro de custo
- Observações

## Contas a Receber

Propriedades sugeridas:
- Título (title)
- Entidade
- Tipo da conta (Fixa, Variável)
- Status (Prevista, Recebida, Vencida, Cancelada)
- Categoria
- Cliente/Projeto
- Valor previsto
- Valor recebido
- Competência
- Vencimento
- Data de recebimento
- Conta bancária
- Forma de recebimento
- Recorrente?
- Periodicidade
- Observações

## Botões e templates recomendados

No front operacional do Notion, usar botões ou templates para:
- Novo pagamento fixo
- Novo pagamento variável
- Novo recebimento fixo
- Novo recebimento variável
- Novo lançamento manual

## Observação importante

O Notion não deve carregar sozinho toda a lógica financeira do produto.
Ele é a camada operacional inicial.
A lógica de recorrência, conciliação e automação deve evoluir no Nofix Finance como produto.
