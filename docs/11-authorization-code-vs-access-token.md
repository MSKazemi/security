# Authorization code vs access token: who receives what?

> **Short answer:** An **authorization code** is a temporary, one-use grant that the OAuth client exchanges at the authorization server's **token endpoint**. An **access token** is a credential that the client presents to an **intended protected API**. They are not interchangeable.

This chapter uses a fictional `school-lab` Keycloak realm, `lesson-web` application, Alice's account and `notes-api`. No real system information or credentials are used.

## 1. Start with a simple analogy

Imagine a student collects a **claim ticket** at reception. The ticket can be exchanged once for a **limited-access pass**. The student presents the pass to a locked resource desk.

- The **authorization code** resembles the claim ticket: temporary, short-lived and meant for **exchange**, not for entering the room.
- The **access token** resembles the limited-access pass: used at a **specific protected resource** and evaluated under that resource's rules.
- **PKCE** resembles an additional proof that the redeemer initiated the same transaction; it is not an account password.
- The desk still decides whether a particular file belongs to Alice. A valid pass never means unlimited access.

**Limit of the analogy:** Real authorization servers also check the registered client, matching redirect URI, transaction binding, code lifetime, code replay and sometimes client authentication. A claim ticket is not literally a user ID.

## 2. Compare the two credentials

| Property | Authorization code | Access token |
| --- | --- | --- |
| Protocol role | One-time **authorization grant** | Credential for a **resource server** |
| Recipient | OAuth client, then **authorization server token endpoint** | **Intended API/resource server** |
| Issued by | Authorization server after successful authorization flow | Authorization server token response |
| Typically delivered via | Browser redirect to the registered callback, using a query parameter in code flow | Back-channel token response to the client in code flow |
| Lifetime | Very short; RFC 6749 recommends **maximum 10 minutes**, provider policy may be shorter | Configured by issuer; no universal duration |
| Reuse | **One-time only**; replay must be rejected | Often valid for repeated requests until expiry/revocation, subject to token policy |
| PKCE | Redeemed with matching `code_verifier` when PKCE applies | No PKCE verifier on normal resource API requests |
| Representation | **Opaque value**, not a token to decode as JWT | May be an **opaque string or JWT** |
| Failure | Expired/reused/wrong verifier may cause `invalid_grant` at token endpoint | Invalid/missing token commonly gives API `401`; insufficient permission commonly gives `403` |

Authorization codes and tokens are **sensitive**. Do not log, post, screenshot or transmit live values in teaching material.

## 3. Four actors and two different destinations

The **running OAuth client** (`lesson-web`) is application-side code. Its **client registration** in Keycloak is server-side metadata. Keycloak hosts an authorization endpoint for browser interactions and a token endpoint for code redemption. The `notes-api` resource server is independent of both endpoints.

```mermaid
flowchart TB
    U["Alice and browser"] -->|"Authorize and authenticate"| K["Keycloak authorization endpoint"]
    K -->|"Redirect with code"| C["lesson-web callback"]
    C -->|"Code plus PKCE verifier"| T["Keycloak token endpoint"]
    T -->|"Access token returned"| C2["lesson-web backend holds token"]
    C2 -->|"Bearer access token"| A["notes-api protected resource"]
    A -->|"Token validation and policy"| P{"Allowed notebook?"}
    P -->|"Yes"| OK["Permitted result"]
    P -->|"No"| NO["Reject request"]
```

**The authorization code never belongs in the API's Bearer header.** Conversely, the access token must not be stuffed into a browser redirect URL in a modern authorization-code design.

## 4. Follow a complete Authorization Code + PKCE login

This is a **Backend-for-Frontend (BFF)** example: the **application backend** manages OAuth tokens and the **browser** receives an application session cookie instead. A browser-only SPA has a different token-storage design.

