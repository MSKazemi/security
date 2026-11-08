# CDN, cache, and session

> **In one sentence:** Static asset caching is different from the storage of login credentials.

## Explain it simply

A CDN delivers files near users; a browser cache may reuse HTTP responses; a server-side session store maintains application login state. These have separate security and expiry rules.

## How it works

Do not confuse caching a JavaScript library with safely storing OAuth tokens. Never cache sensitive token responses in shared caches.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Cache-Control determines response caching behavior; it does not decide authorization.

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
