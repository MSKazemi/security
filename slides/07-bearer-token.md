# Teaching slides — Bearer tokens and OAuth API requests

**Audience:** beginners, students and software engineers.  
**Canonical technical source:** [Bearer tokens](../docs/07-bearer-token.md).  
**Format:** 12 detailed text-first slide outlines with neutral examples. No video, brand assets, animation or platform workflow.

---

## Slide 01 — What does Bearer mean?

**Learning objective:** Explain bearer possession without mistaking it for user authentication.

**On-slide text**

- Bearer = possession is sufficient for presentation
- API still validates credentials
- API still enforces resource permissions

**Teaching explanation:** A bearer token is a credential that a possessor can present without proving ownership of a separate cryptographic key. The issuer and resource server still restrict the token by time, audience, type, scopes and policy. The classroom analogy is a limited access pass: the guard can verify the pass but, solely from possession, cannot know the holder is the original recipient. This makes stolen bearer tokens sensitive.

**Diagram or worked example:** A student notebook pass and a separate validation/authorization gate, with analogy limits noted.

**Self-check:** Does Bearer mean anyone can read every notebook?  
**Answer:** No. A usable token must pass the API's checks and resource policy.

**Sources:** Chapter §1; RFC 6750. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 02 — Where is Bearer sent in HTTP?

**Learning objective:** Read the HTTP Authorization header correctly.

**On-slide text**

- Authorization is the HTTP header
- Bearer is the authentication scheme
- Token value follows after a space
- Use HTTPS

**Teaching explanation:** An OAuth client normally sends a Bearer access token in the Authorization HTTP header, as in Authorization: Bearer EXAMPLE_ACCESS_TOKEN_NOT_REAL. The example is a placeholder, not a working token. The scheme indicates the presentation method; it does not encrypt the token or change its claims. Require HTTPS and avoid putting credentials in query parameters, debugging output, screenshots or logs.

**Diagram or worked example:** Annotated fictional HTTP request from Chapter §2 with header, scheme and placeholder separately boxed.

**Self-check:** Is Bearer itself the token string?  
**Answer:** No, it is the authentication scheme before the token value.

**Sources:** Chapter §2; RFC 6750 §2.1. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 03 — Bearer versus JWT versus opaque token

**Learning objective:** Distinguish presentation scheme from token representation.

**On-slide text**

- Bearer = scheme and possession model
- JWT = possible claims format
- Opaque = another possible token format
- ID token is not API Bearer access

**Teaching explanation:** A bearer access token can be a signed JWT or an opaque string. The first can be validated locally using approved signing keys and claim rules; the second may be checked by trusted introspection. JWT is therefore not a synonym for Bearer. Conversely, a JWT can be an ID token intended for the OIDC client and not an access token for the API. Token purpose and audience still matter.

**Diagram or worked example:** Two-axis matrix: presentation scheme vs credential serialization, with permitted examples.

**Self-check:** Can an opaque access token be used with Bearer?  
**Answer:** Yes.

**Sources:** Chapter §3; RFC 6750; RFC 7519. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 04 — Trace the authorization-code flow

**Learning objective:** Follow how the client obtains and presents a Bearer access token.

**On-slide text**

- Keycloak authenticates Alice
- Client exchanges code and verifier at token endpoint
- Client receives access token with token_type Bearer
- Client calls intended API

**Teaching explanation:** In Authorization Code with PKCE, the OAuth client begins login and the browser follows redirects. After Keycloak authenticates Alice, the client's backend exchanges a short-lived code and PKCE verifier at the token endpoint. Keycloak may return an access token and token_type=Bearer. The backend then sends that access token to notes-api. A full BFF keeps the OAuth token on the backend and gives the browser a separate session cookie.

**Diagram or worked example:** Use Chapter §4 sequence diagram with code, token and cookie lanes distinct.

**Self-check:** Should notes-api receive the authorization code instead of access token?  
**Answer:** No.

