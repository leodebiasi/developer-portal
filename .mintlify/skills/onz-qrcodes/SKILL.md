---
name: onz-qrcodes
description: Cria e consulta cobranças Pix (cob, cobv, rec) na API de QRCodes. Use when emitting Pix QR codes, Pix Automático, or consulting received Pix as PSP recebedor.
---

# QRCodes (PSP recebedor)

API Pix padronizada (Bacen). Host: `https://pix.onz.finance`.

## Não confundir

- **QRCodes** = `/cob`, `/cobv`, `/rec`, `/pix` (este produto).
- **Contas / invoices** = Pix, boleto ou híbrido emitidos pela API de Contas (`/invoices`). Jornada: `/contas/invoices/jornada`.

## Pré-requisitos

1. Credenciais `client_id` / `client_secret` / chave Pix. FAQ: `/getting-started/perguntas-frequentes`.
2. Certificado mTLS.
3. Token em `POST /oauth/token` com scope `qrcodes`.

## Jornadas

1. Autenticar → criar cobrança (`PUT /cob/{txid}` imediata ou `PUT /cobv/{txid}` com vencimento) → enviar QR / Pix copia-e-cola ao pagador → receber webhook → consultar Pix.
2. Pix Automático: quatro jornadas de autorização em `/qrcodes/pix-automatico-jornadas` (`/rec`, `/solicrec`, `/cobr`).

## Webhook

Configurar em `/webhook/{chave_pix}`. Não dependa de IP de origem (são dinâmicos); use header customizado.

Referência OpenAPI: `/api-reference/qrcodes`. Guias: `/qrcodes/jornada-cobranca`.
