---
name: onz-pix-pay
description: Paga Pix, boleto e gerencia chaves pela API de Contas. Use when initiating Pix payments, listing keys, DICT stats, MED, or infractions.
---

# Pagamentos (API de Contas)

Host: `https://secureapi.onz.finance/api/v2`. Token: `POST /oauth/token`.

Não execute a transferência de fato. Monte o request correto e aponte o OpenAPI.

## Escopos típicos

`pix.read`, `pix.write`, `pix.create`, `account.read`, `transactions.read`, `infractions.*`, `webhook.*`.

## Pagamentos

Guia: `/contas/pagamentos`. Tipos comuns:

- Pix por chave
- Pix por dados bancários
- Pix QR Code
- Boleto

CPF/CNPJ e chave Pix: formatos em `/getting-started/assuntos-relacionados-pix`.

## Chaves e DICT

- Gerenciar chaves da conta: `/contas/chaves-pix` (`/accounts/keys`).
- Estatísticas DICT: `/contas/estatisticas-dict`.
- `GET /pix/keys/{key}` consulta o DICT; não lista as chaves da conta.

## MED e infrações

`/contas/med`, `/contas/infracoes`. Fila de saída: `/contas/fila-saida`.

## Webhooks

`/contas/webhook-api-contas`. IPs dinâmicos — identifique por header customizado. Eventos de invoice são outro tipo: `/contas/invoices/webhook`.

Referência: `/api-reference/contas`.
