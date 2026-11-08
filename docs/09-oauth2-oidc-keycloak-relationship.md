# OAuth 2.0, OIDC, and Keycloak

> **In one sentence:** OAuth 2.0 is an authorization framework; OIDC adds a standard identity layer; Keycloak implements both.

## Explain it simply

OAuth access tokens are for protected resources. OIDC introduces the ID token, used by the client to learn about authentication. Keycloak acts as an authorization server and OIDC provider.

## How it works

Authentication often occurs during an OAuth/OIDC flow, but authentication and API authorization are separate judgments.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

An ID token is not a substitute for an API access token.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://openid.net/specs/openid-connect-core-1_0.html)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
