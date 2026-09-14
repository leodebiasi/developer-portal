---
name: onz-baas-onboarding
description: Onboarding BaaS na Banking API (contas, pessoas, credenciais Pix, fee rules). Use when opening accounts as a BaaS partner or configuring pix-manager credentials.
---

# Banking API / BaaS

Credencial criada no **CORE** (Administração > API do Core): `client_id`, `client_secret`, certificado mTLS (365 dias), allowlist de IP.

Token: `POST /auth/token` (não é `/oauth/token` da API de Contas).

`x-account-id` identifica a conta filha nas chamadas BaaS.

## Jornadas

1. Getting started: `/banking/getting-started`
2. Auth & mTLS: `/banking/auth-and-mtls`
3. Onboarding de pessoa/conta: `/banking/onboarding-journey`
4. Saldo: `/banking/balance-flow`
5. Credenciais QRCodes da conta filha: `/banking/pix-manager-credentials-journey`

Gerenciamento: accounts, people, baas, fee-rules, baas-users.

OpenAPI: `/api-reference/banking`.

O host vem da credencial no CORE. Exemplos da POC usam `https://secureapi.onz.finance` **sem** `/api/v2`. Token: `POST /auth/token`.
