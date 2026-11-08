# Authorization code vs access token

> **In one sentence:** The authorization code is exchanged; the access token is presented to an API.

## Explain it simply

The authorization server redirects the browser back to a client with a short-lived, one-use code. The client exchanges that code at the token endpoint; it subsequently sends the access token to the API.

## How it works

A code is not itself an API bearer credential. Do not put access tokens in query strings.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

A successful code exchange does not prove the caller has every API permission.

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
