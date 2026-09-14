---
name: onz-invoices
description: Emite cobranças Pix, boleto ou híbridas pela API de Contas (invoices). Use when creating invoices, customers, or INVOICE webhooks — not Bacen cob/cobv.
---

# Invoices (API de Contas)

Emissão de cobrança **Pix, boleto ou híbrida** pela API de Contas. Não é a API Pix Bacen (`/cob`).

Host: `https://secureapi.onz.finance/api/v2`.

## Fluxo

1. mTLS + token (`/contas/autenticacao-api-contas`).
2. Cadastre o pagador em `/customers` (`/contas/invoices/pagadores`).
3. `POST /invoices` com `type`:
   - `IMMEDIATE` — já registra.
   - `SCHEDULED` — cria `DRAFT`; emita com `POST /invoices/{invoiceId}/emit`. `dueDate` não pode ser anterior a hoje.
4. Entregue o payload (QR / linha digitável) ao pagador.
5. Acompanhe `GET /invoices/{invoiceId}` ou webhook `INVOICE`.
6. Cancele com `DELETE /invoices/{invoiceId}`.

## Webhook

Tipo `invoice` em `/webhooks/invoice`. Documento do pagador chega mascarado. Deduplicação: `invoice-{invoiceId}`.

Guias: `/contas/invoices/jornada`, `/contas/invoices/cobrancas`, `/contas/invoices/webhook`.
OpenAPI: `/api-reference/contas`.
