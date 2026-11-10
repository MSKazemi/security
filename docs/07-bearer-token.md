# Bearer tokens: what `Authorization: Bearer` really means

> **One sentence:** A **Bearer token** can be presented by **whoever possesses it**. The protected API still has to validate that token and authorize the requested action. **Bearer is a usage model and HTTP authentication scheme, not a JWT format.**

We use fictional `school-lab` Keycloak, `lesson-web`, Alice and `notes-api`. Never expose real bearer tokens, account credentials or production endpoints in demonstrations.

## 1. A pass, not proof of the holder's identity

Think of a temporary pass to read a notebook. A guard can examine whether the pass is **genuine, current, addressed to this place and authorized for the action**. But if someone steals a working bearer pass, the guard cannot establish solely from possession that the presenter is its original recipient.

In OAuth 2.0, **Bearer** means the client generally does not need to prove possession of an additional cryptographic key when presenting the access token. That is why protecting the token against theft is essential.

**Analogy limit:** Real tokens do not grant universal access just because someone has them. APIs validate issuer, token kind, audience, time and permissions.

## 2. The HTTP Authorization header

Illustrative request with an **unusable placeholder**, not a real token:

```http
GET /notes/mine HTTP/1.1
Host: notes-api.example.test
Authorization: Bearer EXAMPLE_ACCESS_TOKEN_NOT_REAL
```

| Part | Meaning | Who supplies it? |
| --- | --- | --- |
| `Authorization` | HTTP header carrying the credential | Running client application |
| `Bearer` | OAuth Bearer authentication scheme (RFC 6750) | Client uses scheme provided by token type |
| `EXAMPLE_ACCESS_TOKEN_NOT_REAL` | Placeholder for an access credential | Authorization server issues real token |
| `notes-api` | Intended protected resource in this classroom | Resource server validates and authorizes |

The preferred Bearer presentation method is the **Authorization header**, not a query-string parameter. Never put real tokens in URLs, screenshots, logs, chats, shared code or public decoding sites. Use HTTPS with appropriate certificate validation.

## 3. Bearer is not JWT

| Term | What it describes | Can it be used interchangeably? |
| --- | --- | --- |
| **Bearer** | Credential possession/presentation scheme | Not a cryptographic token representation |
| **JWT** | Standardized JSON claims token representation | A JWT may be used as an access token, but is not always a bearer token |
| **Opaque token** | String with meaning maintained by the issuer | Can also be an OAuth Bearer access token |
| **ID token** | OIDC authentication result for the relying party | **Not** an API access token |
| **Refresh token** | Credential to request renewed tokens at authorization server | **Not** an API access token |

A signed JWT's signature can establish integrity and the key used to sign it, **if verified under trusted issuer configuration**. It does not prove the current presenter is Alice. Conversely, an opaque Bearer token can be validated through an issuer-approved introspection process.

## 4. How the token reaches the API

```mermaid
sequenceDiagram
    autonumber
    actor U as Alice
    participant B as Browser
    participant C as lesson-web backend
    participant K as Keycloak school-lab
    participant API as notes-api
    U->>B: Open notebook application
    B->>C: Begin login
    C-->>B: Redirect to Keycloak
    B->>K: Authorization request with PKCE challenge
    U->>K: Authenticate
    K-->>B: Redirect with one-time authorization code
    B->>C: Deliver code and state
    C->>K: Exchange code and verifier at token endpoint
    K-->>C: Access token with token_type Bearer if granted
    C->>API: Authorization Bearer access token
    API->>API: Validate intended credential and notebook permission
    API-->>C: Permitted response or rejection
```

This example uses a **Backend-for-Frontend (BFF)**, where OAuth tokens remain in backend-controlled storage and the browser uses an application session cookie. Browser-only SPAs have different token handling, but the resource API's validation responsibilities remain.

The authorization code and PKCE verifier go to the **token endpoint**, not the protected API. The API receives an appropriate **access token**, not an OIDC ID token or refresh token.

## 5. Where does the word Bearer come from?

After a successful OAuth token exchange, the authorization server can return a response like:

```json
{
  "access_token": "EXAMPLE_ACCESS_TOKEN_NOT_REAL",
  "token_type": "Bearer",
  "expires_in": 300
}
```

This is a **schematic example**, not a real response or guaranteed Keycloak default. `token_type=Bearer` identifies the token's usage scheme, while `expires_in` indicates the token response's access-token lifetime in seconds under the actual issuer configuration. The client uses the issued token according to its type and the intended resource server.

Some deployments support **sender-constrained** tokens with other token types, such as **DPoP**. Do not blindly force every OAuth token response into the Bearer scheme.

## 6. What does the API do on receipt?

```mermaid
flowchart TD
    REQ["API receives Bearer access token"] --> FORM{"Credential suitable for this API?"}
    FORM -->|"No"| NO401["401 and Bearer challenge"]
    FORM -->|"Yes"| VALID{"Issuer, signature or introspection,<br/>audience and time valid?"}
    VALID -->|"No"| NO401
    VALID -->|"Yes"| POLICY{"Permitted to perform this action<br/>on this notebook?"}
    POLICY -->|"No"| NO403["403 Forbidden"]
    POLICY -->|"Yes"| OK["Permit operation"]
```

A JWT-aware API normally validates trusted keys, allowed algorithms, exact issuer, audience, token purpose and expiration. An API using opaque tokens may call a **trusted introspection endpoint** to determine token active status and related metadata.

