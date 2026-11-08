# Validating an API token

> **In one sentence:** An API must not trust a token simply because it looks like a JWT.

## Explain it simply

Check the expected token type/purpose, permitted signature algorithm and signature, trusted issuer, intended audience, expiry and other time constraints, then enforce the API's required scopes or roles and object-level permissions.

## How it works

Reject ID tokens presented as API bearer access tokens. A signed token for some other API is still the wrong credential.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

A 401 typically signals missing/invalid authentication; a 403 indicates valid credentials lacking permission.

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
