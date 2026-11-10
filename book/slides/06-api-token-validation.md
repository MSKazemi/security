# Technical teaching slides — API access-token validation

**Audience:** beginner and intermediate software engineers.  
**Content format:** 12 detailed, text-first slides; no rendered deck, branding, animation or platform operations.  
**Canonical chapter:** [API access-token validation](../../docs/06-api-token-validation.md).

All users and service names in the examples are fictional.

---

## Slide 01 — Two gates: credential and permission

**Learning objective:** Distinguish access-token validation from resource authorization.

**On-slide text**

- Gate one: is access token valid for this API?
- Gate two: is this exact action permitted?
- Login success does not unlock all resources.

**Teaching explanation:** A protected API first verifies that an access credential is genuine, current, and addressed to its audience. Separately, it decides whether Alice can access the specific notebook. A general notes:read scope may be necessary but not sufficient if Alice is not the owner. Authentication and resource authorization are different security decisions even when implemented in the same request handler.

**Diagram or worked example:** Two decision diamonds: valid access credential? then allowed on this notebook? with 401 and 403 branches.

**Self-check:** Can Alice read Bob's private notebook after merely logging in?  
**Answer:** Not without a resource-level authorization rule.

**Sources:** Chapter §1; OAuth Bearer RFC 6750. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 02 — Who sends the access token?

**Learning objective:** Identify OAuth client, Keycloak and protected API.

**On-slide text**

- Keycloak issues credential under policy.
- lesson-web presents access token.
- notes-api validates and authorizes.
- Browser cookie and OAuth token are distinct in BFF.

**Teaching explanation:** Keycloak can act as authorization server and issue a signed access JWT or another configured token format. The OAuth client obtains the token and presents it to notes-api. The resource API validates credentials and enforces resource policy. In a Backend-for-Frontend system, the browser may use only an application session cookie and the backend holds the OAuth tokens.

**Diagram or worked example:** Follow Chapter §2 sequence: Keycloak → lesson-web → notes-api, optional trusted JWKS fetch.

**Self-check:** Is the API responsible for validating its received access token?  
**Answer:** Yes, the protected resource must do its own checks.

**Sources:** Chapter §2; OAuth framework RFC 6749. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 03 — What must a JWT validator verify?

**Learning objective:** List policy-bound cryptographic checks before trusting claims.

**On-slide text**

- Allowed signing algorithm and trusted key
- Correct cryptographic signature
- Exact preconfigured issuer
- Expected audience and lifetime
- Agreed access-token profile

**Teaching explanation:** A decoded token is only data, not proof. A JWT-aware validation library should constrain allowed algorithms, verify a trusted public key and the signature, compare issuer and audience to local configuration, check expiration and relevant not-before conditions, and enforce token purpose. Parsing an untrusted JWT header does not authorize changing key sources. After these checks, the application still needs scope and resource-level authorization.

**Diagram or worked example:** Checklist aligned to Chapter §3, with untrusted token data clearly separated from local validator configuration.

**Self-check:** Is a correctly signed JWT automatically acceptable to every API?  
**Answer:** No; audience, purpose and resource policy must also match.

**Sources:** Chapter §3; RFC 8725; RFC 9068. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 04 — Wrong audience, right signature

**Learning objective:** Explain why an otherwise valid token is still rejected.

**On-slide text**

- iss = trusted school-lab
- aud = billing-api
- Target API = notes-api
- Outcome = reject wrong audience

**Teaching explanation:** An authorization server can issue tokens for distinct resource servers. A signed token addressed to billing-api cannot be reused at notes-api. Without audience validation, one application's token could be substituted at another resource. Keycloak registration and roles do not guarantee notes-api is automatically present in every token's audience; configure and test an intended audience claim deliberately.

**Diagram or worked example:** Present a synthetic claims JSON and a red 'notes-api is not in aud' comparison; no working token string.

**Self-check:** Should notes-api accept a token whose aud contains only billing-api?  
**Answer:** No, it is not the intended recipient.

