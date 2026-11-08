# Keycloak fundamentals

> **In one sentence:** Keycloak is an identity and access management server that can authenticate users and issue tokens.

## Explain it simply

A realm is a security boundary, a user is an account, and a client is an application registered to use Keycloak.

## How it works

The application runs separately; its Keycloak client registration stores allowed redirect URIs, permitted flows, scope settings, and authentication configuration. A resource server is the API enforcing access decisions.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

A Keycloak client registration is not an application process running inside Keycloak.

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
