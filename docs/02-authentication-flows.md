# Choosing login flows

> **In one sentence:** Different devices and applications use different OAuth grant types.

## Explain it simply

An interactive browser or mobile app commonly uses Authorization Code with PKCE. A TV or CLI without a convenient browser can use Device Authorization. A service can use Client Credentials when no end user is signing in.

## How it works

Password grant exposes the user's password to the client and is not a recommended design for new applications.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Do not confuse a grant type with a user's permissions.

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
