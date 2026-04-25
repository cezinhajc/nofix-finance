# Nofix Finance, Processamento de Compras Reais v2

## Objetivo

Evoluir o processamento de compras no cartão para:
- marcar compras já processadas
- identificar o cartão específico da compra

## Ajustes necessários no Notion

### Base Compras no Cartão
Adicionar campos operacionais:
- Cartão (identificação textual inicial ou relação futura)
- Processada? (checkbox)
- Purchase Key (rich_text)

## Regras

### Marcação de processamento
Ao concluir o processamento com sucesso:
- marcar Processada? = true
- gravar Purchase Key

### Cartão específico
Na versão atual:
- identificar cartão por nome textual informado na compra
- se estiver vazio, usar fallback configurado

## Evolução futura

- trocar identificação textual por relação nativa
- impedir processamento se cartão estiver ausente ou inválido
