# PKCE: verifier and challenge

> **In one sentence:** PKCE helps protect the authorization-code exchange.

## Explain it simply

The client creates a fresh high-entropy code_verifier and sends an S256 code_challenge during authorization. At the token endpoint, it sends the original verifier. The server checks that SHA256(verifier), Base64URL-encoded, matches the stored challenge.

## How it works

Use S256, HTTPS, an exact registered redirect URI, and state and/or OIDC nonce as appropriate. PKCE does not replace all protections.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Never put the verifier in the initial authorization request.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://www.rfc-editor.org/rfc/rfc7636)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
