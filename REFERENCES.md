# Official technical references

These are pointers to **authoritative specifications and provider documentation**. Verify currently applicable errata and version-specific changes before implementing security-critical systems.

## OAuth 2.0, OpenID Connect and tokens

- [RFC 6749 — OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 6750 — OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- [RFC 7636 — PKCE](https://www.rfc-editor.org/rfc/rfc7636)
- [RFC 7662 — OAuth 2.0 Token Introspection](https://www.rfc-editor.org/rfc/rfc7662)
- [RFC 8252 — OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252)
- [RFC 8628 — Device Authorization Grant](https://www.rfc-editor.org/rfc/rfc8628)
- [RFC 8705 — OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 9700 — OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)
- [RFC 10017 — OAuth 2.0 for Browser-Based Applications](https://www.rfc-editor.org/rfc/rfc10017)
- [RFC 10027 — Security of Cross-Device Flows](https://www.rfc-editor.org/rfc/rfc10027)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)

## JWT and JSON Web Keys

- [RFC 7515 — JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC 7516 — JSON Web Encryption](https://www.rfc-editor.org/rfc/rfc7516)
- [RFC 7517 — JSON Web Key / JWK Set](https://www.rfc-editor.org/rfc/rfc7517)
- [RFC 7519 — JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 8725 — JWT Security Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)
- [RFC 9068 — JWT Profile for OAuth 2.0 Access Tokens](https://www.rfc-editor.org/rfc/rfc9068)

## Implementations and web infrastructure

- [Keycloak documentation](https://www.keycloak.org/documentation)
- [Keycloak OIDC endpoint documentation](https://www.keycloak.org/securing-apps/oidc-layers)
- [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [Authlib documentation](https://docs.authlib.org/)
- [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)

**Technical note:** RFC 9068 specifies a **particular** access-token JWT profile, not the representation of every Keycloak JWT. RFC 9449 DPoP sender constraint is not automatically enabled by ordinary JWT signing.


## Browser OAuth, identity deployment and caching references

- [Authlib — OAuth Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/)
- [Starlette SessionMiddleware — signed, browser-readable cookies](https://www.starlette.io/middleware/#sessionmiddleware)
- [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter)
- [Keycloak hostname v2 and reverse-proxy URLs](https://www.keycloak.org/server/hostname)
- [Keycloak realm import and export](https://www.keycloak.org/server/importExport)
- [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts)
- [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
- [MDN Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)

**Reminder:** Starlette signed client-side session data is *readable*, not an encrypted server-side token store. A full OAuth BFF protects tokens and mediates API requests; see RFC 10017.
