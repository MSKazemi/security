# Teaching slides — How Keycloak issues signed JWTs

**Audience:** beginner to intermediate developers learning Keycloak.  
**Canonical source:** [How Keycloak issues a signed JWT](../../docs/04-jwt-issuance.md).  
**Output:** **12 text-first educational slides** for future visual design. No branding, video, animation, soundtrack, or publishing plan.

Each slide includes a learning outcome, concise visible copy, a full explanation, a diagram or example, and a self-check. Fictional classroom identities only.

---

## Slide 01 — The application asks, Keycloak issues

**Learning objective:** Understand who constructs and signs a token.

**On-slide text**

- Application requests tokens using a permitted flow
- Keycloak checks client, grant and policies
- Keycloak assembles and signs the JWT

**Teaching explanation:** After a successful OAuth grant exchange, an authorization server such as Keycloak can issue a signed JWT access token. The running application does not manufacture the Keycloak access token or possess its signing private key. Keycloak verifies the applicable grant, client and permissions before constructing claims and signing them. The resource API later validates and authorizes the request independently. An OAuth access token can alternatively be opaque, depending on issuer configuration.

**Diagram or worked example:** Four-actor diagram from Chapter §2: Alice, lesson-web client, Keycloak, and notes-api. Highlight issuer versus recipient.

**Self-check:** Who creates and signs Keycloak's access JWT?  
**Answer:** Keycloak after an allowed token grant.

**Sources:** Chapter §§1–2; Keycloak OIDC docs. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 02 — Creating a realm is not issuing a token

**Learning objective:** Separate initial configuration from actual issuance.

**On-slide text**

- Realm = identity and signing configuration
- Grant success = occasion for token issuance
- Client registration is not a token

**Teaching explanation:** An administrator can create a realm, configure users and generate signing keys without issuing Alice a JWT. The first JWT is issued only when the relevant token grant succeeds. By contrast, OAuth Authorization Code returns an authorization code during browser redirection, and the access token comes later from the token endpoint. This prevents the mistaken idea that merely registering a client or creating a user should produce a token.

**Diagram or worked example:** Timeline: realm created → client registered → later approved grant → token issued.

**Self-check:** Does a realm's key creation automatically issue Alice's access token?  
**Answer:** No.

**Sources:** Chapter §1; Keycloak OIDC docs. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 03 — Authorization Code + PKCE timing

**Learning objective:** Locate the code and the later token response.

**On-slide text**

- Browser callback receives a short-lived code
- Client exchanges code and PKCE verifier at token endpoint
- Token response may include access and ID tokens

**Teaching explanation:** With Authorization Code + PKCE, the client first generates state and a verifier/challenge, then redirects the browser to Keycloak. After Alice authenticates, Keycloak returns a short-lived authorization code through the registered callback. The real client subsequently exchanges that code and verifier at the token endpoint. If all checks pass, Keycloak can issue an access token and, for applicable OIDC requests, an ID token. The browser redirect itself is not the access-token response.

**Diagram or worked example:** Two clearly labeled arrows: browser redirect carries code; client-to-token endpoint exchange returns tokens.

**Self-check:** Where is the authorization code redeemed?  
**Answer:** At the authorization server's token endpoint.

**Sources:** Chapter §1; RFC 6749; RFC 7636. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 04 — Device Flow begins with codes, not JWTs

**Learning objective:** Explain the initial and final Device Flow responses.

**On-slide text**

- CLI requests device authorization
- User code and device code are NOT access tokens
- Browser approval precedes successful polling

**Teaching explanation:** A CLI or input-constrained client starts Device Authorization Grant, receives a verification URI and codes, and displays instructions. Alice authenticates and approves through a separate browser. The CLI polls the token endpoint, respecting intervals and error responses, until approval or denial/expiry. Only a successful token grant produces the access token. This architecture avoids having Alice enter her password into the CLI. Device codes are transaction artifacts, not resource-server Bearer credentials.

**Diagram or worked example:** Use Chapter §8 sequence; group initial device codes and later access-token response separately.

**Self-check:** Can the CLI use device_code as Authorization: Bearer?  
**Answer:** No.

**Sources:** Chapter §§1, 8; RFC 8628. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 05 — Other grants can also issue tokens

**Learning objective:** Avoid describing every token as an interactive login.

**On-slide text**

- Client Credentials may represent a service account
- Refresh grant may produce renewed access tokens
- Grant policy differs by flow

**Teaching explanation:** A Keycloak service client can obtain access credentials through Client Credentials without Alice logging in, while an already authenticated application's refresh-token flow can obtain new access tokens under issuer policy. The protocol's grant defines which checks happen before issuance. Thus, a diagram labeling every access token as 'Alice just logged in' is technically wrong. Explain flow-specific subjects, scopes, session context and restrictions.

**Diagram or worked example:** Three lanes labeled authorization-code, device, and client-credentials, merging at token endpoint only after checks.

**Self-check:** Does Client Credentials require a browser login for Alice?  
**Answer:** No.

**Sources:** Chapter §1; RFC 6749; Keycloak documentation. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 06 — Where do signed JWT claims come from?

**Learning objective:** Trace built-in metadata and configurable claim sources.

**On-slide text**

- Realm engine: iss, iat, exp policy
- Identity and groups: subject and roles
- Client scopes/mappers: optional claims and audience

**Teaching explanation:** Keycloak assembles token information from realm settings, account or service-account identity, role assignments, effective client scopes/mappers and authentication context. Important standard metadata such as issuer and expiration are commonly generated by the token engine, not fetched from a custom mapper. The same user may receive different claims for different clients or requested scopes. The API must validate these claims according to its own trust policy.

