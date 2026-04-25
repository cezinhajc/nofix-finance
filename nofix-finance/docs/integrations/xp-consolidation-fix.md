# Consolidação da integração XP no Nofix

## Problema identificado

As compras importadas da Pierre estavam chegando no Nofix, mas o processamento ainda podia cair no cartão padrão antigo, gerando inconsistência entre:
- cartão de origem da compra
- cartão usado no processamento
- consolidação da página Cartões

## Objetivo da correção

Garantir que compras importadas do XP Banking sejam:
- vinculadas ao cartão correto
- processadas com o cartão correto
- consolidadas corretamente na base Cartões

## Ajustes necessários

1. usar a relação nativa `Cartão Rel` na compra sempre que houver correspondência
2. priorizar `Cartão Rel` no processamento, antes de fallback textual
3. preencher `Cartão Rel` já na importação da Pierre
4. manter `Cartão` textual apenas como apoio visual

## Resultado esperado

- XP Banking passa a consolidar suas compras corretamente
- página do cartão pode exibir compras do próprio cartão
- processamento deixa de cair no Cartão Inter quando não deveria