**Sources:** Chapter §4; RFC 8725 §3.9; RFC 9068. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 05 — ID token versus API access token

**Learning objective:** Prevent cross-token substitution.

**On-slide text**

- ID token → OIDC relying party/client
- Access token → intended resource API
- Both may be signed JWTs
- Signature alone does not identify purpose

**Teaching explanation:** An ID token conveys an authentication result to the client application; it is not the API's bearer access credential. A signed ID token may contain sub and exp and verify against the same issuer's public keys, but that does not make it an access token. A validator should implement an agreed access-token profile plus issuer, audience and authorization checks.

**Diagram or worked example:** Two token lanes: ID goes to lesson-web; access goes to notes-api; reject the wrong arrow.

**Self-check:** Can notes-api accept an ID token just because Keycloak signed it?  
**Answer:** No, token purpose and intended audience differ.

**Sources:** Chapter §5; OIDC Core; RFC 9068. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 06 — RFC 9068 is a specific token profile

**Learning objective:** Explain why at+jwt rules are profile-dependent.

**On-slide text**

- RFC 9068: OAuth JWT access-token profile
- typ = at+jwt or application/at+jwt
- Not every provider token follows RFC 9068
- Enforce actual agreed issuer/token profile

**Teaching explanation:** When an issuer and API use RFC 9068, the resource server requires at+jwt typing alongside issuer, audience, signature and lifetime validation. Other deployed Keycloak configurations may use different access-token representations. Therefore, don't mechanically reject valid provider tokens simply for not matching a profile never agreed upon, or accept arbitrary JWTs because they say JWT. Explicit validation rules are necessary for whichever profile is in use.

**Diagram or worked example:** Comparison of RFC 9068-specific versus provider-configured JWT shapes, labeling which rules apply to which profile.

**Self-check:** Must every JWT from every Keycloak installation declare at+jwt?  
**Answer:** No. Only the specific RFC 9068 profile requires it.

**Sources:** Chapter §5; RFC 9068 §4. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 07 — Trust the issuer's JWKS

**Learning objective:** Locate verification keys safely and rotate them.

**On-slide text**

- Configure trusted issuer and JWKS origin
- Use HTTPS and validate discovery metadata
- kid is only a selection hint
- Reject untrusted jku/x5u URLs

**Teaching explanation:** For signed JWTs, the protected API can retrieve public verification keys from a preconfigured trusted Keycloak issuer. It may discover jwks_uri using the trusted issuer's metadata. Keys should be cached with bounded refresh for rotation. Never permit a token's header to instruct the API to fetch arbitrary URLs; that risks signing-key substitution and SSRF. Unknown keys are not a reason to skip cryptographic verification.

**Diagram or worked example:** Trusted issuer → discovery → JWKS → local verification. Cross out token-supplied external URL.

**Self-check:** May an attacker-controlled kid tell the API to trust a new host?  
**Answer:** No, candidate keys must come from trusted issuer configuration.

**Sources:** Chapter §6; RFC 8725; RFC 7517. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 08 — Opaque access tokens and introspection

**Learning objective:** Explain the network-validation alternative to local JWT signature checks.

**On-slide text**

- Opaque token cannot be parsed as JWT
- Use protected RFC 7662 introspection
- Check active, audience and applicable metadata
- Still enforce object-level policy

**Teaching explanation:** An opaque bearer token needs an issuer-approved validation method, often authenticated introspection. The protected API calls a known trusted authorization server endpoint over HTTPS; the response indicates active state and can include audience, scope, issuer, subject and expiration metadata. active=true is not unlimited permission; it does not remove the need to check the requested action and resource. Caching introspection answers improves performance but can delay revocation awareness.

**Diagram or worked example:** Chapter §7 sequence: client → notes-api → trusted issuer introspection → API policy.

**Self-check:** Is active=true sufficient to read any notebook?  
**Answer:** No. Resource-level policy remains essential.

**Sources:** Chapter §7; RFC 7662. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 09 — 401 and 403 are different