```mermaid
sequenceDiagram
    autonumber
    actor U as Alice
    participant B as Browser
    participant C as lesson-web BFF
    participant K as Keycloak
    participant API as notes-api
    C->>C: Create unique state and PKCE verifier
    C-->>B: Redirect to authorization endpoint with challenge
    B->>K: Request code with client_id, redirect_uri and scope
    U->>K: Authenticate under realm policy
    K-->>B: Redirect to registered callback with code and state
    B->>C: Deliver code and state
    C->>C: Verify state and retrieve matching verifier
    C->>K: POST token endpoint with code and verifier
    K->>K: Check code lifetime, single use, client and PKCE
    alt Exchange valid
        K-->>C: Access token and OIDC ID token if requested
        C->>C: Validate login and store tokens on backend
        C-->>B: Set secure opaque application session cookie
        B->>C: GET notebook with session cookie
        C->>API: Bearer access token intended for notes-api
        API->>API: Validate access token and notebook policy
        API-->>C: Authorized response or denial
    else Invalid grant
        K-->>C: OAuth error, normally invalid_grant
    end
```

At the token endpoint, a **confidential** client also authenticates according to its configured method. **PKCE does not replace confidential-client authentication**. Token issuance may additionally depend on consent, session, user and authorization policies.

The browser receives the redirect; the **client** completes the code exchange. The protected API never processes the authorization code.

## 5. See the two HTTP requests

First, the browser follows an authorization request. This is an **illustrative query**, not a live command:

```text
GET https://login.example.test/realms/school-lab/protocol/openid-connect/auth
    ?response_type=code
    &client_id=lesson-web
    &redirect_uri=REGISTERED_CALLBACK
    &scope=openid
    &state=RANDOM_PER_LOGIN_STATE
    &code_challenge=S256_DERIVED_CHALLENGE
    &code_challenge_method=S256
```

After authentication, Keycloak redirects to the registered callback with a temporary code and the originally supplied state, or returns an appropriate protocol error. The client verifies the transaction, then exchanges the code **in a separate HTTP POST**:

```http
POST /realms/school-lab/protocol/openid-connect/token HTTP/1.1
Host: login.example.test
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id=lesson-web&code=EXAMPLE_ONE_TIME_CODE&redirect_uri=REGISTERED_CALLBACK&code_verifier=EXAMPLE_VERIFIER
```

The **example** client may also authenticate confidentially, using a separate client authentication method not shown in that schematic form body. Never copy these placeholder values into a real deployment.

Only after receiving a valid access token does the client call its intended API:

```http
GET /notes/mine HTTP/1.1
Host: notes-api.example.test
Authorization: Bearer EXAMPLE_ACCESS_TOKEN
```

**Keycloak endpoint discovery:** Prefer the OIDC discovery document at `/realms/school-lab/.well-known/openid-configuration` over hardcoding URLs. The `.test` hostnames above are reserved examples; they are not deployed services.

## 6. What if the code has expired or been replayed?

Authorization codes are **single use**. Correct PKCE is **not sufficient** if a code is expired or was redeemed before.

```mermaid
flowchart TD
    R["Token endpoint receives code and verifier"] --> C{"Code valid, unused and for this client?"}
    C -->|"No"| X["Reject: invalid_grant or appropriate OAuth error"]
    C -->|"Yes"| D{"Redirect and other grant checks valid?"}
    D -->|"No"| X
    D -->|"Yes"| V{"PKCE verification succeeds?"}
    V -->|"No"| X
    V -->|"Yes"| S["Apply remaining checks and issue tokens"]
```

**Counterexample:** A code was configured to expire at 10:05 and the client redeems it at 10:05:10 using the **correct** PKCE verifier. Keycloak must **reject** the expired code. The five-minute example is hypothetical, **not** a statement of Keycloak's default lifetime.

Normally the token endpoint returns an OAuth `invalid_grant` for an expired or invalid authorization grant, but exact error details depend on the failure and provider. Do not infer success from the correct verifier alone.

## 7. How is PKCE different from the code?

- The **client** creates a fresh high-entropy `code_verifier` before making the authorization request.
- It sends the derived `code_challenge` with `code_challenge_method=S256` to the **authorization endpoint**.
- **Keycloak** associates that challenge/method with the authorization transaction/code.
- Keycloak sends the **authorization code** after the relevant authentication/authorization steps.
- The **client** sends that code **and original verifier** only to the **token endpoint**.
- Keycloak recomputes S256 and compares it to the bound challenge before issuing tokens.

