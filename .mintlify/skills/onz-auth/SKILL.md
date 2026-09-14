---
name: onz-auth
description: Autentica nas APIs ONZ com mTLS e OAuth 2.0 client_credentials. Use when obtaining tokens, configuring certificates, or calling any ONZ API.
---

# Autenticação ONZ

Não execute pagamentos. Apenas oriente o desenvolvedor a autenticar.

## Regras

- Toda chamada exige **mTLS** (certificado cliente `.crt` + `.key` ou PFX) **e** `Authorization: Bearer <token>`.
- IPs de origem precisam estar na allowlist da credencial.
- Playground do browser **não funciona** (não envia mTLS). Use `curl`, Bruno ou Postman.
- Não invente hosts. Nunca `api.example.com`.

## Hosts

| Produto | Token | API |
| --- | --- | --- |
| Contas | `POST https://secureapi.onz.finance/api/v2/oauth/token` | `https://secureapi.onz.finance/api/v2` |
| QRCodes | `POST https://pix.onz.finance/oauth/token` | `https://pix.onz.finance` |
| Banking API | `POST /auth/token` no host da credencial CORE | `https://secureapi.onz.finance` (POC, sem `/api/v2`) |

Grant: `client_credentials`. Body `application/x-www-form-urlencoded`: `client_id`, `client_secret`, `grant_type=client_credentials`.

Token de Contas traz `expires_at`. Token de QRCodes traz `expires_in` (segundos, tipicamente 300) e `scope` contendo `qrcodes`.

## Headers

- `Authorization: Bearer <access_token>`
- `x-account-id` **somente** em contas BaaS (credencial filha). Não enviar em Pix/QRCodes de parceiro tradicional.

## Fluxo

1. Parceiro recebe certificado compactado da equipe de integração (ou o CORE gera o certificado na Banking API).
2. Configurar mTLS no cliente HTTP.
3. Obter token no host do produto.
4. Cachear o JWT até perto do expiry; renovar com a mesma grant. Não pedir token a cada request.
5. Chamar o recurso protegido.

Detalhes: `/getting-started/autenticacao`, `/getting-started/perguntas-frequentes`, `/qrcodes/autenticacao-api-pix`, `/contas/autenticacao-api-contas`, `/banking/auth-and-mtls`.
