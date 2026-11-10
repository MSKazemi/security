# Detailed teaching slides — FastAPI/Authlib OAuth BFF security

**Audience:** developers moving from browser OAuth to protected backend token handling.  
**Canonical chapter:** [OAuth BFF with FastAPI, Authlib and Keycloak](../docs/13-bff-authlib-browser-session-security.md).  
**Format:** 12 detailed text-first slides. No rendered deck, branding, animation, voiceover or publishing copy.

All examples use imaginary `school-lab`, `lesson-web`, Alice and `notes-api`.

---

## Slide 01 — What makes a backend a full OAuth BFF?

**Learning objective:** Identify the BFF's three required responsibilities.

**On-slide text**

- Backend acts as confidential OAuth client
- Backend manages access and refresh tokens
- Backend mediates protected resource requests
- Browser uses separate app session

**Teaching explanation:** RFC 10017 describes a BFF as the server-side OAuth client handling login, token state, and resource API requests. The browser never needs to read access or refresh tokens in this architecture. It instead sends an application-session cookie to the BFF. Merely adding an OAuth library to a Python service does not implement all these responsibilities. The API still validates bearer tokens and resource permissions.

**Diagram or worked example:** Five boxes: browser, BFF, session store, Keycloak, protected API; map responsibilities without implying any live deployment.

**Self-check:** Does importing Authlib alone implement a full BFF?  
**Answer:** No, you must add session, token management and API mediation.

**Sources:** Chapter §§1–2; RFC 10017 §6.1. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 02 — Full BFF vs token mediator vs browser client

**Learning objective:** Distinguish architectures by where access tokens go.

**On-slide text**

- Full BFF: OAuth access tokens backend-only
- Token mediator: browser may receive access token
- Browser client: JS obtains/manages tokens
- Storage model matters for XSS risks

**Teaching explanation:** A token-mediating backend might handle OAuth code exchange and keep refresh tokens on the server, while delivering access tokens to JavaScript so the browser can call an API. A browser-based OAuth client such as keycloak-js handles the login and token interaction in the frontend. A full BFF does neither: all resource requests pass through its backend. The user experience may look identical despite very different credential exposure.

**Diagram or worked example:** Three-column architecture comparison, with a clear boundary showing whether browser JavaScript can reach access tokens.

**Self-check:** If FastAPI returns access_token to the browser, is it a full BFF?  
**Answer:** No, that resembles token mediation.

**Sources:** Chapter §2; RFC 10017 §§6.1–6.3. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 03 — Five actors and two credentials

**Learning objective:** Explain the app cookie and OAuth access token as different objects.

**On-slide text**

- Browser → BFF: opaque session cookie
- BFF → server store: session lookup
- BFF → notes-api: intended access token
- Keycloak → BFF: token response

**Teaching explanation:** In the recommended classroom design, the browser stores a high-entropy opaque application session identifier. Only the BFF understands the cookie and uses it to retrieve Alice's session and protected token state. The BFF attaches the appropriate access token to an authorized downstream notes-api call. The API does not treat a browser session cookie as its OAuth credential. Both the cookie and access token are sensitive and require separate lifetimes.

**Diagram or worked example:** Chapter §3 Mermaid trust-boundary flow; mark client cookie and downstream access token arrows differently.

**Self-check:** Is the BFF's browser session cookie a JWT issued by Keycloak?  
**Answer:** No, it is a distinct app credential in this example.

**Sources:** Chapter §3; RFC 10017 §6.1. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 04 — Authorization Code + PKCE login: first half

**Learning objective:** Trace authorization without revealing the verifier.

**On-slide text**

- BFF creates state and verifier
- Browser redirects with S256 challenge
- Keycloak authenticates Alice
- Browser callback carries one-use code and state

**Teaching explanation:** A confidential BFF begins Authorization Code + PKCE by generating a per-request verifier, storing the matching transaction, and sending only its S256 challenge in the browser authorization request. After Alice signs in, Keycloak redirects to the registered callback with a one-time code. The backend checks callback state and other transaction bindings before exchanging that code. Redirect URI validation, issuer binding and OIDC nonce are independent checks according to the configured flow.

**Diagram or worked example:** First half of Chapter §4 sequence; tag the S256 challenge in authorization request and hide the verifier until code exchange.

**Self-check:** Should the original PKCE verifier appear in the browser authorization URL?  
**Answer:** No, only the challenge travels first.