**Diagram or worked example:** Use Chapter §3 source-to-claim diagram with five sources.

**Self-check:** Does every claim need a custom protocol mapper?  
**Answer:** No, many standard values are built in.

**Sources:** Chapter §§3–4; Keycloak Admin Guide. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 07 — A signed JWT's three components

**Learning objective:** Recognize header, payload and signature.

**On-slide text**

- Base64URL(header)
- Base64URL(payload with claims)
- Base64URL(signature)

**Teaching explanation:** A commonly issued signed JWT uses compact JWS serialization: header.payload.signature. The header may identify algorithm and key ID, while payload holds claims such as iss, sub, aud, exp and scope. The signature binds the encoded header and payload to the private signing key. Decoding the content is easy and does not verify it; Base64URL is encoding rather than encryption. Do not include confidential user data unless it is justified and appropriately protected.

**Diagram or worked example:** Three segment diagram with header alg/kid, claims, and signature, not a live token.

**Self-check:** Does Base64URL make the payload secret?  
**Answer:** No.

**Sources:** Chapter §5; RFC 7519; RFC 7515. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 08 — An illustrative token payload

**Learning objective:** Distinguish token claims from user permissions.

**On-slide text**

- iss = configured realm issuer
- aud = notes-api
- scope = notes:read
- API also checks notebook ownership

**Teaching explanation:** A fictional signed token may contain an issuer URL, Alice's subject, notes-api in the audience, expiration, and notes:read scope. None of these means that Alice can read every student's notebook. Authorization should be handled by notes-api using trusted token claims and resource policy. The illustrative JSON in Chapter §5 is not a real signed token and should never be presented as Keycloak's universal token schema.

**Diagram or worked example:** Use a small JSON card with fake values and a separate API permission decision.

**Self-check:** Does notes:read automatically grant Bob's private notebook?  
**Answer:** No.

**Sources:** Chapter §§5, 10; RFC 9068; Keycloak docs. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 09 — Private signing key vs public JWKS

**Learning objective:** Explain signing and verification responsibilities.

**On-slide text**

- Keycloak protects signing private key
- JWKS publishes suitable public verification keys
- API fetches keys from configured trusted issuer

**Teaching explanation:** With asymmetric algorithms, Keycloak signs tokens using its own private signing key. The API verifies signatures using public keys published under a trusted issuer's JWKS metadata, typically obtained through OIDC discovery. The kid header is a key-selection hint, not permission to contact an attacker-chosen URL. The API constrains allowed algorithms and validates issuer, audience, time and token purpose. Key rotation can require controlled JWKS cache refresh.

**Diagram or worked example:** Signing on Keycloak side; verifying with trusted public key on notes-api side.

**Self-check:** Should the client application store Keycloak's private signing key?  
**Answer:** No.

**Sources:** Chapter §§6–7; RFC 7517; RFC 8725. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 10 — Different credentials, different destinations

**Learning objective:** Explain code, access, ID and refresh recipients.

**On-slide text**

- Authorization code → token endpoint
- Access token → intended resource API
- ID token → OIDC client
- Refresh token → token endpoint

**Teaching explanation:** Several credential types can appear in a login sequence. An authorization code is exchanged once and cannot authorize API requests. An ID token describes the OIDC authentication result to the relying party; an access token authorizes access to intended resource servers under API policy. A refresh token requests replacement tokens from the authorization server. Device codes are yet another type of transaction code. Mixing token purposes is a common security bug.

**Diagram or worked example:** Use Chapter §9 diagram with each credential destination labeled and invalid ID-to-API arrow crossed out.

**Self-check:** May notes-api accept an ID token as Bearer access?  
**Answer:** No.

**Sources:** Chapter §9; OIDC Core; RFC 6749. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 11 — Failure cases: issuance and use are separate

**Learning objective:** Explain denied grants and denied API operations.

**On-slide text**

- Invalid grant/PKCE → no access token
- Correctly issued token with wrong audience → API rejects
- Valid access token with no notebook permission → API denies

**Teaching explanation:** Even after a successful login, Keycloak may reject a token grant because a code expired, a verifier mismatched or a client configuration is wrong. Conversely, successfully issuing a signed access JWT is not a guarantee that every resource API should accept it. The target API must validate its audience, token purpose and expiry, then authorize the concrete action. An already-issued JWT can have stale role claims if permissions change later.

**Diagram or worked example:** Two-stage failure tree: token endpoint gate then notes-api validation/policy gate.

**Self-check:** Can a valid signature overcome a wrong API audience?  
**Answer:** No.

**Sources:** Chapter §10; RFC 9700. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## Slide 12 — Explain issuance in one sentence

**Learning objective:** Summarize the end-to-end signed JWT process.

**On-slide text**

- Grant succeeds under issuer policy
- Keycloak builds claims and signs token
- Client receives and protects it
- API validates and checks permissions

**Teaching explanation:** Ask a student to retell the flow: the running client requests a permitted grant; Keycloak checks client and grant, obtains standard and mapped claims, signs its JWT and returns the credential. The client presents an access token only to the intended resource server. The API verifies issuer, signature, audience, expiry and token purpose, then checks resource-specific policy. This summary works for a typical signed JWT but not for every opaque access-token implementation.

**Diagram or worked example:** Single clean source-to-token-to-API diagram; label that it is signed JWT issuance, not all OAuth tokens.

**Self-check:** Who authorizes reading a specific notebook after token issuance?  
**Answer:** The protected API.

**Sources:** Chapter §§1–11; Keycloak OIDC docs. [Canonical chapter](../../docs/04-jwt-issuance.md) · [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

