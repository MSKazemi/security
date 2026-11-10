# Teaching slide outline — OAuth, OIDC and Keycloak learning roadmap

**Format:** 12 detailed, text-first classroom slides. **Audience:** beginners and practicing engineers.  
**Canonical source:** [Security learning roadmap](../docs/00-learning-roadmap.md).  
**Not included:** rendered slides, branding, narration, animations or platform publishing. All examples are synthetic.

---

## Slide 01 — Your security learning journey

**Learning objective:** Understand what the course teaches and how concepts connect.

**On-slide text**

- Learn people and app roles
- Follow authorization grants and tokens
- Validate API requests
- Choose a safe app architecture

**Teaching explanation:** Security login protocols become easier when the student asks concrete questions: who is the user, where does the running client live, who issues tokens and who protects data? The course begins with concepts and then follows real protocol boundaries. The goal is not merely to decode a JWT but to explain why an API accepts or rejects a particular action on a particular resource.

**Diagram or worked example:** Draw four stages—identity, token grant, credential validation and permission check—connected in order.

**Self-check:** Does a successful login automatically grant every API operation?  
**Answer:** No, each API must enforce appropriate resource permissions.

**Sources:** Roadmap §§1–4; Keycloak docs. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 02 — Authentication versus authorization

**Learning objective:** Separate identity establishment from permission checks.

**On-slide text**

- Authentication: who signed in?
- Authorization: what action on what resource?
- Login is not universal permission

**Teaching explanation:** Alice may authenticate successfully to the school identity provider while still lacking permission to read Bob's private notebook. Authentication establishes her identity or login event under an issuer; authorization determines access based on resource policy. These are separate decisions, even if they happen near each other in a web application. A valid access token can also represent a client/service without any interactive end-user login.

**Diagram or worked example:** Two gates: login identity established, then notes-api ownership and policy decision.

**Self-check:** Can authentication alone authorize Bob's notebook?  
**Answer:** No.

**Sources:** Roadmap §§1, 5; RFC 9700. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 03 — The five actors in a normal login

**Learning objective:** Identify the user, browser, client, issuer and API.

**On-slide text**

- Alice is the person
- lesson-web is the running OAuth client
- Keycloak is authorization server / OIDC provider
- notes-api is the protected resource

**Teaching explanation:** An OAuth client is actual application code. A Keycloak client registration describes how that running app is allowed to interact with the issuer, but the registration is not an app deployment. Alice signs in through a browser; Keycloak handles authorization and may issue tokens; notes-api receives an appropriate access token and decides whether the requested notebook action is permitted.

**Diagram or worked example:** Chapter §2 concept map, with registration shown inside Keycloak and running client outside.

**Self-check:** Does creating a Keycloak client registration launch the app?  
**Answer:** No, it is configuration metadata.

**Sources:** Roadmap §2; Keycloak fundamentals. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 04 — OAuth, OIDC and Keycloak: three levels

**Learning objective:** Explain how framework, identity layer and implementation relate.

**On-slide text**

- OAuth 2.0: delegated authorization framework
- OIDC: identity layer on OAuth 2.0
- Keycloak: server implementing these protocols

**Teaching explanation:** OAuth 2.0 specifies mechanisms for a client to obtain authorized access to resources; it does not define the complete user-login outcome in the same manner as OpenID Connect. OIDC adds identity tokens and standardized authentication semantics. Keycloak implements OAuth/OIDC behavior for configured realms and clients. Choosing Keycloak does not remove the need for an OAuth client and protected resource server.

**Diagram or worked example:** Three-layer diagram: OAuth base, OIDC additional login semantics, Keycloak product implementing.

**Self-check:** Does OIDC replace OAuth?  
**Answer:** No, OIDC builds on OAuth.

**Sources:** Roadmap §§1, 3; OIDC Core. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 05 — Choose a flow based on who runs where

**Learning objective:** Match login grants to the application type.

**On-slide text**

- Web/native with browser: Authorization Code + PKCE
- Constrained two-device: risk-assessed Device Flow
- Service acting as itself: Client Credentials
- Avoid password grant

**Teaching explanation:** The correct OAuth grant depends on whether a human is present, how the client can handle redirects and secrets, and whether it is genuinely input constrained. Authorization Code + PKCE is standard for interactive browser/native applications. Client Credentials is for a service principal, not Alice's login. Device Flow is for constrained devices and has consent-phishing risks; never use it by default when an external-browser flow is possible.

**Diagram or worked example:** Four scenario cards—web, desktop, smart TV and backend service—with one flow and caveat each.

**Self-check:** Should every command-line tool use Device Flow?  
**Answer:** No; prefer external-browser Authorization Code + PKCE when feasible.

**Sources:** Roadmap §5; RFC 8252; RFC 10027. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 06 — Code and PKCE are not access tokens

**Learning objective:** Track the one-time code and verifier correctly.

**On-slide text**

- Client creates verifier V and challenge H
- Authorization request carries H
- Callback carries one-use code
- Token request carries code and V

**Teaching explanation:** The client creates the PKCE verifier before login, sends a derived S256 challenge to Keycloak and saves the original verifier. The browser redirect carries an authorization code once the user approves. The running client exchanges that code with the original verifier at the token endpoint. The API receives a suitable access token after the exchange, never the code or verifier. A correct verifier does not revive an expired code.

**Diagram or worked example:** Two arrows with different labels: browser authorization challenge and back-channel token exchange.

**Self-check:** Does notes-api check a PKCE verifier on each call?  
**Answer:** No; PKCE is checked by the token endpoint.

**Sources:** Roadmap §§4, 6; RFC 7636. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 07 — Four credentials, four destinations

