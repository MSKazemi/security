# Teaching slide outlines

These are **content-first technical slide outlines** derived from the security course chapters. All 17 chapters have **draft** teaching outlines. They are source material for study, classrooms and future presentations, not a rendered deck.

Each slide specifies an educational objective, short visible text, a complete explanation, the diagram or example that makes it understandable, and traceable references. The slide outlines deliberately avoid brand-specific colors, logos, asset requirements, platform-specific copy, and private production notes.

## Available technical slide outlines

| Topic | Slides | Level | Related chapter |
| --- | ---: | --- | --- |
| [Learning roadmap: security foundations](00-learning-roadmap.md) | 12 | Beginner | [Learning roadmap](../docs/00-learning-roadmap.md) |
| [Keycloak fundamentals: identity, client and API](01-keycloak-fundamentals.md) | 12 | Beginner → intermediate | [Keycloak fundamentals](../docs/01-keycloak-fundamentals.md) |
| [Choosing OAuth and OIDC flows](02-authentication-flows.md) | 12 | Beginner → intermediate | [Grant selection](../docs/02-authentication-flows.md) |
| [Device Authorization Grant](03-device-flow.md) | 12 | Beginner → intermediate | [Device codes and polling](../docs/03-device-flow.md) |
| [How Keycloak issues JWTs](04-jwt-issuance.md) | 12 | Beginner → intermediate | [JWT issuance](../docs/04-jwt-issuance.md) |
| [JWT claims and protocol mappers](05-claims-and-mappers.md) | 12 | Beginner → intermediate | [Claims, roles, mappers](../docs/05-claims-and-mappers.md) |
| [API access-token validation](06-api-token-validation.md) | 12 | Beginner → intermediate | [API credential and authorization checks](../docs/06-api-token-validation.md) |
| [Bearer tokens and HTTP authentication](07-bearer-token.md) | 12 | Beginner → intermediate | [Bearer credential usage](../docs/07-bearer-token.md) |
| [Realm, User, Client and Client Scope](08-realm-client-user-client-scope.md) | 12 | Beginner → intermediate | [Keycloak object model](../docs/08-realm-client-user-client-scope.md) |
| [OAuth 2.0 vs OIDC vs Keycloak](09-oauth-oidc-keycloak.md) | 12 | Beginner → intermediate | [OAuth/OIDC/Keycloak](../docs/09-oauth2-oidc-keycloak-relationship.md) |
| [PKCE: Verifier, Challenge and S256](10-pkce-generation.md) | 12 | Beginner → intermediate | [PKCE mechanics](../docs/10-pkce-generation.md) |
| [Authorization Code vs Access Token](11-authorization-code-vs-access-token.md) | 12 | Beginner → intermediate | [Code versus access token](../docs/11-authorization-code-vs-access-token.md) |
| [Keycloak deployment and stable identity](12-keycloak-deployment-identity-and-sessions.md) | 12 | Intermediate | [Issuer, HTTPS, persistence and sessions](../docs/12-keycloak-deployment-identity-and-sessions.md) |
| [FastAPI/Authlib full BFF security](13-bff-authlib-browser-session-security.md) | 12 | Intermediate → advanced | [BFF, cookies, CSRF, refresh and logout](../docs/13-bff-authlib-browser-session-security.md) |
| [keycloak-js browser adapter](14-keycloak-js-browser-adapter.md) | 12 | Beginner → intermediate | [Browser OAuth/OIDC client](../docs/14-keycloak-js-browser-adapter.md) |
| [JWT vs JWK vs JWKS](15-jwt-vs-jwks-verification.md) | 12 | Beginner → intermediate | [JWT/JWKS verification](../docs/15-jwt-vs-jwks-verification.md) |
| [CDN, HTTP cache and protected sessions](16-cdn-vs-cache-keycloak-assets.md) | 12 | Beginner → intermediate | [Static assets, JWKS and session stores](../docs/16-cdn-vs-cache-keycloak-assets.md) |

## Common structure

1. **Learning objective:** one thing a student should understand after the slide.
2. **On-slide text:** a concise headline and a few technically correct points; not a transcript.
3. **Teaching explanation:** fuller context for a reader or instructor; it must stand alone.
4. **Diagram or example:** a semantic explanation or link to a safe Mermaid diagram already documented in the chapter.
5. **Check and source:** question or important caveat, plus the exact chapter section or authoritative specification.

Treat chapter documents as the source of truth. Revise a chapter first if you discover a factual inconsistency, and then synchronize its slides. A slide is complete only when its technical claims and examples agree with the chapter and authoritative references.

## How to study

Read one slide's **On-slide text**, try to explain it in your own words, then open **Teaching explanation** and answer the **Self-check** question. After the outline, use the linked chapter and practical lab for deeper study.

**Privacy rule:** Only independent, generic technical education belongs here. Never include customer or organizational details, real accounts, secrets, internal discussions, scripts for publishing, social-platform tactics, animation prompts, or agent instructions.
