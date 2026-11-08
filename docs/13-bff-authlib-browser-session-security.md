# Backend-for-Frontend (BFF)

> **In one sentence:** A BFF allows a browser to use an application session while OAuth tokens stay in a backend.

## Explain it simply

The backend uses an OAuth/OIDC client library such as Authlib to handle the authorization code exchange and manage credentials. Browser requests use a Secure, HttpOnly, appropriately SameSite session cookie. Backend forwards authorized API requests.

## How it works

Protect against CSRF, session fixation, open redirects and token leakage; implement expiry, revocation, and logout. Authlib does not automatically guarantee server-side token storage.

## Simple classroom example

Imagine a student using `lesson-app`, a registered application in the fictional `school-lab` realm, to reach `notes-api`. Identify which participant is the user, client, identity provider, and API. Use fake identifiers only.

## Common mistake / security warning

In a BFF, the browser normally does not send OAuth access tokens directly to the API.

## Remember

undefined

## Quick self-check

1. Can you explain this concept to someone who has never built a login system?
2. What role does `notes-api` play?
3. Which failure should a secure implementation detect?

## Learn more

- [Authoritative technical reference](https://www.ietf.org/archive/id/draft-ietf-oauth-browser-based-apps-25.html)
- [Related learning chapters](../book/README.md)

> This is introductory education, not a deployment checklist. Confirm product-version-dependent behavior and current standards before implementing a production system.