**Learning objective:** Distinguish code, access, ID and refresh tokens.

**On-slide text**

- Code → token endpoint for one-time exchange
- Access token → intended resource API
- ID token → OIDC client
- Refresh token → authorization server renewal

**Teaching explanation:** Several related artifacts occur in identity systems, but they have distinct recipients and purposes. An ID token can tell the OIDC client about authentication, while an access token authorizes resource-server requests according to the API's policy. A refresh token belongs only at the issuer token endpoint for renewal, not in an API Authorization header. Mixing token types can introduce token-substitution vulnerabilities.

**Diagram or worked example:** Four token cards each connecting to its allowed recipient. Cross out ID token to API.

**Self-check:** Can an API accept an ID token as a Bearer access token?  
**Answer:** No.

**Sources:** Roadmap §6; OIDC Core; RFC 9700. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 08 — JWT is a format; JWKS is a trusted key set

**Learning objective:** Explain what token contents and signature keys represent.

**On-slide text**

- JWT may carry signed claims
- JWK describes a cryptographic key
- JWKS contains a set of JWKs
- Decoding never equals verifying

**Teaching explanation:** A JWT can contain claims such as issuer, audience and expiration. A JWK represents one cryptographic key; a trusted JWKS can publish public keys that allow a resource server to validate appropriate JWT signatures. A JSON key set fetched from an arbitrary host is not trustworthy just because it parses as JSON. The API must anchor verification to a preconfigured issuer, supported algorithm and intended audience.

**Diagram or worked example:** JWT card and a key-set cabinet; mark trusted issuer as source of key trust.

**Self-check:** Does decoding a JWT verify the signature?  
**Answer:** No.

**Sources:** Roadmap §§1, 6; RFC 7517; RFC 7519. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 09 — An API has its own security job

**Learning objective:** Follow credential validation and object-level authorization.

**On-slide text**

- Validate issuer, signature or introspection
- Check audience, expiry and purpose
- Check scope/role and resource ownership
- Reject wrong audience or forbidden notebook

**Teaching explanation:** Even a correctly signed JWT can be inappropriate for a particular API. notes-api must check that the token is intended for it, was issued by the trusted authority and meets time and token-type requirements. Only then can the API decide if Alice may read the specific notebook. A broad reader role cannot stand in for notebook ownership or tenant policy. This is why successful authentication and token issuance are not the end of the security story.

**Diagram or worked example:** Two-stage API decision tree with 401 for invalid credential and 403 for forbidden action.

**Self-check:** May notes-api accept a signed token intended only for billing-api?  
**Answer:** No.

**Sources:** Roadmap §§1, 8; RFC 8725; RFC 9700. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 10 — Device Flow has a distinct security problem

**Learning objective:** Recognize cross-device consent phishing and limited inputs.

**On-slide text**

- One device shows user code or QR
- User approves in separate trusted browser
- Client polls for token response
- Cross-device context can be phished

**Teaching explanation:** Device Authorization is useful when a device lacks a usable keyboard/browser, but it transfers authorization context between devices over a channel that is not automatically authenticated. A user can be misled into approving a request initiated by someone else. The 2026 cross-device security BCP requires a risk assessment and appropriate mitigations. For normal same-device browser flows, Authorization Code + PKCE is generally safer and simpler.

**Diagram or worked example:** Smart TV, user phone and Keycloak diagram; warning that QR/source context must be trusted.

**Self-check:** Should an app trust every official-looking login QR code?  
**Answer:** No; cross-device requests can be phished.

**Sources:** Roadmap §5; RFC 8628; RFC 10027. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 11 — Browser architecture: BFF versus SPA

**Learning objective:** Explain who holds OAuth tokens and who uses a session cookie.

**On-slide text**

- Full BFF: backend handles OAuth tokens
- Browser normally uses app session cookie
- Browser OAuth client: JS directly receives tokens
- CSRF and XSS still matter

**Teaching explanation:** A browser-facing app may be built as a full Backend-for-Frontend, token-mediating backend, or browser-only OAuth client. These architectures differ in who performs code exchange and how tokens are stored or exposed. A BFF can keep OAuth tokens server-side, but must still protect cookies and sessions from CSRF and XSS-related abuse. Selecting a flow without understanding the actual application architecture leads to misleading security claims.

**Diagram or worked example:** Three architecture rows from RFC 10017, highlighting browser token exposure differences.

**Self-check:** Does a BFF automatically eliminate CSRF and XSS?  
**Answer:** No.

**Sources:** Roadmap §5; RFC 10017. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 12 — Practice, explain, and test safely

**Learning objective:** Use a course-completion method without real secrets.

**On-slide text**

- Read chapter and slide explanation
- Draw arrows without looking
- Predict denied and accepted cases
- Use a disposable local realm and offline PKCE lab

**Teaching explanation:** The learner should be able to draw the actors, follow each credential, explain why a wrong-audience token is rejected and select the right grant for four scenarios. Reproduce only in a disposable Keycloak environment with fictional users. The offline PKCE Python lab teaches S256 without an online service. Never publish real tokens, signing keys, session identifiers or customer configuration. Practical confirmation is necessary before treating implementation understanding as complete.

**Diagram or worked example:** Four-step learning loop: read, draw, predict, practice. Finish with a small quiz.

**Self-check:** What is the final security question after validating a token?  
**Answer:** Whether the requested action on this particular resource is allowed.

**Sources:** Roadmap §§7–10; book index. [Canonical roadmap](../docs/00-learning-roadmap.md) · [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700) · [Browser Apps BCP](https://www.rfc-editor.org/rfc/rfc10017).

