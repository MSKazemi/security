# keycloak-js browser adapter

> **In one sentence:** keycloak-js is a JavaScript library that helps browser applications interact with Keycloak.

## Explain it simply

It can start interactive login, manage browser-side authentication state, and use Authorization Code with PKCE. The registered Keycloak client still describes the application but does not host its JavaScript.

## How it works

Avoid exposing secrets in browser apps. Browser contexts and cookie restrictions affect behavior; use secure HTTPS deployments.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

A browser public client and a confidential BFF are different architectures.

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
