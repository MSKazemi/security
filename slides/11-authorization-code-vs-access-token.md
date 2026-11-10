# Technical teaching slides — authorization code vs access token

**Format:** text-first technical slides.  
**Canonical chapter:** [Authorization code vs access token](../docs/11-authorization-code-vs-access-token.md)  
**Audience:** beginner to intermediate developers. **Slides:** 12.

This is detailed educational text, **not** a rendered slide deck or a media production script. Fictional examples only.

---

## Slide 01 — Why are there two different values?

**Learning objective:** Distinguish code exchange from API access.

**On-slide text**

- Authorization code = exchange once.
- Access token = call the intended API.
- Neither means unlimited permission.

**Teaching explanation:** A school application starts login and receives a short-lived authorization code via browser redirect. The running OAuth client exchanges that code with Keycloak at the token endpoint. It then receives an access token for its intended API. An API does not accept an authorization code as an access credential, and a token's validity does not imply universal authorization.

**Diagram or example:** Two differently labeled passes: an exchange ticket and a limited API pass. Separate doors for token endpoint and notes-api.

**Self-check:** Can the code be submitted to notes-api as Bearer?  
**Answer:** No; it belongs at Keycloak's token endpoint.

**Sources:** Chapter §§1–2; RFC 6749 §§4.1.2–4.1.3. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 02 — Who is involved in an authorization-code login?

**Learning objective:** Recognize user, browser, client, server, and API.

**On-slide text**

- Alice = user.
- lesson-web = running OAuth client.
- Keycloak = authorization and token server.
- notes-api = protected resource server.

**Teaching explanation:** The browser follows redirects, but the OAuth client is the running code that holds the transaction data and completes token redemption. Keycloak has a registration for lesson-web; that registration does not run the web app. After authentication and code exchange, the resource API validates access credentials and permissions on its own.

**Diagram or example:** Four actors plus browser drawn as distinct boxes. One arrow for redirect, one for token request, one for API request.

**Self-check:** Does Keycloak's client registration deploy the application?  
**Answer:** No, it only configures its identity-protocol relationship.

**Sources:** Chapter §§3–4; RFC 6749 §1.1. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 03 — Where does the code appear?

**Learning objective:** Trace the authorization response and callback.

**On-slide text**

- Authorization endpoint handles browser login.
- Browser redirected to registered callback.
- Callback receives code and state.
- Code is short-lived and single-use.

**Teaching explanation:** After Alice authenticates and the request is authorized, Keycloak returns a redirect to the client's registered callback with a temporary code and transaction state. The client must check the callback is part of the transaction it initiated. This redirect is not a token endpoint request, and the code must not be reused for later API calls.

**Diagram or example:** Authorization request → Keycloak → browser callback with code and state; mark the callback as client-owned.

**Self-check:** Is a code a JWT that should be decoded?  
**Answer:** Treat it as opaque; its purpose is single-use exchange.

**Sources:** Chapter §§2, 4; RFC 6749 §4.1.2. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 04 — How does the client redeem the code?

**Learning objective:** Explain the separate token endpoint exchange.

**On-slide text**

- Client sends POST /token.
- Include grant_type=authorization_code.
- Send code, redirect_uri and client_id.
- Include PKCE verifier and client authentication as applicable.

**Teaching explanation:** The token request occurs at the authorization server's token endpoint. The client sends the authorization code and the required binding information. When PKCE was used, it includes the original verifier, never the challenge as a substitute. Confidential clients also authenticate according to their registered method. The authorization server checks everything before returning tokens.

**Diagram or example:** A form request box leading from client to Keycloak token endpoint; no arrow to API in this stage.

**Self-check:** Does the browser send the access token to the API before token redemption?  
**Answer:** Not in the demonstrated backend code flow.

**Sources:** Chapter §§4–5; RFC 6749 §4.1.3; RFC 7636. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 05 — Where does the access token go?

**Learning objective:** Distinguish token response and API presentation.

**On-slide text**

- Token response → client.
- Access token → intended resource API.
- API checks audience, validity and permissions.

**Teaching explanation:** After code redemption, the authorization server returns an access token in its token response. In the BFF example, the backend holds that token and uses it for calls to notes-api; the browser instead uses a secure application session cookie. The API must verify the token's purpose and audience, its cryptographic or introspection validity and the requested resource action.

**Diagram or example:** Two lanes: Token endpoint → client and client → notes-api. A cookie stays on the browser-to-BFF lane.

**Self-check:** Can an ID token replace the API access token?  
**Answer:** No. OIDC ID tokens have a different purpose and recipient.

**Sources:** Chapter §§4, 8; OIDC Core; RFC 9700. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 06 — A complete BFF login sequence

**Learning objective:** Follow the entire five-part exchange accurately.

**On-slide text**

- 1. Start login with state + PKCE.
- 2. Keycloak authenticates.
- 3. Callback carries code.
- 4. BFF exchanges code and stores tokens.
- 5. API validates access token.

**Teaching explanation:** In a full Backend-for-Frontend architecture, the trusted application backend is the OAuth client. It creates transaction state and PKCE verifier, initiates authorization, validates callback state, redeems the code and securely stores tokens on the server. Browser requests subsequently use an opaque session identifier. The API receives an access token from the backend, not the browser's session cookie.

**Diagram or example:** Use the chapter §4 Mermaid sequence. Color must not be the only way to distinguish browser cookie, code and access token.

**Self-check:** Are BFF access tokens automatically stored server-side by every web framework?  
**Answer:** No; server-side storage is a separate design requirement.

