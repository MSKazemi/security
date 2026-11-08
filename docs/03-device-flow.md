# Device Authorization Flow

> **In one sentence:** A device can let you sign in using another device with a browser.

## Explain it simply

The CLI requests a device_code and a user_code. The user visits the verification URL and enters the user_code. The CLI polls the token endpoint with the device_code until the user finishes or authorization expires.

## How it works

Respect polling intervals and slow_down responses. Never treat a user_code as an access token.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

Two codes have different roles: a user-facing code for confirmation and a device code for polling.

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
