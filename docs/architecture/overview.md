# Arquitetura v1 do Nofix Finance

## Objetivo

Criar uma base de produto financeiro replicável, com setup por cliente, usando Notion como operação inicial e integração bancária para conciliação.

## Direção arquitetural

O projeto deve ser organizado em camadas:

### Core
Contém as regras de negócio financeiras:
- entidades
- contas
- lançamentos
- categorias
- conciliação
- indicadores

### Integrações
Contém conectores externos:
- Notion
- providers bancários/Open Finance
- mensageria futura

### Aplicações
Camadas executáveis do sistema:
- API
- Worker de sincronização
- Dashboard

### Setup
Camada responsável por onboarding de novos clientes:
- perguntas interativas
- validação de credenciais
- geração de configuração
- provisionamento inicial

## Modelo de implantação

A versão inicial será single-tenant replicável.

Ou seja:
- uma instalação por cliente
- mesma base de código
- configuração específica por implantação
- possibilidade futura de evolução para multi-tenant

## Componentes esperados

### apps/api
API interna do sistema.

### apps/dashboard
Painel financeiro e operacional.

### apps/worker
Sincronização com bancos, Notion e rotinas de conciliação.

### packages/core
Regras de negócio.

### packages/notion
Mapeamento e operações no Notion.

### packages/banking
Integrações com Open Finance.

### packages/reconciliation
Engine de conciliação.

### packages/setup
Onboarding e provisionamento por cliente.

### packages/shared
Tipos, helpers e config compartilhada.

## Decisões iniciais

- nome formal do projeto: Nofix Finance
- nome curto do produto: Nofix
- primeiro provider bancário provável: Pierre
- primeiro piloto: Julio / Simpia
- foco inicial: separação entre pessoal e empresa

## Requisitos do setup

O setup deve permitir:
- cadastrar dados do cliente
- coletar tokens e IDs
- definir entidades financeiras
- gerar arquivo de configuração local
- preparar estrutura padrão do Notion
- validar integrações externas

## Evolução prevista

1. template operacional em Notion
2. sincronização bancária
3. conciliação básica
4. dashboard
5. regras avançadas
6. replicação rápida para novos clientes
