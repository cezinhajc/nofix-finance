# Nofix Finance, Preenchimento automático de relações no Notion

## Objetivo

Usar as relações nativas recém-criadas para conectar automaticamente os registros do fluxo de cartão.

## Ligações desejadas no processamento

### Ao processar compra
- compra aponta para o cartão usado
- compra aponta para parcelas geradas
- parcela aponta para a compra

### Ao gerar contas a pagar
- parcela aponta para a conta a pagar criada
- conta a pagar aponta para a parcela

## Resultado esperado

- navegação completa entre os objetos
- maior integridade do fluxo
- base pronta para dashboards e automações futuras
