# JWT vs JWK vs JWKS

> **In one sentence:** JWT is a token format; JWK is a JSON key; JWKS is a collection of public keys.

## Explain it simply

An API checks a signed JWT using appropriate public keys from the issuer's trusted JWKS endpoint and selects an allowed key by key identifier and policy.

## How it works

Never trust an attacker-supplied key URL or arbitrary algorithm in the JWT header. Verify issuer and audience after signature checks.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

JWKS contains verification keys, not the access token itself.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://www.rfc-editor.org/rfc/rfc7517)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
