# Versionamento do Nofix Finance

## Objetivo

Criar um modelo simples de versionamento para que fique claro no GitHub o que mudou em cada versão.

## Padrão adotado

Usar versão no formato:
- `MAJOR.MINOR.PATCH`

Exemplo:
- `1.0.1`

## Regra de leitura

### MAJOR
Mudança grande:
- quebra de estrutura
- nova fase do produto
- alteração importante de arquitetura

Exemplo:
- `1.0.0` → `2.0.0`

### MINOR
Nova funcionalidade ou melhoria relevante sem quebrar o funcionamento anterior.

Exemplos:
- nova integração
- nova tela operacional
- melhoria de arquitetura funcional
- evolução importante de design do produto

Exemplo:
- `1.0.0` → `1.1.0`

### PATCH
Ajustes menores e incrementais.

Exemplos:
- correção de bug
- pequenos refinamentos
- melhorias simples
- ajuste de consolidação

Exemplo:
- `1.0.0` → `1.0.1`

## Categorias de mudança

Toda versão deve registrar uma ou mais categorias:
- `feat` = nova funcionalidade
- `fix` = correção de bug
- `design` = melhoria de arquitetura, design de fluxo ou organização estrutural
- `docs` = documentação
- `infra` = automação, scripts, publicação, setup

## Arquivos recomendados

### CHANGELOG.md
Arquivo principal com histórico das versões.

### RELEASES.md (opcional futuro)
Resumo mais executivo das entregas por versão.

## Modelo de anotação no changelog

```markdown
## [1.0.1] - 2026-04-26
### fix
- corrigida a consolidação das compras XP com o cartão correto

### design
- refinada a modelagem da página Cartões

### docs
- documentada a separação entre segundo-cérebro e produto Nofix
```

## Recomendação prática

- usar `MINOR` para entregas que o usuário percebe como nova capacidade
- usar `PATCH` para correções e refinamentos
- fazer tag de versão no GitHub quando a mudança estiver estável
