# Realm, client, user, and client scope

> **In one sentence:** Keycloak has different objects for identity and application settings.

## Explain it simply

Realm: a managed authentication boundary. User: an identity. Client: a registration of an application. Client scope: a reusable set of scope mappings and protocol mappers.

## How it works

A Keycloak client is not the same as a user, nor is a client scope identical to a user role.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Use one fictional realm (school-lab), one client (lesson-app), and one API (notes-api) to study the hierarchy.

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
