# Security, Explained Simply

An open, visual-first security course for learning **authentication, authorization, OAuth 2.0, OpenID Connect (OIDC), Keycloak, JWTs, and practical API security**.

For students, developers, and curious engineers. Start with plain language, then study diagrams, standards, and hands-on labs. All identities, hosts, and applications in this repository are fictional.

> **Principle:** Authentication asks *who are you?* Authorization asks *what may you do?* OAuth 2.0 delegates access; OIDC adds a standardized identity layer on top of OAuth 2.0; Keycloak is software that implements these protocols.

## Start learning

Start with the [learning roadmap](docs/00-learning-roadmap.md), explore the [slide outlines](slides/README.md), or consult the [plain-English glossary](docs/glossary.md).

**Teaching slides:** The [slide library](slides/README.md) has 12 detailed text-first outlines per chapter (204 slides total). These are teaching drafts, not rendered presentations.

### Chapters

| # | Topic |
|---|---|
| 00 | [Learning roadmap](docs/00-learning-roadmap.md) |
| 01 | [Keycloak fundamentals: realm, user, client, API](docs/01-keycloak-fundamentals.md) |
| 02 | [Authentication and authorization flows](docs/02-authentication-flows.md) |
| 03 | [Device Authorization Flow](docs/03-device-flow.md) |
| 04 | [How Keycloak issues JWTs](docs/04-jwt-issuance.md) |
| 05 | [JWT claims, mappers, and client scopes](docs/05-claims-and-mappers.md) |
| 06 | [How APIs validate access tokens](docs/06-api-token-validation.md) |
| 07 | [What Bearer tokens mean](docs/07-bearer-token.md) |
| 08 | [Realm vs client vs user vs client scope](docs/08-realm-client-user-client-scope.md) |
| 09 | [OAuth 2.0 vs OIDC vs Keycloak](docs/09-oauth2-oidc-keycloak-relationship.md) |
| 10 | [PKCE: verifier and challenge](docs/10-pkce-generation.md) |
| 11 | [Authorization code vs access token](docs/11-authorization-code-vs-access-token.md) |
| 12 | [Deployment security and identity stability](docs/12-keycloak-deployment-identity-and-sessions.md) |
| 13 | [Backend-for-Frontend: BFF and browser sessions](docs/13-bff-authlib-browser-session-security.md) |
| 14 | [keycloak-js browser adapter](docs/14-keycloak-js-browser-adapter.md) |
| 15 | [JWT vs JWK vs JWKS](docs/15-jwt-vs-jwks-verification.md) |
| 16 | [CDN vs browser cache vs application session](docs/16-cdn-vs-cache-keycloak-assets.md) |

## Learn by doing

- [Device Flow lab](labs/01-first-jwt-device-flow.md)
- [Generate a PKCE challenge with Python](labs/pkce_generate.py)
- [Self-check questions and answers](exercises/questions-and-answers.md)
- [Official specifications and documentation](REFERENCES.md)

## Safe examples, accurate explanations

- Never use a real password, token, secret, private key, personal account, or company infrastructure in examples.
- Validate access tokens at APIs: signature, issuer, audience, time validity, and authorization.
- Do **not** use ID tokens as API access tokens.
- Prefer Authorization Code with PKCE for interactive clients; the password grant is historical and discouraged.
- Example hostnames such as `https://login.example.test` are illustrative, not deployed services.
- Keycloak user-interface names can differ by version; verify configuration against official documentation.
- Explanations simplify complex systems; follow links to standards for production decisions.

## Contributing

Suggestions that improve clarity, sources, diagrams, or reproducible exercises are welcome. Please avoid uploading private operational context and secrets. Educational material is separated from internal planning and production assets.

This project is an independent educational resource and is not affiliated with Keycloak or its maintainers.