Stolen code **without** the matching verifier is not normally redeemable. If both are stolen, or the attack compromises the initiating client/session, PKCE alone cannot prevent misuse. See [PKCE in detail](10-pkce-generation.md).

## 8. Access tokens, ID tokens and refresh tokens: different roles

| Credential | Intended consumer | Role |
| --- | --- | --- |
| Authorization code | OAuth client at **token endpoint** | Exchange once for tokens |
| Access token | Intended **resource server** | Authorization credential for a particular API |
| ID token (OIDC) | **OIDC relying party/client** | Authenticated identity information |
| Refresh token | **Authorization server token endpoint** | Request new tokens if issued and authorized |

Do **not** use an OIDC ID token as the API's Bearer access token. An API must validate that the **access** token is intended for its audience, is valid and grants the requested permission. It may be a JWT or opaque token depending on the server and resource-server integration.

A client-credentials flow has **no user authorization code**; Device Flow has a different device/user-code exchange. Authorization Code is a common grant, not a prerequisite to all OAuth tokens.

## 9. Security boundaries that still matter

- **Exact registered redirect URIs** and HTTPS protect the flow; native localhost loopback callbacks are a special case addressed by OAuth specifications.
- **Transaction binding:** Use unique authorization requests, PKCE, login CSRF protection, verified redirect/callback state and OIDC nonce handling as appropriate.
- **Client authentication:** A confidential client still authenticates at the token endpoint, even if it also uses PKCE.
- **Issuer selection:** Clients supporting multiple authorization servers must prevent mix-up attacks and bind each callback to the correct server.
- **Token purpose, audience and expiry:** The API validates the access token and concrete resource policy; signature alone is insufficient.
- **Avoid credential leaks:** Do not put access tokens in URL query strings, log code/verifier values, or expose refresh tokens in unsafe browser storage.
- **Revocation model:** A valid, unexpired JWT may not reflect immediate session changes without additional checking. Select sensible lifetime and revocation/introspection approaches.

See [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) for the current OAuth security best current practice.

## 10. How to read the arrows

In Mermaid **sequence diagrams**, `->>` is a solid arrow used here for requests; `-->>` is a dotted arrow used here for responses. The vertical dashed participant line is its **lifeline**, not an error or weaker network protection. In a Mermaid flowchart, `---` is a **solid unheaded** connection, whereas `-.->` is a dotted directed connection. Line style does **not** encode OAuth security guarantees.

## 11. Quick questions

1. **Why do we call an authorization code a grant?** It is exchanged at the authorization server for tokens, subject to its binding and validity.
2. **Can the API accept the code as Bearer?** No.
3. **Does the API normally receive a PKCE verifier?** No, only the token endpoint does.
4. **May the same authorization code be reused?** No, it is single use.
5. **Can the token endpoint accept an expired code with a correct verifier?** No.
6. **Are all access tokens JWTs?** No; an OAuth server may issue opaque tokens.
7. **Does receiving an access token grant access to Bob's notebook?** Not unless that action passes API authorization policy.
8. **Where does a refresh token go?** To the authorization server's token endpoint, never as an API bearer access token.

## Sources and next lessons

- [RFC 6749 §4.1.2 — authorization code response and single-use](https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.2)
- [RFC 6749 §4.1.3 — code exchange](https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.3)
- [RFC 6749 §5.2 — token endpoint errors](https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2)
- [RFC 7636 — PKCE](https://www.rfc-editor.org/rfc/rfc7636)
- [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700)
- [Keycloak OIDC integration documentation](https://www.keycloak.org/securing-apps/oidc-layers)
- [Next: PKCE](10-pkce-generation.md) · [OAuth/OIDC/Keycloak relationship](09-oauth2-oidc-keycloak-relationship.md) · [API token validation](06-api-token-validation.md)

*Generic educational material. Avoid using real credentials or client configuration in public examples.*
