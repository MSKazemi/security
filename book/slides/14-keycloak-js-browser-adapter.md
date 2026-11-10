# Detailed teaching slides — keycloak-js browser OIDC adapter

**Audience:** browser application developers and students.  
**Canonical source:** [keycloak-js browser adapter](../../docs/14-keycloak-js-browser-adapter.md).  
**Format:** 12 detailed text-first slides; no rendered, branded or animated presentation.

All examples use only fictional classroom users, applications and tokens.

---

## Slide 01 — What is keycloak-js?

**Learning objective:** Identify adapter, OAuth client and identity provider as separate parts.

**On-slide text**

- keycloak-js: browser JavaScript library
- Keycloak: authorization server / OIDC provider
- Client registration: server-side metadata
- Running website: OAuth client

**Teaching explanation:** The Keycloak JavaScript adapter helps a browser application talk to Keycloak using OIDC and OAuth. The library runs in the page, while Keycloak runs separately as the identity service. A client registration stores the identifier, allowed callbacks and flow settings; it does not host the JavaScript application. This difference is the basis for comparing browser-based OAuth clients with a backend Authlib client.

**Diagram or worked example:** Object diagram from Chapter §1 with running app outside Keycloak and a separate configuration record inside the identity service.

**Self-check:** Is the keycloak-js package itself an authentication server?  
**Answer:** No, it is a browser-side client library.

**Sources:** Chapter §1; Keycloak JS documentation. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 02 — Browser application is the OAuth client

**Learning objective:** Understand why browser JavaScript is public client code.

**On-slide text**

- OAuth code runs in the browser
- Client ID is public, not password
- No private client secret in bundled JS
- API validates Bearer token separately

**Teaching explanation:** When keycloak-js handles login, the JavaScript application is the OAuth client. Because anyone can inspect a site's JavaScript, it cannot safely keep a confidential OAuth client secret. Register it accordingly and use Authorization Code + PKCE. After the exchange, browser JavaScript can possess an access token to call the intended API, which must independently validate the token and enforce access to the particular notebook.

**Diagram or worked example:** Chapter §2 flow: browser app → Keycloak → browser app → notes-api, separating grant from API permission.

**Self-check:** Can hiding a client secret in minified JavaScript keep it confidential?  
**Answer:** No.

**Sources:** Chapter §2; RFC 10017. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 03 — Adapter initialization in a fictional app

**Learning objective:** Explain the URL, realm, client ID and onLoad settings.

**On-slide text**

- url = trusted Keycloak origin
- realm = school-lab
- clientId = lesson-web
- onLoad = check-sso or login-required

**Teaching explanation:** The JavaScript app builds a Keycloak adapter using an issuer URL, realm identifier and registered client ID. It then calls init with a login behavior and can explicitly configure PKCE S256. The example contains no secrets. Developers must verify a trusted HTTPS origin and correct redirects for the installed version. Init may interact with URL parameters, so application routing startup order can matter.

**Diagram or worked example:** Small conceptual configuration example from Chapter §3 with only fictional fields, no real tokens.

**Self-check:** Is clientId an OAuth client secret?  
**Answer:** No, it identifies the client registration.

**Sources:** Chapter §3; Keycloak JS documentation. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 04 — Authorization Code + PKCE in the browser

**Learning objective:** Track challenge, code, verifier and token positions.

**On-slide text**

- Client makes V and S256 challenge H
- Authorization request carries H
- Callback returns code
- Token endpoint receives code plus V

**Teaching explanation:** The browser app generates a fresh verifier and derived challenge for a login. It navigates to Keycloak using the challenge. Keycloak authenticates the user and redirects the browser with an authorization code. The adapter checks its transaction and exchanges that code with the original verifier. A successful token response may include an access token for the API. This flow is different from the historical Implicit grant and must never be represented as returning an API access token in the initial callback.

**Diagram or worked example:** Chapter §4 sequence: color-independent labels for challenge, code, verifier, access token.

