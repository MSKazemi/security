# Teaching slides — Choosing OAuth and OIDC flows

**Audience:** engineering students and application developers.  
**Canonical source:** [Flow selection chapter](../docs/02-authentication-flows.md).  
**Format:** 12 detailed text-first slides, not a rendered deck, storyboard or social script. All examples fictional.

---

## Slide 01 — Flows are ways to obtain tokens

**Learning objective:** Understand grants rather than treating flow names as permissions.

**On-slide text**

- Grant chooses how client obtains token
- OAuth scope and API permission are different
- App architecture affects security

**Teaching explanation:** Authorization Code, Device Authorization and Client Credentials are different methods for a client to request access tokens from an authorization server. They do not mean every operation is automatically permitted: the resource API must validate the access token and check authorization for the specific resource. When selecting a flow, distinguish the presence of a human, the client type, and whether a trusted browser/redirect is feasible.

**Diagram or worked example:** One token-issuance gate and one distinct API-permission gate.

**Self-check:** Does choosing Device Flow grant permission to all API resources?  
**Answer:** No; grants and resource authorization serve different purposes.

**Sources:** Chapter §§1–2; RFC 6749. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 02 — Three questions before choosing

**Learning objective:** Start with human presence, client location and browser capabilities.

**On-slide text**

- Is a person logging in?
- Where does client code run?
- Can the user use an external browser and redirect?

**Teaching explanation:** A web application and a headless service have different security requirements. A backend can protect client authentication credentials; a distributed CLI or browser SPA cannot hold a shared confidential secret safely. If a client has a usable trusted browser and callback, Authorization Code + PKCE is generally the starting point. Device Flow should be considered only for genuinely constrained cases after a security risk assessment.

**Diagram or worked example:** Three-step decision tree based on Chapter §1; do not draw every client as a web browser.

**Self-check:** What flow is natural for a backend service acting as itself?  
**Answer:** Client Credentials.

**Sources:** Chapter §1; RFC 9700; RFC 8252. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 03 — Four choices, one comparison

**Learning objective:** Recognize what each major grant is for.

**On-slide text**

- Code + PKCE: interactive redirect
- Device: cross-device authorization and polling
- Client Credentials: service access
- Refresh Token: renew existing authorization

**Teaching explanation:** An Authorization Code flow involves a browser redirect and later one-time code redemption. Device Authorization uses a second device for user interaction and requires polling. Client Credentials is a non-user grant for a client/service principal. A Refresh Token grant renews prior authorization when allowed but does not replace a user's initial authentication mechanism. ROPC and Implicit are historical patterns not recommended for new designs.

**Diagram or worked example:** Four rows with user involvement, browser requirement, network exchange and risks.

**Self-check:** Which grant doesn't require Alice to sign in interactively?  
**Answer:** Client Credentials.

**Sources:** Chapter §2; RFC 6749; RFC 8628. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 04 — Code flow: browser and client have different jobs

**Learning objective:** Follow authorization response versus token exchange.

**On-slide text**

- Browser follows authorization URL
- Keycloak authenticates Alice
- Callback returns short-lived code
- Client exchanges code at token endpoint

**Teaching explanation:** The running OAuth client initiates authorization and creates per-request state and PKCE values. The browser transports the user to Keycloak. After successful interaction, Keycloak redirects the browser with a code; the client uses the callback to bind the transaction and exchange that code at the token endpoint. The API only sees a valid access token later, not the authorization code. This is why the code and access-token names should never be used interchangeably.

**Diagram or worked example:** Chapter §3 sequence diagram labeled with authorization endpoint, callback, token endpoint and API.

**Self-check:** Does the browser's callback itself contain the API access token in code flow?  
**Answer:** No, it contains a code for later exchange.

**Sources:** Chapter §3; RFC 6749 §4.1. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 05 — PKCE protects code redemption

**Learning objective:** Understand challenge first and verifier later.

**On-slide text**

- Client generates secret verifier V
- Authorization request sends derived S256 challenge
- Token request sends original verifier V
- Server verifies match and code validity

**Teaching explanation:** Public authorization-code clients must use PKCE under the OAuth security BCP; confidential clients should also use it. The client retains a fresh secret verifier while sending only the derived S256 challenge at the authorization endpoint. Keycloak binds the challenge to the authorization code and later compares it with the verifier during redemption. A correct verifier cannot revive an expired code, and a confidential backend still uses its registered client authentication.

**Diagram or worked example:** PKCE H and V on separate lanes, with an explicit expired-code rejection counterexample.

**Self-check:** Can PKCE replace a confidential client's authentication method?  
**Answer:** No.

**Sources:** Chapter §3; RFC 7636; RFC 9700. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 06 — BFF, token mediator and browser OAuth

**Learning objective:** Recognize three browser-application architectures.

**On-slide text**

- BFF: OAuth tokens kept backend-side
- Token-mediator: backend obtains, JS may receive tokens
- Browser client: JavaScript obtains OAuth tokens

**Teaching explanation:** A Backend-for-Frontend can keep OAuth access/refresh tokens on a trusted backend and issue a browser application session cookie. A token-mediating backend may facilitate the exchange while returning API tokens to the browser. A browser-based OAuth client obtains and manages tokens in JavaScript. Each design has different token exfiltration, CSRF, XSS and session boundaries. Choosing Authorization Code alone does not determine where OAuth tokens live.

**Diagram or worked example:** Three lanes from RFC 10017 with browser/token boundaries, no rendered architecture assets.

**Self-check:** Do all browser apps keep OAuth tokens server-side?  
**Answer:** No, only some architectures such as a full BFF.