**Sources:** Chapter §4; OAuth RFC 6749; PKCE RFC 7636. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 05 — What token_type tells the client

**Learning objective:** Interpret token response metadata without inventing a default lifetime.

**On-slide text**

- access_token is the issued credential
- token_type specifies presentation scheme
- expires_in gives configured access-token lifetime
- Refresh or ID tokens have separate purposes

**Teaching explanation:** An OAuth token response can return a value named access_token, token_type Bearer, and expires_in. These fields have different jobs. The client should use the indicated scheme and protect the token against disclosure. The sample lifetime of 300 seconds in a classroom response is illustrative rather than a universal Keycloak default. A real token response can include other credentials, but only an appropriate access token belongs at the protected API.

**Diagram or worked example:** Small token response JSON card with clear placeholder data; separate labels for value, scheme, and lifetime.

**Self-check:** Is token_type=Bearer proof that the token is valid for every API?  
**Answer:** No.

**Sources:** Chapter §5; RFC 6749 §5.1. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 06 — How the API validates Bearer

**Learning objective:** Locate signature/introspection, audience and authorization gates.

**On-slide text**

- JWT: verify with trusted keys and policy
- Opaque: use issuer-approved validation
- Check expiry, issuer, audience, token purpose
- Enforce concrete notebook permission

**Teaching explanation:** Presentation through the Authorization header is only the beginning. notes-api must validate that a token is genuinely issued by a trusted server, is intended for it, and is still valid. A JWT may be checked using a trusted issuer's JWKS; an opaque token may require authenticated introspection. Then current resource policy decides whether Alice may read a particular notebook. Signature validity alone is not universal authorization.

**Diagram or worked example:** Use Chapter §6 two-decision flow and the linked API validation chapter.

**Self-check:** Will a correctly signed token for billing-api work at notes-api?  
**Answer:** No, wrong audience.

**Sources:** Chapter §6; RFC 7662; RFC 8725. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 07 — 401, 403 and WWW-Authenticate

**Learning objective:** Explain how a resource responds to common Bearer failures.

**On-slide text**

- 401: absent or invalid credential
- WWW-Authenticate: Bearer challenge
- 403: valid token but insufficient permission
- insufficient_scope is an OAuth Bearer error

**Teaching explanation:** RFC 6750 defines Bearer challenges and error codes. A missing or invalid token generally produces 401 and a Bearer challenge, often with invalid_token for a provided bad token. A valid token lacking required scope commonly produces 403 and may include insufficient_scope. Object ownership denial is also typically 403. Avoid exposing full tokens, internal policy details or stack traces in error responses. Malformed requests can have other status codes.

**Diagram or worked example:** Table pairing absent, expired, insufficient scope and wrong notebook owner with HTTP outcomes.

**Self-check:** What is the typical status for a valid token denied by notebook policy?  
**Answer:** 403 Forbidden.

**Sources:** Chapter §7; RFC 6750 §3. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 08 — Why stolen Bearer tokens matter

**Learning objective:** Understand replay risk without giving attack instructions.

**On-slide text**

- A stolen usable token can be presented
- No separate possession key is required
- Audience, scope and expiry limit impact
- Protect storage and transport

**Teaching explanation:** An attacker possessing a stolen valid bearer access token can attempt requests without Alice's password. The API will still enforce audience, expiry and permissions, but the possession model itself does not prove original client identity. Defenses include TLS, safe backend or platform storage, least-privilege scopes, short lifetimes, minimizing token logging, XSS protections, revocation strategies and authorization checks for sensitive actions.

**Diagram or worked example:** Chapter §8 threat model with legitimate token holder and unauthorized possessor; both reach the same API checks.

**Self-check:** Does an attacker need Alice's password for every usable Bearer request?  
**Answer:** No.

**Sources:** Chapter §8; RFC 6750; RFC 9700. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 09 — Bearer versus sender-constrained tokens

**Learning objective:** Explain DPoP and mTLS as separate replay defenses.

