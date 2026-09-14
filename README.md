# ONZ Developers (POC Mintlify)

POC do portal de desenvolvedores em [Mintlify](https://mintlify.com), migrado de [developers.onz.software](https://developers.onz.software) (Docusaurus + Redocusaurus).

O conteúdo de produção **continua** no portal atual até a POC ser avaliada.

## O que esta POC cobre

- Guias em MDX (primeiros passos, QRCodes, Contas, Banking, CloudPix, SPB, Onboarding, Cash)
- OpenAPI em `openapi/` com overlays de `servers` reais (sem `api.example.com`)
- Skills em `.mintlify/skills/` (`onz-auth`, `onz-qrcodes`, `onz-pix-pay`, `onz-invoices`, `onz-baas-onboarding`)
- Navegação por produto em `docs.json`

Mintlify gera `llms.txt`, páginas `.md` e MCP a partir deste repo.

## Preview local

```bash
npm i -g mint
mint dev
```

Abre em `http://localhost:3000`.

```bash
mint validate
```

## Publicar

Instale o GitHub App da Mintlify no dashboard e faça push em `main`. O domínio da POC fica no dashboard (não substitui `developers.onz.software` por enquanto).

## Fonte

Markdown e specs vieram de `developers.onz.software`. O script `scripts/migrate.py` foi o conversor one-shot e **não deve ser reexecutado** — as páginas de índice, overlays e hosts foram ajustados depois da conversão.