**Sources:** Chapter §4; RFC 10017. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 07 — Native CLI with browser access

**Learning objective:** Apply the native-app external browser best practice.

**On-slide text**

- Desktop/mobile app is typically a public client
- Use system browser, not an embedded login WebView
- Authorization Code + PKCE
- Safe OS callback/loopback redirect

**Teaching explanation:** A native app cannot protect a shared client secret shipped in an app binary. RFC 8252 recommends using an external browser for authorization, then an app-specific or suitable loopback-IP callback to receive the authorization code. The client verifies the redirect transaction and uses PKCE. Loopback HTTP redirect is a constrained local-only exception, not approval for insecure HTTP redirects over a network. This is normally preferable to using Device Flow for a desktop CLI with browser access.

**Diagram or worked example:** Desktop CLI → system browser → loopback IP callback → token endpoint.

**Self-check:** Is embedding a secret in a CLI binary equivalent to confidential client authentication?  
**Answer:** No.

**Sources:** Chapter §5; RFC 8252. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 08 — When is Device Flow justified?

**Learning objective:** Explain constrained device login and its new risks.

**On-slide text**

- Device shows user code or QR
- User approves on a separate trusted browser
- Client polls token endpoint
- Cross-device consent phishing is possible

**Teaching explanation:** Device Authorization is designed for devices where normal browser-based redirection or user input is impractical. It begins with device/user codes, then the user authorizes on another device. The original client polls until a terminal outcome. Cross-device code/QR transfer does not itself authenticate which physical device started the request; the 2026 BCP requires a risk assessment and suitable mitigations. Do not automatically apply Device Flow to a normal web or desktop client.

**Diagram or worked example:** Two-device sequence with the polling arrow clearly labeled as a request-response, not server push.

**Self-check:** If a CLI can use the system browser, must it still use Device Flow?  
**Answer:** No.

**Sources:** Chapter §§6, 9; RFC 8628; RFC 10027. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 09 — Client Credentials has no human login

**Learning objective:** Describe a machine identity correctly.

**On-slide text**

- Service authenticates to authorization server
- Receives service access token
- Token represents the service/client, not Alice
- API enforces service permissions

**Teaching explanation:** A backend worker can ask Keycloak for an access token using Client Credentials after authenticating under its registered method. In this flow no end user is required to sign in. The API must validate issuer, intended audience and the service's permissions, and avoid mistaking a service-principal subject for a human account. This protects against client-as-user impersonation and overprivileged service-to-service access.

**Diagram or worked example:** Three nodes: notes-worker → Keycloak → notes-api, labeled service principal.

**Self-check:** Does a Client Credentials token prove Alice logged in?  
**Answer:** No.

**Sources:** Chapter §7; RFC 6749 §4.4; RFC 9700. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 10 — Two historical flows to avoid

**Learning objective:** Understand the deprecated security patterns.

**On-slide text**

- ROPC requires client to collect human password
- RFC 9700 says ROPC MUST NOT be used
- Implicit exposes tokens through browser front channel
- New browser apps should use Authorization Code + PKCE

**Teaching explanation:** The password grant directly exposes the user's reusable credentials to an OAuth client, increases the phishing surface and is unsuitable for modern MFA and passkey authentication. Its existence in old provider settings does not legitimize it for new systems. The Implicit grant is also an older browser-era pattern that avoids the back-channel code exchange and has been superseded by safer Authorization Code patterns. Teach these only to recognize and replace legacy designs.

**Diagram or worked example:** Two obsolete branch cards labeled historical, with safer replacement shown.

**Self-check:** Is the password grant acceptable because Keycloak has a Direct Access Grants option?  
**Answer:** No, RFC 9700 says it MUST NOT be used.

**Sources:** Chapter §8; RFC 9700; RFC 10017. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 11 — Flow security continues after issuance

**Learning objective:** Emphasize issuer, audience, session and API policy.

**On-slide text**

- Bind request to initiating client/session
- Protect credentials and redirect handling
- Validate correct token at intended API
- Check exact resource action

**Teaching explanation:** Flow selection is one aspect of security. Interactive clients must bind authorization responses to the initiating transaction and trusted issuer. API requests require suitable access tokens checked for signature or introspection, audience, purpose and lifetime, followed by object-level authorization. Token theft, stale claims and deferred operations may require additional controls. A grant is not a universal access policy, and correctly using PKCE does not remove API security checks.

**Diagram or worked example:** End-to-end sequence with authentication, token issuance and separate API permission decision.

**Self-check:** Can a correctly signed token for billing-api authorize notes-api?  
**Answer:** No, wrong audience.

**Sources:** Chapter §§3, 9, 11; RFC 9700. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 12 — Pick the grant in four scenarios

**Learning objective:** Test flow selection without memorizing vendor UI.

**On-slide text**

- Web login → Code + PKCE, architecture-aware
- Desktop CLI with browser → Code + PKCE
- TV with remote → risk-assessed Device Flow
- Backend service → Client Credentials

**Teaching explanation:** A class should justify each scenario. A web login needs a browser-based authorization flow and suitable BFF/browser architecture; a desktop app with an external browser can use Authorization Code + PKCE; a truly constrained television may use Device Authorization if phishing risks can be mitigated; and a machine service calls an API as a service principal using Client Credentials. None of these flows permits Alice to read someone else's notebook without API authorization.

**Diagram or worked example:** Four exam cards, each with a flow answer, a caveat and one failure test.

**Self-check:** What should be checked even after selecting the correct grant?  
**Answer:** The access token and the exact resource policy.

**Sources:** Chapter §§1–12; RFC 9700; RFC 10027. [Chapter](../docs/02-authentication-flows.md) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

