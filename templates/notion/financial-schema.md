# Nofix Finance, Template Inicial de Databases no Notion

## Bases iniciais

### 1. Entidades
Finalidade: separar pessoa física, empresa ou unidade operacional.

Propriedades:
- Nome (title)
- Tipo (select: Pessoa, Empresa, Unidade)
- Status (select: Ativa, Inativa)
- Moeda (select)
- Timezone (rich_text)
- Observações (rich_text)

Seeds iniciais do piloto:
- Julio
- Simpia

### 2. Lançamentos
Finalidade: base central do financeiro.

Propriedades:
- Descrição (title)
- Entidade (relation -> Entidades)
- Tipo (select: Receita, Despesa, Transferência, Ajuste)
- Status (select: Previsto, Pago, Recebido, Conciliado, Cancelado)
- Valor (number)
- Data de competência (date)
- Data de vencimento (date)
- Data de liquidação (date)
- Conta bancária (relation -> Contas Bancárias)
- Categoria (relation -> Categorias)
- Cliente/Projeto (relation -> Clientes/Projetos)
- Centro de custo (rich_text)
- Forma de pagamento (select: Pix, TED, Boleto, Cartão, Dinheiro, Outro)
- Origem (select: Manual, Banco, Sistema, Cartão)
- ID transação bancária (rich_text)
- Conciliado? (checkbox)
- Observações (rich_text)

### 3. Contas Bancárias
Finalidade: cadastro de contas por entidade.

Propriedades:
- Nome da conta (title)
- Entidade (relation -> Entidades)
- Banco (rich_text)
- Tipo (select: Corrente, Poupança, Pagamento, Cartão)
- Saldo inicial (number)
- Saldo atual (number)
- Ativa? (checkbox)
- Provider (select: Pierre, Outro)
- Account ID externo (rich_text)
- Observações (rich_text)

### 4. Categorias
Finalidade: classificação financeira.

Propriedades:
- Nome (title)
- Entidade (relation -> Entidades)
- Tipo (select: Receita, Despesa)
- Categoria pai (rich_text)
- Ativa? (checkbox)
- Observações (rich_text)

Seeds iniciais do piloto:
- Julio: Moradia, Alimentação, Transporte, Saúde, Lazer, Receitas Pessoais
- Simpia: Receita de Projetos, Ferramentas, Parceiros, Impostos, Administrativo, Marketing

### 5. Clientes/Projetos
Finalidade: associar receitas e despesas da operação.

Propriedades:
- Nome (title)
- Entidade (relation -> Entidades)
- Tipo (select: Cliente, Projeto)
- Status (select: Ativo, Pausado, Encerrado)
- Cliente principal (rich_text)
- Valor previsto (number)
- Início (date)
- Fim (date)
- Observações (rich_text)

Seeds iniciais do piloto:
- Hospital Cirurgia
- Clínica Silhouette Estética Avançada