**Self-check:** Does Keycloak return access token directly in the callback URL for standard code flow?  
**Answer:** No.

**Sources:** Chapter §4; RFC 7636; RFC 9700. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 05 — What does the browser do with tokens?

**Learning objective:** Recognize token exposure and resource API validation.

**On-slide text**

- Adapter exposes access-token state
- Browser can call intended API with Bearer
- API validates issuer, audience and permission
- ID token is not API access token

**Teaching explanation:** A browser OAuth client may include a current access token in an Authorization header when calling a protected resource. The API cannot trust that token just because keycloak-js returned it; it must verify issuer, audience, expiry, token type and object-level authorization. ID tokens are intended for the OIDC relying party and cannot replace API access credentials. A stolen usable Bearer token can be replayed within its valid scope and lifetime.

**Diagram or worked example:** Two separate token lanes showing ID token to client and access token to notes-api.

**Self-check:** May notes-api accept an ID token signed by the same Keycloak issuer?  
**Answer:** No, the token purpose is different.

**Sources:** Chapter §§4–5; RFC 8725. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 06 — updateToken and refresh failures

**Learning objective:** Understand the adapter's lifecycle interface.

**On-slide text**

- updateToken(minValidity) checks expiry
- May obtain new token using refresh grant
- Failed refresh requires recovery
- Never log token strings

**Teaching explanation:** The adapter offers updateToken to refresh access-token state when the existing access token is near expiration, subject to issuer policy. A request can fail because the refresh grant is revoked or expired, Keycloak is unavailable or the client session is invalid. The app must handle that failure without leaking credentials or silently assuming continued login. API authorization remains separate even when a refresh succeeds. Token timing and clock skew should be measured rather than assumed.

**Diagram or worked example:** Lifecycle decision tree: usable token? refresh possible? update or clear/relogin.

**Self-check:** Does updateToken always succeed because Alice previously logged in?  
**Answer:** No.

**Sources:** Chapter §5; Keycloak JS documentation. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 07 — login-required vs check-sso

**Learning objective:** Explain two startup behaviors and tradeoffs.

**On-slide text**

- login-required can force login
- check-sso can leave page unauthenticated
- Silent check may use iframe
- Browser cookie restrictions affect detection

**Teaching explanation:** The adapter can require authentication on startup or check if an existing SSO session is available. A silent check can avoid a full navigation by using an iframe, but modern browser tracking protections may block relevant third-party cookies and make silent SSO detection fail or fall back to a normal redirect. An app should handle unauthenticated states instead of assuming every page load produces a valid token.

**Diagram or worked example:** Chapter §6 branching diagram for login-required, check-sso, silent and fallback.

**Self-check:** Does silent check-sso work identically across all browsers?  
**Answer:** No.

**Sources:** Chapter §6; Keycloak JS modern browsers section. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 08 — Session-status iframe and logout detection

**Learning objective:** Explain why browser policies can delay logout awareness.

**On-slide text**

- Iframe may monitor SSO cookie state
- Third-party cookie restrictions may disable it
- Refresh failure can reveal changed SSO state
- Do not parse provider cookie internals

**Teaching explanation:** The Keycloak JavaScript adapter can use a session-status iframe to detect single sign-out in supported browsers. If third-party cookie restrictions prevent it from working, the application might not recognize that a user logged out elsewhere until a later token refresh attempt or another session check. That delay is not equivalent to unlimited API access because access tokens still have lifetime and audience policies, but it must influence session and revocation design.

**Diagram or worked example:** Simple timeline: remote logout → iframe blocked → later refresh failure → app reauth.

**Self-check:** Will the adapter always immediately know about an SSO logout in a different window?  
**Answer:** No.

**Sources:** Chapter §6; Keycloak JS documentation. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 09 — Web Crypto requires a trusted origin

**Learning objective:** Distinguish local browser behavior from remote deployment.

**On-slide text**

