# Nofix Finance

Nofix Finance é um sistema financeiro operacional com base no Notion, integrado a Open Finance para conciliação bancária, automações e dashboards.

## Visão do projeto

O Nofix nasce como um produto replicável por cliente.

Ele deve permitir:
- operação financeira no Notion
- integração com bancos via Open Finance
- conciliação bancária
- dashboards financeiros
- setup guiado para novas implantações

## Princípios

- separação clara entre regra de negócio e integrações
- setup replicável por cliente
- Notion como camada operacional inicial, não como dependência eterna
- arquitetura preparada para múltiplas implantações

## Estrutura inicial

```bash
nofix-finance/
  apps/
    api/
    dashboard/
    worker/
  packages/
    core/
    notion/
    banking/
    reconciliation/
    setup/
    shared/
  templates/
    notion/
    seeds/
  docs/
    architecture/
    product/
    setup/
  scripts/
```

## MVP proposto

### Fase 1
- modelagem financeira base
- setup guiado por cliente
- estrutura de databases no Notion
- integração com provider bancário
- conciliação bancária básica

### Fase 2
- dashboard financeiro
- alertas
- fluxo de caixa
- contas a pagar e receber

### Fase 3
- regras avançadas de conciliação
- automações por cliente
- multi-instância mais robusta

## Casos de uso

- financeiro pessoal
- financeiro de pequenas empresas
- operação financeira para clientes
- conciliação de contas bancárias
- organização financeira com dashboard gerencial

## Conceito de implantação

Cada cliente terá um setup próprio com perguntas como:
- nome do cliente
- timezone
- moeda
- token do Notion
- page ID ou database IDs
- provider bancário
- API key do provider
- entidades financeiras
- categorias iniciais
- centros de custo

## Próximos passos

1. formalizar arquitetura v1
2. definir template de Notion
3. definir fluxo de setup
4. implementar clients/config
5. iniciar integração Notion
6. iniciar integração bancária