**Sources:** Chapter §4; RFC 7636; RFC 9700. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 05 — Authorization Code exchange: second half

**Learning objective:** Locate client authentication, token receipt and session creation.

**On-slide text**

- BFF validates state before redemption
- Token request sends code and verifier
- Confidential BFF authenticates as client
- Backend stores tokens and sets new app cookie

**Teaching explanation:** The OAuth client backend validates state and retrieves the matching PKCE verifier, then calls Keycloak's token endpoint. A confidential client separately proves its registered client identity; PKCE does not replace client authentication. After a successful exchange and required OIDC validation, the backend associates tokens with a server-side application session and returns a cookie holding only the new opaque session identifier. The browser never receives raw OAuth token values.

**Diagram or worked example:** Second half of Chapter §4 sequence: code exchange, token response to backend, cookie to browser and Bearer API request.

**Self-check:** Which component receives the access/refresh token response?  
**Answer:** The BFF backend.

**Sources:** Chapter §4; RFC 10017 §6.1.3.1. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 06 — Authlib is a protocol library, not a whole architecture

**Learning objective:** Identify implementation work outside the OAuth client library.

**On-slide text**

- authorize_redirect handles authorization initiation
- authorize_access_token exchanges the grant
- App designs protected session and token storage
- App implements policy, refresh and logout

**Teaching explanation:** Authlib provides OAuth/OIDC web-client integration for Python frameworks. It can help generate and verify transaction parameters and exchange authorization codes with the server, but the app remains responsible for mapping sessions to users, protecting access/refresh tokens, enforcing resource authorization, managing concurrent refresh and safely forwarding API calls. A small standalone PoC using Authlib may demonstrate login correctly without proving that the product's integrated BFF security behavior exists.

**Diagram or worked example:** Draw Authlib inside FastAPI as a library; outside it show storage, cookie policy, CSRF, API proxy and lifecycle tasks.

**Self-check:** If Authlib successfully refreshes a token in a test container, is the integrated backend verified?  
**Answer:** No, you must test actual integration and all boundaries.

**Sources:** Chapter §5; Authlib Web Clients. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 07 — Signed Starlette cookie is readable

**Learning objective:** Prevent the common session vault misconception.

**On-slide text**

- Starlette SessionMiddleware signs cookie state
- Signed does NOT mean encrypted
- Never put refresh/access tokens in readable cookie
- Use opaque ID plus protected backend store

**Teaching explanation:** Starlette's built-in SessionMiddleware provides signed client-side session contents: the browser can read the content, though it cannot alter it undetected. Therefore, storing an OAuth refresh token inside a signed request.session can expose that credential to browser recipients. For a strict server-side-token BFF design, store only an unguessable session ID in the cookie and retain tokens in protected backend storage. Framework defaults may not meet this architecture without extra session infrastructure.

**Diagram or worked example:** Side-by-side signed readable cookie versus opaque cookie pointing to protected backend record.

**Self-check:** Can signed request.session securely hide OAuth refresh tokens from the browser?  
**Answer:** No.

**Sources:** Chapter §5; Starlette SessionMiddleware. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 08 — Cookie flags and session fixation

**Learning objective:** Select browser cookie controls and server-side expiry.

**On-slide text**

- Secure and HttpOnly
- Carefully selected SameSite, Path and host scope
- Rotate identifier at login
- Enforce server expiry and invalidate on logout

**Teaching explanation:** A BFF session cookie must use Secure over HTTPS and HttpOnly. RFC 10017 recommends SameSite=Strict, Path=/, no Domain attribute and a host-only HTTP cookie prefix. A carefully justified Lax exception for particular login-return flows needs additional CSRF defenses. SameSite determines which cross-site requests carry the cookie; Strict may require adjusted navigation UX. The __Host- cookie prefix has specific Secure, Path=/ and no-Domain requirements. Server-side TTL and session rotation matter independently from cookie expiry: a replayed pre-login ID should not remain valid after authentication.

**Diagram or worked example:** Cookie annotation plus rotation timeline pre-login ID → new post-login ID.

**Self-check:** Does HttpOnly by itself stop a malicious cross-site request?  
**Answer:** No; CSRF needs its own defense.

**Sources:** Chapter §6; RFC 10017 §6.1.3.2. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 09 — CSRF, CORS and XSS are not synonyms

**Learning objective:** Understand each browser threat at the correct boundary.