**Learning objective:** Choose accurate OAuth Bearer failure responses.

**On-slide text**

- 401: missing or invalid credential
- 403: valid credential, forbidden action
- Bearer challenge for unacceptable credentials
- insufficient_scope is a defined Bearer error

**Teaching explanation:** For an API using Bearer authorization, missing or invalid access credentials generally result in 401 plus a WWW-Authenticate Bearer challenge, with invalid_token when appropriate. A valid token with insufficient scope generally yields 403, potentially using insufficient_scope. An object-level policy refusal commonly yields 403 as well. RFC 6750 also defines error handling for malformed requests; these examples are common patterns, not substitutes for the full protocol.

**Diagram or worked example:** Table with expired token, wrong audience, missing scope and unauthorized notebook owner, with response code.

**Self-check:** What is typical when a valid token cannot read Bob's private notes?  
**Answer:** 403 Forbidden, after validation and policy checks.

**Sources:** Chapter §8; RFC 6750 §3. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 10 — Delayed actions and stale roles

**Learning objective:** Explain time-of-check versus time-of-use authorization.

**On-slide text**

- Permission can change after token issuance
- A valid JWT can be stale
- Recheck sensitive rights at execution
- Consider policy, short lifetimes and revocation

**Teaching explanation:** Suppose Alice requests a notebook export while authorized. Her permission is revoked before the export runs. A previously issued signed JWT may remain unexpired and cryptographically valid, so the application must assess current authorization at execution time for sensitive delayed operations. The appropriate freshness mechanism depends on threat model, perhaps live resource policy, introspection, session invalidation or short token lifetime.

**Diagram or worked example:** Chapter §9 fictional notebook-export sequence. Avoid any internal company queue or infrastructure details.

**Self-check:** Can a signature check alone reveal a newly revoked role?  
**Answer:** Not necessarily; current policy/freshness checks may be required.

**Sources:** Chapter §9; RFC 7662; RFC 9700. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 11 — Security-focused API tests

**Learning objective:** Turn mistakes into expected rejection cases.

**On-slide text**

- Reject wrong issuer and signature
- Reject wrong audience or token kind
- Reject expired tokens
- Deny missing scope or wrong resource owner
- Fail closed on untrusted JWKS

**Teaching explanation:** A test matrix should include missing/invalid Bearer token, wrong audience, expired token, inappropriate ID token, unfamiliar key ID, unsupported algorithm, insufficient scope and notebook ownership denial. Use synthetic tokens or controlled test fixtures only; real credentials never belong in published teaching examples. Tests must cover not only happy-path authentication but also denied resource operations.

**Diagram or worked example:** Chapter §10 matrix as a readable table of input scenario and expected outcome.

**Self-check:** What should happen when JWKS cannot establish a valid key?  
**Answer:** Reject rather than skipping signature verification.

**Sources:** Chapter §10; RFC 6750; RFC 8725. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

## Slide 12 — Complete acceptance mental model

**Learning objective:** Connect every verification and authorization boundary.

**On-slide text**

- Extract appropriate Bearer credential
- Validate using trusted issuer and profile
- Check audience, time, purpose and policy
- Execute only authorized operation

**Teaching explanation:** An API starts with local security configuration: which issuer it trusts, which token formats it accepts, which signature algorithms and keys are permitted, and which audience identifies the resource. It validates the access token, determines the principal under trustworthy context, then uses current policy to decide the exact action on the resource. JWTs and opaque tokens require different validation paths, but neither skips resource authorization. Keep real implementation inside maintained libraries and audited middleware.

**Diagram or worked example:** One diagram from incoming credential through validation to a notebook-specific allow/deny decision.

**Self-check:** Why is 'signed by Keycloak' insufficient for access?  
**Answer:** The API must still be intended audience and the resource action must be authorized.

**Sources:** Chapter §§1–12; RFC 6750; RFC 7662; RFC 8725. [Canonical chapter](../../docs/06-api-token-validation.md) · [Bearer RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [Introspection RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725).

