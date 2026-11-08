# Learning roadmap

> **In one sentence:** Begin with identity, permissions, tokens, then inspect complete flows.

## Explain it simply

Authentication answers who is signing in; authorization decides what that identity may access.

## How it works

Study in order: authentication vs authorization; OAuth 2.0 and OIDC; Keycloak realms and clients; authorization code and PKCE; access/ID/refresh tokens; JWT claims and JWKS; audience validation; Device Flow; BFF and sessions.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Draw the browser, app, identity provider, and API. Trace each credential between them.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://www.rfc-editor.org/rfc/rfc6749)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
