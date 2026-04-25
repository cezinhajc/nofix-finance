# Nofix Finance, Automação de Cartão de Crédito

## Objetivo

Definir a lógica inicial para processar compras no cartão de crédito, gerar parcelas, calcular vencimentos e preparar impactos financeiros no Nofix.

## Fluxo esperado

1. Usuário registra uma compra em Compras no Cartão.
2. O Nofix lê os dados da compra.
3. O sistema identifica o cartão usado.
4. Calcula valor da parcela.
5. Gera todas as parcelas futuras.
6. Define competência e vencimento de cada parcela.
7. Atualiza limite disponível do cartão.
8. Prepara integração futura com Contas a Pagar e Lançamentos.

## Regras iniciais

### Compra à vista no cartão
- gera uma única parcela
- associa ao próximo vencimento aplicável do cartão

### Compra parcelada
- divide o valor total pela quantidade de parcelas
- cria uma linha por parcela
- define vencimentos mensais subsequentes

### Limite disponível
- deve ser reduzido pelo valor total da compra no momento do lançamento
- deve ser recomposto conforme parcelas sejam efetivamente pagas, em regra futura

## Regras de data

A lógica precisa considerar:
- dia da compra
- dia de fechamento do cartão
- dia de vencimento do cartão

### Regra simplificada inicial
- se a compra ocorrer antes ou no fechamento, primeira parcela vai para a próxima fatura
- se ocorrer após o fechamento, primeira parcela vai para a fatura do mês seguinte

## Integrações futuras

Depois da geração das parcelas, o sistema poderá:
- criar contas a pagar correspondentes
- gerar lançamentos quando a fatura for quitada
- conciliar pagamentos bancários com fatura/cartão

## Limitações desta primeira etapa

Nesta fase, o foco é estruturar a engine.
Ainda não estamos cobrindo:
- estorno
- juros
- IOF
- parcelamento com entrada
- múltiplos cartões na mesma compra
- fechamento excepcional

## Próximo passo técnico

Criar um módulo local no Nofix para:
- receber a compra
- calcular parcelas
- produzir estrutura padronizada de saída