The scope `notes:read` alone is not sufficient to read Bob's private notes: the API still checks object-level policy. See [API access-token validation](06-api-token-validation.md).

## 7. Common errors and status codes

RFC 6750 defines a `WWW-Authenticate: Bearer` response challenge for missing/invalid Bearer credentials and error values such as `invalid_token` and `insufficient_scope`.

| Situation | Typical HTTP result | What to communicate |
| --- | --- | --- |
| No suitable credential | **401 Unauthorized** | Bearer challenge; normally omit detailed error when nothing was supplied |
| Invalid, expired or wrong-audience token | **401 Unauthorized** | `invalid_token` if appropriate |
| Token valid but lacks necessary scope | **403 Forbidden** | `insufficient_scope` if applicable |
| Token valid but Alice cannot read Bob's notebook | **403 Forbidden** | Resource-level authorization denial |
| Token valid and the specific action permitted | **200 OK** for successful read | Return only approved data |

Illustrative authentication challenge:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="school-notes", error="invalid_token"
```

Other malformed requests may have different HTTP statuses, such as 400. Do not expose raw tokens, sensitive validation details or user-account information in responses.

## 8. What happens when someone steals a bearer token?

A stolen **usable** Bearer access token can be presented without Alice's password. The attacker still needs it to pass the intended API's validation and authorization rules, and may be limited by audience, scope, token lifetime and resource policy.

```mermaid
flowchart LR
    K["Issuer grants Bearer access token"] --> C["Legitimate client stores token"]
    C -->|"Normal protected request"| API["notes-api"]
    C -.->|"If token leaks"| X["Unauthorized possessor"]
    X -.->|"Replay attempt while usable"| API
    API --> CHECK{"Valid access token and resource policy?"}
    CHECK -->|"No"| DENY["Reject"]
    CHECK -->|"Yes"| RISK["Bearer alone does not prove original holder"]
```

**Defenses:** TLS, careful storage, short-lived access tokens, least-privilege scopes and audiences, reduced logging, client-side script-injection defenses, revocation/current-policy strategies, and strong application authorization. If work executes later, recheck critical permission at execution time.

A Bearer token is a **sensitive credential**, even when it resembles a readable JWT with a short expiration.

## 9. Bearer vs sender-constrained access tokens

| Model | What a thief typically needs to present a stolen token |
| --- | --- |
| **Bearer** | The valid token itself, within its audience, lifetime and permissions |
| **DPoP sender-constrained** (RFC 9449) | Bound token **plus** proof of possession of the associated private key |
| **OAuth mutual TLS sender-constrained** (RFC 8705) | Bound token **plus** appropriate certificate/private-key proof under mTLS |

DPoP sends a signed per-request proof, with method/URI and other replay-defense fields; DPoP-bound access tokens use the **DPoP** authentication scheme and require resource-server proof validation. A resource server supporting both schemes must **reject DPoP-bound tokens presented merely as Bearer** to prevent downgrade.

**Important:** DPoP and mTLS are not automatically enabled just because a JWT is signed by Keycloak. DPoP also cannot prevent abuse when attacker-controlled code can operate within the legitimate client's execution context. They add defense against token replay under specific threat models, not universal security.

## 10. A safe demonstration without exposing tokens

Using a **disposable local test** and a client with a legitimate test access token, inspect only the *structure* of the HTTP request and the server's response. Do not copy the credential value into learning files.

A schematic shell command:

```sh
# Illustration only. Never paste a real token directly into command text or history.
# A securely populated local environment variable could supply the test token.
curl --fail-with-body \
  --header "Authorization: Bearer ${ACCESS_TOKEN}" \
  https://notes-api.example.test/notes/mine
```

The `.test` domain is deliberately nonfunctional and intended for explanation. In a real disposable lab, protect shell history, process information, debugging output and the token environment. An HTTP command-line demonstration does not replace proper access-control tests.

Try conceptual failure cases: expired access token, wrong API audience, ID token substituted for access token, and valid access token without notebook permission. Only the final case is **valid credential / forbidden resource**.

## 11. Misconceptions and self-check

1. **Does Bearer mean JWT?** No. Bearer is a presentation scheme, JWT a token format.
2. **Can an opaque token be Bearer?** Yes.
3. **Does the caller need Alice's password for every Bearer request?** No.
4. **Does Keycloak's public signing key prove who is holding the token now?** No, it helps verify signature authenticity.
5. **Should an API accept an ID token as an access token?** No.
6. **Does a signed token for a different audience work here?** No.
7. **What is the preferred Bearer transport?** The `Authorization` header over HTTPS.
8. **Is an access token safe to post in an example if it expires soon?** No.
9. **Which status normally applies to a valid but underprivileged token?** 403, sometimes with `insufficient_scope`.
10. **What extra proof can DPoP require?** A request-specific proof associated with the bound key.

## Sources and connected chapters

- [RFC 6750 — OAuth Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- [RFC 6749 — OAuth Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7662 — Token Introspection](https://www.rfc-editor.org/rfc/rfc7662)
- [RFC 9449 — DPoP](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 8705 — OAuth mutual TLS](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 9700 — OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700)
- [Keycloak OIDC integration](https://www.keycloak.org/securing-apps/oidc-layers)
- [Related: API token validation](06-api-token-validation.md) · [Keycloak JWT issuance](04-jwt-issuance.md) · [Device Flow](03-device-flow.md) · [JWT/JWKS](15-jwt-vs-jwks-verification.md)

*Independent security education. No customer or employer systems, private credentials, or real tokens are included.*
