# How JWTs are issued

> **In one sentence:** A JWT is a container of claims that may be cryptographically signed.

## Explain it simply

After the applicable authentication and grant checks, an authorization server assembles claims such as iss, sub, aud, iat, and exp, then signs the token with a configured signing key.

## How it works

A signed JWT is not necessarily encrypted. Validate it before trusting any claims.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

The three dot-separated Base64URL segments typically represent a JWS header, payload, and signature.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://www.rfc-editor.org/rfc/rfc7519)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
