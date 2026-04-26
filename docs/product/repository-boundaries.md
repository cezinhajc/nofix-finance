# Limites de repositório e contexto do Nofix

## Estrutura correta

### Segundo cérebro / workspace principal
Este workspace representa o ambiente operacional amplo da Lurdes.

Aqui ficam:
- memória
- contexto do Julio
- contexto da Simpia
- outros projetos e frentes
- automações gerais da assistente

Este não é o repositório do produto Nofix.

### Nofix
O Nofix é um produto separado.

Definição:
- produto nascido a partir do contexto da Simpia
- mas com identidade própria
- potencial de virar SaaS
- repositório próprio no GitHub
- arquitetura própria
- roadmap próprio

## Regra operacional

- o workspace principal não deve apontar para o GitHub do Nofix como remoto padrão
- publicações do Nofix devem ocorrer de forma explícita e controlada
- usar subtree publish para enviar apenas `nofix-finance/` ao repositório do produto

## Objetivo dessa separação

Evitar mistura entre:
- memória e operação do segundo cérebro
- código e ativos do produto Nofix

## Publicação recomendada

Usar o script:
- `nofix-finance/scripts/publish_github.sh`

Esse fluxo publica apenas a pasta do produto para o repositório separado.