**On-slide text**

- CSRF abuses automatic cookie sending
- CORS controls selected cross-origin browser reads
- XSS can send same-origin authenticated requests
- Defend actions with context-aware CSRF controls

**Teaching explanation:** With cookie-based sessions, other websites can attempt to trigger operations through a victim's browser. A full BFF must implement CSRF protection: SameSite, Origin checks, anti-CSRF tokens or equivalent controls depending on application design. CORS is not a universal authorization layer and HttpOnly cannot stop same-origin malicious JavaScript from making requests. CSP, output encoding and strong frontend practices mitigate XSS, but do not change API resource authorization responsibilities.

**Diagram or worked example:** Risk matrix with three rows: CSRF, CORS, XSS; note each prevents a different attack.

**Self-check:** Does a full BFF eliminate XSS or CSRF?  
**Answer:** No.

**Sources:** Chapter §7; RFC 10017 §6.1.3.3. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 10 — Refresh races, revocation and logout

**Learning objective:** Explain lifecycle behavior after initial login.

**On-slide text**

- Coordinate concurrent refresh
- Atomically persist rotated token state
- Distinguish invalid refresh grant from outage
- Separate local session logout from issuer logout

**Teaching explanation:** A valid app session may outlive an access token. Several concurrent browser requests can detect expiry at once and try to redeem the same rotating refresh token, which may cause invalid_grant failures. A backend should coordinate refresh per session and update stored tokens atomically. A revoked refresh grant requires reauthentication, while temporary Keycloak outages need bounded error handling. Local session deletion, OIDC provider logout and access-JWT validity are related but different state transitions.

**Diagram or worked example:** Chapter §8 flowchart with concurrent refresh coordination and failure branches.

**Self-check:** Does deleting an app cookie automatically revoke every issued access JWT?  
**Answer:** Not necessarily.

**Sources:** Chapter §8; RFC 9700; RFC 10017. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 11 — Why localhost HTTP can behave differently

**Learning objective:** Distinguish secure context errors from actual network security.

**On-slide text**

- localhost often treated as trustworthy
- Ordinary http://VM-IP not a secure context
- WebCrypto may require HTTPS secure context
- Backend PKCE does not make HTTP transport safe

**Teaching explanation:** Browsers commonly treat loopback origins as potentially trustworthy even when using HTTP. A browser app served on a normal private-network HTTP IP is usually not a secure context, so APIs such as crypto.subtle may be unavailable. Running the PKCE code exchange inside Python removes that particular browser JavaScript requirement, but does not protect user cookies or OAuth codes from interception on an unencrypted network. The correct production answer is trusted HTTPS and controlled proxy/redirect configuration.

**Diagram or worked example:** Two browser address bars: loopback with conditional secure-context badge, VM IP HTTP without, plus HTTPS recommendation.

**Self-check:** Should a developer disable PKCE or use plain HTTP to work around unavailable WebCrypto?  
**Answer:** No.

**Sources:** Chapter §9; MDN Secure Contexts. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 12 — BFF security acceptance checklist

**Learning objective:** Convert design understanding into testable outcomes.

**On-slide text**

- Login: state, PKCE and new opaque session
- Browser: cookie only, no OAuth tokens
- API: access token and resource policy
- Refresh/logout/outage: fail safely

**Teaching explanation:** The final learning goal is to separate conceptual correctness from tested implementation. Check that the actual backend validates callbacks, stores tokens server-side, sets correct cookie flags, enforces CSRF, mediates authorized API calls and blocks token leakage. **RFC 10017 also requires a strict outbound host/path allowlist before forwarding access tokens**, so a client-supplied URL must not be usable to divert credentials. Then test concurrent refresh, revocation, Keycloak downtime, logout behavior, wrong-audience access tokens and notebook ownership denial. A standalone demonstration is not a substitute for integration tests and a security review.

**Diagram or worked example:** Small matrix: test scenario, intended evidence, expected failure mode; do not claim results without running tests.

**Self-check:** What must be verified before calling an application a secure full BFF?  
**Answer:** All OAuth, session, resource mediation, CSRF and lifecycle boundaries.

**Sources:** Chapter §§10–12; RFC 10017; Authlib. [Chapter](../docs/13-bff-authlib-browser-session-security.md) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/) · [Starlette Sessions](https://www.starlette.io/middleware/#sessionmiddleware).

