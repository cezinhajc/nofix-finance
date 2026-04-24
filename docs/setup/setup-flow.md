# Setup Flow Inicial do Nofix Finance

## Objetivo

Permitir a implantação do Nofix para um novo cliente com um fluxo guiado e repetível.

## Etapas do setup

### 1. Identificação do cliente
Perguntas:
- nome do cliente
- slug do projeto
- timezone
- moeda

### 2. Modelo financeiro
Perguntas:
- entidades financeiras
- usa contas a pagar?
- usa contas a receber?
- usa cartões?
- usa centros de custo?
- usa projetos/clientes?

### 3. Notion
Perguntas:
- token da integração
- page ID principal
- criar databases novas ou conectar existentes?
- nomes das databases

### 4. Bancos / Open Finance
Perguntas:
- provider escolhido
- API key
- ambiente
- sincronização manual ou automática?

### 5. Estrutura inicial
Perguntas:
- categorias iniciais
- contas bancárias iniciais
- centros de custo iniciais
- projetos/clientes iniciais

## Saídas esperadas

Ao final do setup, o sistema deve ser capaz de:
- gerar arquivo de configuração local
- validar credenciais
- registrar entidades
- preparar estrutura inicial do cliente
- deixar a implantação pronta para uso

## Observações

Segredos nunca devem ser commitados.

O setup deve gerar exemplos e arquivos locais como:
- .env.local
- client.config.json
- seeds iniciais
