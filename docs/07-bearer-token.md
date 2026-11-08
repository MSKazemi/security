# Bearer tokens

> **In one sentence:** A bearer token works like a ticket: possession is sufficient to present it.

## Explain it simply

An HTTP caller typically sends an access token in the Authorization: Bearer header. TLS, limited privileges, short lifetime, and safe storage reduce theft risks.

## How it works

Never publish a real bearer token, including in examples, screenshots, logs, or shell history.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Bearer is a presentation scheme, not a special JWT encoding.

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