- http://localhost often considered secure-context exception
- Ordinary remote HTTP IP isn't
- crypto.subtle may be absent
- Use trusted HTTPS, not disabled PKCE

**Teaching explanation:** Browser Web Crypto features required by PKCE or optional sender-constraining mechanisms generally need a secure context. Localhost and loopback often receive special browser treatment. A remote HTTP page usually does not, so the same adapter may behave differently even though its JavaScript file is identical. Shipping the library from a local static route does not change the page origin's security classification. Use HTTPS and correct callback policy; never turn off PKCE as a workaround.

**Diagram or worked example:** Two fake browser address bars with secure-context state and encrypted-transport label.

**Self-check:** Can bundling keycloak-js locally make http://remote-IP a secure context?  
**Answer:** No.

**Sources:** Chapter §7; MDN Secure Contexts. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 10 — Browser adapter versus FastAPI/Authlib BFF

**Learning objective:** Explain who performs exchange and who stores tokens.

**On-slide text**

- Browser adapter: OAuth client in JS
- BFF: OAuth client in backend
- Browser adapter may expose access tokens to JS
- Full BFF proxies resource APIs and uses app cookie

**Teaching explanation:** Both architectures can speak standards-based OAuth/OIDC with Keycloak and use Authorization Code + PKCE, but they differ critically in their threat boundaries. Browser keycloak-js exchanges the code and manages token state in JavaScript memory. A full BFF performs the exchange as a confidential backend, protects token state and sends the browser an application session cookie. A hybrid backend returning access tokens to JavaScript should be called token mediation instead.

**Diagram or worked example:** Chapter §8 comparison table, with trust boundaries independent of styling.

**Self-check:** If Authlib exchanges the code but returns access_token to JS, is it full BFF?  
**Answer:** No.

**Sources:** Chapter §8; RFC 10017. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 11 — CDN is script delivery, not identity

**Learning objective:** Separate asset source from login protocol and transport.

**On-slide text**

- Script may come from CDN or local bundle
- Cache may reuse either source
- Keycloak performs actual authentication
- Neither path fixes insecure HTTP page

**Teaching explanation:** A browser may download keycloak-js from a CDN or an application-controlled bundle. That choice affects external runtime dependency, supply-chain review and caching, but does not decide which component acts as the OAuth client or whether the browser origin is secure. The identity provider still authenticates and issues tokens. If dependency delivery fails, first-load availability changes; a cached copy may still be used according to HTTP policy.

**Diagram or worked example:** Two asset-source routes converging into the same browser OAuth application and Keycloak server.

**Self-check:** Does removing a runtime CDN guarantee secure OAuth cookies or PKCE?  
**Answer:** No.

**Sources:** Chapter §9; MDN Caching. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 12 — Browser adapter security self-check

**Learning objective:** Explain expected failures before implementing production code.

**On-slide text**

- Public client, no embedded secrets
- Authorization Code + PKCE S256
- Trusted HTTPS and narrow callbacks
- Token refresh and third-party cookie tests
- API audience and notebook policy

**Teaching explanation:** A responsible developer tests login-required and check-sso behavior with and without an issuer session; observes PKCE fields without leaking tokens; verifies refresh and logout handling; and repeats the browser checks in a mode blocking third-party cookies. A resource server should reject wrong-audience tokens and forbidden notebook access independently. This test suite is an educational acceptance plan, not evidence that a real browser or production application has already been tested.

**Diagram or worked example:** Chapter §11 matrix of tests and expected observations; finish with short scenario questions.

**Self-check:** What security property must notes-api still enforce after a successful adapter login?  
**Answer:** Access-token validation and exact resource authorization.

**Sources:** Chapter §§10–12; Keycloak JS; RFC 10017. [Chapter](../../docs/14-keycloak-js-browser-adapter.md) · [Keycloak JavaScript adapter](https://www.keycloak.org/securing-apps/javascript-adapter) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

