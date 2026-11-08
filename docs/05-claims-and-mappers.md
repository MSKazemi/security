# JWT claims and mappers

> **In one sentence:** Claims are facts or attributes represented in a token.

## Explain it simply

A token may include issuer (iss), subject (sub), audience (aud), expiry (exp), scopes, and roles. Keycloak protocol mappers and client-scope settings control many emitted claims.

## How it works

Claim presence does not automatically grant application access. The API applies its authorization policy.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Scope, client scope, and role are related but different concepts.

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