**On-slide text**

- Bearer token alone is presentable
- DPoP adds signed possession proof
- OAuth mTLS binds to certificate/key
- These mechanisms are not automatic with Keycloak JWT signing

**Teaching explanation:** DPoP and mutual TLS offer sender constraint: use of a token requires proof associated with a bound key. DPoP uses a signed per-request proof JWT with values such as HTTP method and URL, while mutual TLS uses the relevant certificate/private-key proof. Their goals and deployment complexity differ from ordinary bearer tokens. A resource supporting DPoP must ensure bound tokens are not accepted under the Bearer scheme, preventing an authentication downgrade.

**Diagram or worked example:** Comparison table with bearer pass, DPoP-bound pass plus key proof, and mTLS-bound certificate proof.

**Self-check:** Can someone treat a DPoP-bound access token as ordinary Bearer?  
**Answer:** A compliant supporting API must reject that downgrade.

**Sources:** Chapter §9; RFC 9449; RFC 8705. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 10 — Limits of proof-of-possession

**Learning objective:** Avoid promising universal security from DPoP or mTLS.

**On-slide text**

- Key binding reduces stolen-token replay
- Client compromise can still enable misuse
- TLS remains required
- API resource policy remains essential

**Teaching explanation:** Sender-constrained tokens improve protection when an attacker obtains only the token string. However, malicious code running in the legitimate client context may be able to produce valid proofs while that context is compromised. A DPoP proof is not user authentication and does not authorize arbitrary resources; the API still validates the access token and specific permission. Teach the threat model, rather than presenting DPoP as a magic replacement for safe application design.

**Diagram or worked example:** Threat-model box: stolen token only versus compromised legitimate execution context.

**Self-check:** Does DPoP remove the need for API authorization checks?  
**Answer:** No.

**Sources:** Chapter §9; RFC 9449 §11. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 11 — How to demonstrate safely

**Learning objective:** Plan a no-secrets classroom exercise.

**On-slide text**

- Use disposable local authorization and API
- Use fake token placeholders in teaching
- Observe headers and status, never live values
- Test invalid, expired, wrong audience and denied resource

**Teaching explanation:** A classroom demonstration should show structure rather than expose credentials. The instructor can sketch Authorization: Bearer EXAMPLE_ACCESS_TOKEN_NOT_REAL and discuss what the API checks. If a local lab uses an actual temporary token, keep it out of screenshots, shell history, logs, chat and source control; secure the environment variable or secret store. Compare missing token, wrong audience, ID-token substitution and valid credential with insufficient resource permission.

**Diagram or worked example:** Diagram of safe local notes-api test matrix with secrets redacted.

**Self-check:** Should a real access token be pasted into a public JWT decoder for teaching?  
**Answer:** No.

**Sources:** Chapter §10; RFC 6750. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

## Slide 12 — Bearer's core lesson

**Learning objective:** Summarize responsibilities and common confusions.

**On-slide text**

- Issuer grants a limited credential
- Client protects and presents it
- API validates audience and purpose
- API checks exact action and resource

**Teaching explanation:** The correct mental model is an issued credential carried by the client and presented under a scheme. Bearer means possession is enough to present, not that authentication and authorization are waived. JWT and opaque formats are independent choices. A stolen bearer token remains sensitive, and a correctly signed token may still be wrong for the API or insufficient for Bob's notebook. Sender-constrained alternatives add key proof but not universal permission.

**Diagram or worked example:** One actor flow: Keycloak → client → notes-api → notebook-level allow/deny, with sensitive-token icon.

**Self-check:** Why is Bearer not the same as JWT?  
**Answer:** Bearer describes presentation; JWT describes one possible representation.

**Sources:** Chapter §§1–11; RFC 6750. [Canonical chapter](../docs/07-bearer-token.md) · [RFC 6750 Bearer](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 9449 DPoP](https://www.rfc-editor.org/rfc/rfc9449).

