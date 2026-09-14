# ONZ Developers — instruções para agentes

Portal Mintlify das APIs ONZ Finance. Páginas em MDX, config em `docs.json`, specs em `openapi/`, overlays em `overlays/`, skills em `.mintlify/skills/`.

Instale o skill da Mintlify se for editar componentes: `npx skills add https://mintlify.com/docs`.

## Hosts (não invente)

| Produto | Host | Token |
| --- | --- | --- |
| Contas | `https://secureapi.onz.finance/api/v2` | `POST /oauth/token` |
| QRCodes | `https://pix.onz.finance` | `POST /oauth/token` |
| Banking API | host da credencial no CORE (POC: `https://secureapi.onz.finance`, sem `/api/v2`) | `POST /auth/token` |
| Onboarding | mesmo host da API de Contas | OAuth Contas |
| CloudPix | host sob demanda (`suporte@onz.software`) + PFX | header `ONZ-Token` |

Nunca use `api.example.com`, `api.qrcodes-h.sulcredi.coop.br` ou `api.bancodigital.com` em exemplos novos.

## Regras de produto

- Toda API pública exige **mTLS + OAuth client_credentials** e allowlist de IP. Playground do browser não envia certificado.
- `x-account-id` só em contas BaaS (credencial filha). Não enviar em Pix/QRCodes de parceiro tradicional.
- Cobrança Bacen (`/cob`, `/cobv`, `/rec`) = produto QRCodes. Cobrança Pix/boleto/híbrido = produto Contas (`/invoices`).
- Não invente endpoints. Use o OpenAPI do produto.

## Estilo

- Português brasileiro
- Segunda pessoa, frases curtas
- Sentence case nos títulos
- Código para paths, hosts, headers e scopes