**Sources:** Chapter §4; Keycloak OIDC docs; RFC 9700. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 07 — Why are codes single-use and short-lived?

**Learning objective:** Explain code replay and expiration.

**On-slide text**

- Authorization code is a one-time grant.
- Issuer enforces expiry and binding.
- RFC 6749 recommends at most 10 minutes.
- Provider configuration may be shorter.

**Teaching explanation:** A code exposed in a redirect URL has a limited role. OAuth servers must reject attempted reuse, and clients should exchange promptly. RFC 6749 recommends a code maximum lifetime of ten minutes but does not prescribe the same actual lifetime for every provider. A code issued at a hypothetical 10:00 and expiring at 10:05 must be rejected at 10:05:10, even with a valid verifier.

**Diagram or example:** Timeline with issuance, configured expiry, then a late redemption attempt marked rejected.

**Self-check:** Can PKCE turn an expired authorization code valid again?  
**Answer:** No; proof and validity are independent checks.

**Sources:** Chapter §§2, 6; RFC 6749 §4.1.2. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 08 — What exactly does PKCE add?

**Learning objective:** Explain challenge and verifier in the same flow.

**On-slide text**

- Client generates secret verifier V.
- Client sends S256 challenge H during authorization.
- Client sends original V at token exchange.
- Issuer checks H == S256(V).

**Teaching explanation:** PKCE is generated by the client per authorization request. The challenge is sent earlier through the browser, while the verifier is kept private until code redemption. The server binds the challenge/method to the code. An attacker with a stolen code but without the verifier ordinarily cannot redeem it. PKCE does not replace confidential-client authentication, redirect protection or API authorization.

**Diagram or example:** Split-screen: early S256 challenge and late secret verifier; only the token endpoint sees V.

**Self-check:** Is the verifier supposed to be part of the initial browser URL?  
**Answer:** No. Send only the derived challenge during authorization.

**Sources:** Chapter §7; RFC 7636 §§4.1–4.6. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 09 — What can cause invalid_grant?

**Learning objective:** Distinguish independent grant validation failures.

**On-slide text**

- Expired or reused code.
- Wrong client or redirect binding.
- Wrong or missing PKCE verifier.
- Invalid authorization grant.

**Teaching explanation:** The token endpoint has several independent reasons to deny redemption. A correct verifier is not sufficient when the code is expired, already consumed or bound to another client/redirect. The server generally uses invalid_grant for an invalid authorization grant, although exact responses vary with failure conditions. Do not turn error descriptions into assumptions about a successful login or API access.

**Diagram or example:** Decision tree based on chapter §6 with independent code validity and PKCE branches.

**Self-check:** An expired code has a matching verifier. Should tokens issue?  
**Answer:** No, reject the invalid grant.

**Sources:** Chapter §6; RFC 6749 §5.2; RFC 7636. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 10 — Four different credentials

**Learning objective:** Compare code, access, ID and refresh tokens.

**On-slide text**

- Authorization code → token endpoint (once).
- Access token → resource API.
- ID token → OIDC client.
- Refresh token → token endpoint (renewal).

**Teaching explanation:** These are not different names for the same object. An ID token conveys authentication claims to an OpenID Connect relying party, while the API expects a suitable access token. Refresh tokens, when issued, help the client request fresh access tokens and must be protected. Some grants issue tokens without an authorization code, so this diagram is for code flow rather than all OAuth grant types.

**Diagram or example:** Four credential cards with explicit destinations; avoid arrows from ID token to API.

**Self-check:** Does Client Credentials require a user's authorization code?  
**Answer:** No; it is a separate grant.

**Sources:** Chapter §8; RFC 6749; OIDC Core. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 11 — Security checks after token issuance

**Learning objective:** Show why token issuance is not final API authorization.

**On-slide text**

- Use HTTPS and exact redirects.
- Bind client transaction with state/PKCE.
- Validate issuer and intended audience.
- Enforce object-level API permissions.

**Teaching explanation:** A token's signature alone does not guarantee that the requesting user can operate on any resource. The API needs the right token type, trusted issuer, appropriate audience, validity and scopes/roles plus a decision about the particular notebook. Token lifetimes and revocation strategy also matter. The browser client must prevent injected or mixed-up authorization responses when it supports multiple identity providers.

**Diagram or example:** An API decision gate: credential valid → purpose/audience valid → notebook permission → accept or deny.

**Self-check:** Alice has a valid access token. May she read Bob's notebook?  
**Answer:** Only if the API explicitly authorizes it.

**Sources:** Chapter §9; RFC 9700. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 12 — Review: choose the correct recipient

**Learning objective:** Demonstrate mastery of the two endpoint roles.

**On-slide text**

- Keycloak /auth → initiate login.
- Keycloak /token → redeem code and refresh.
- notes-api → present access token.
- Different protocols, different trust decisions.

**Teaching explanation:** Revisit the same fictional lesson-web login. The authorization endpoint handles browser-based interaction; the token endpoint redeems a one-use grant and issues tokens; the resource API validates access tokens and applies policy. In particular, a matching PKCE verifier does not defeat code expiry, a valid ID token is not an API access credential, and a client's registration does not implement the business API.

**Diagram or example:** One final end-to-end map with labels code, verifier, access token and browser session cookie.

**Self-check:** What should happen if the API receives the authorization code as a Bearer credential?  
**Answer:** Reject it; the code is not a resource-server access token.

**Sources:** Chapter §§3–11; RFC 6749; RFC 9700. [Canonical chapter](../docs/11-authorization-code-vs-access-token.md) · [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

