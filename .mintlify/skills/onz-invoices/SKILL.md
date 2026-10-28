---
name: onz-invoices
description: Emite cobranças Pix, boleto ou híbridas pela API de Contas (invoices). Use when creating invoices, customers, or INVOICE webhooks — not Bacen cob/cobv.
---

# Invoices (API de Contas)

Emissão de cobrança **Pix, boleto ou híbrida** pela API de Contas. Não é a API Pix Bacen (`/cob`).

Host: `https://secureapi.onz.finance/api/v2`.

## Fluxo

1. mTLS + token (`/contas/autenticacao-api-contas`).
2. Informe exatamente uma opção no pedido: `customerId` de `/customers` ou os dados do pagador em `payer`.
3. `POST /invoices` com `type`:
   - `IMMEDIATE` — já registra.
   - `SCHEDULED` — cria `DRAFT`; para boleto ou híbrida, envie `emit: true` ou emita depois com `POST /invoices/{invoiceId}/emit`. `dueDate` não pode ser anterior a hoje.
4. Entregue o payload (QR / linha digitável) ao pagador.
5. Obtenha o documento com `GET /invoices/{invoiceId}/pdf` quando a cobrança estiver disponível para impressão.
6. Acompanhe `GET /invoices/{invoiceId}`, `GET /invoices` com filtros de status/período ou webhook `INVOICE`.
7. Cancele com `DELETE /invoices/{invoiceId}`.

## Listagem

`GET /invoices` aceita `status`, `dateField` (`CREATED_AT`, `DUE_DATE` ou `PAID_AT`), `startDate` e `endDate`. As duas datas são obrigatórias em conjunto. `WRITTEN_OFF` filtra cobranças pagas por outro canal.

## Webhook

Tipo `invoice` em `/webhooks/invoice`. Documento do pagador chega mascarado. Deduplicação: `invoice-{invoiceId}`.

Guias: `/contas/invoices/jornada`, `/contas/invoices/cobrancas`, `/contas/invoices/webhook`.
OpenAPI: `/api-reference/contas`.
