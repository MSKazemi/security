# Technical teaching slides — JWT vs JWK vs JWKS

**Format:** 12 detailed text-first slides, not a rendered or branded presentation.  
**Canonical technical chapter:** [JWT vs JWK vs JWKS](../docs/15-jwt-vs-jwks-verification.md).  
**Audience:** students, developers and engineers studying authentication and API security.

Every slide includes learner-facing text, teaching notes, a conceptual illustration and a question. Fictional values only.

---

## Slide 01 — JWT, JWK and JWKS

**Learning objective:** Identify which object is a token, a key, or a key set.

**On-slide text**

- JWT = claims format
- JWK = one JSON key
- JWKS = a set of keys
- key information does not itself authorize API calls.

**Teaching explanation:** A JWT carries claims. A JWK represents one cryptographic key in JSON, and a JWKS organizes several keys in a keys array. In the common asymmetric Keycloak pattern, Keycloak signs with a protected private key and makes corresponding public keys available. The API needs trusted keys to verify a signature, but must still validate issuer, audience and the resource operation.

**Diagram or worked example:** Draw a signed letter, one verification key and a directory containing keys. Add a separate API permission gate.

**Self-check:** Does a JWKS decide whether Alice may read Bob's notes?  
**Answer:** No, the resource API applies its own authorization.

**Sources:** Chapter §§1–2; RFC 7517; RFC 7519. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 02 — A signed token has three parts

**Learning objective:** Separate Base64URL decoding from cryptographic verification.

**On-slide text**

- header.payload.signature
- Base64URL is encoding
- reading claims is not proving validity.

**Teaching explanation:** A typical signed JWT serialized as a JWS contains Base64URL-encoded header, payload and signature segments. Anyone who has the token can normally read its decoded claims. An attacker can forge readable parts without knowing the signing key. Cryptographic signature verification and trusted key/algorithm selection are required before using the claims, followed by claim checks.

**Diagram or worked example:** Show three parts of a fictional signed JWT and label the decoded payload UNVERIFIED.

**Self-check:** Can decoding establish whether Keycloak issued a JWT?  
**Answer:** No.

**Sources:** Chapter §3; RFC 7515; RFC 7519. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 03 — JWS vs JWE

**Learning objective:** Explain signing and encryption as separate properties.

**On-slide text**

- JWS = signed/MAC-protected
- JWE = encrypted
- compact JWS often 3 parts
- compact JWE 5 parts.

**Teaching explanation:** JWT is a claim format that can be carried in JWS or JWE. A compact JWS provides integrity/authenticity under a trusted key but is usually readable. JWE provides encryption and generally appears in five segments in compact serialization. Nested signed and encrypted tokens can exist. Never teach that all JWTs are encrypted or that all JWTs have exactly three parts.

**Diagram or worked example:** Compare JWS three segments with JWE five; draw signature and confidentiality as separate features.

**Self-check:** Does a signed JWT automatically hide its contents?  
**Answer:** No.

**Sources:** Chapter §§2–3; RFC 7515; RFC 7516. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 04 — Who owns the signing keys?

**Learning objective:** Trace the issuer/API trust boundary.

**On-slide text**

- Issuer protects private signing key
- API uses trusted public verification key
- Keycloak certs publishes public keys.

**Teaching explanation:** For asymmetric signing such as RS256, the issuer protects the private key and the API verifies signatures using its public counterpart. The API need not obtain the private key. Generic JWKs can also describe private or symmetric keys, so a public OIDC certs endpoint is special: it exposes selected public verification keys, not private signing material. Symmetric MACs like HS256 require another key management pattern.

**Diagram or worked example:** Keycloak with private key on one side; notes-api with public key on the other.

**Self-check:** Should the API download a realm's private key from JWKS?  
**Answer:** No.

**Sources:** Chapter §4; RFC 7517; Keycloak OIDC docs. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 05 — Don't trust the JWT header

**Learning objective:** Treat kid and alg as untrusted input.

**On-slide text**

- kid = candidate key hint
- alg = claimed algorithm
- typ = token type as specified
- all must obey verifier policy.

**Teaching explanation:** A forged token can contain a believable kid or request an unsafe algorithm. The API should select candidate keys only from the trusted issuer's set and enforce its own allowlist of algorithms and key types. It should also check the expected token type according to its token profile. A kid matching a trusted key does not verify the token until its signature checks out.

**Diagram or worked example:** Label a fictitious JSON header with kid key-A, alg RS256 and typ JWT; stamp it UNTRUSTED.

**Self-check:** Does a plausible kid prove the signature is valid?  
**Answer:** No, it only helps select a candidate key.

**Sources:** Chapter §5; RFC 8725. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 06 — What is inside a JWKS?

**Learning objective:** Read the public key-set structure.

**On-slide text**

- JWKS contains keys array
- each entry is a JWK
- RSA fields may include kty, n and e
- kid distinguishes keys.

**Teaching explanation:** A JWK Set is a JSON object whose keys member is an array. For public RSA keys, kty names the algorithm family, n is the modulus and e is the exponent; kid, use and alg may be present. Other approved public key types may appear. A generic JWK can hold sensitive material, so do not publish arbitrary JWK files. Keycloak's certs endpoint is specifically intended to share public verification keys.

**Diagram or worked example:** Draw a keys array containing two fake public RSA JWK entries labeled key-A and key-B.

**Self-check:** Is every JWK automatically safe to make public?  
**Answer:** No.

**Sources:** Chapter §6; RFC 7517. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 07 — Find the trusted key source

**Learning objective:** Use trusted issuer metadata rather than token-provided URLs.

**On-slide text**

- Configure issuer
- discover jwks_uri
- verify HTTPS in production
- reject arbitrary jku/x5u sources.

**Teaching explanation:** OIDC provider metadata from a configured trusted issuer can advertise jwks_uri. The API should use that preconfigured issuer relationship to fetch and cache keys, with suitable TLS and key-selection controls. Attacker-supplied JWT header URLs such as jku and x5u are not authorization to contact arbitrary servers and may cause SSRF or key substitution. The token must never choose its own trust anchor.

**Diagram or worked example:** Trusted realm → discovery document → jwks_uri → JWKS cache. Cross out the arrow from an attacker-supplied URL.

**Self-check:** Who chooses the allowed JWKS source?  
**Answer:** The API's trusted issuer configuration.

**Sources:** Chapter §7; RFC 8725; Keycloak OIDC docs. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 08 — Validate more than the signature

**Learning objective:** Trace the signature, claim and permission gates.

**On-slide text**

- Choose permitted key/algorithm
- verify signature
- validate iss, aud, exp and purpose
- enforce object permission.

**Teaching explanation:** The API may first use the untrusted kid as a lookup hint into a trusted key cache. Signature validation ensures integrity under that key. It must still verify that the issuer is expected, the token is intended for this API, its lifetime is valid, and its purpose is appropriate. Finally the API checks the requested action and resource policy. A correctly signed token for a different audience is still invalid for this API.

**Diagram or worked example:** Show Chapter §9's decision chart with separate 401 and 403 exits.

**Self-check:** What if the signature is valid but aud belongs to another API?  
**Answer:** Reject the token.

**Sources:** Chapter §§8–9; RFC 8725; RFC 9068. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 09 — ID token is not an API access token

**Learning objective:** Recognize token-type substitution.

**On-slide text**

- ID token → OIDC client
- access token → resource API
- profile typing adds another validation rule.

**Teaching explanation:** An OIDC ID token carries authentication information to its client and is not a bearer access credential for a resource API. APIs should reject a correctly signed ID token presented in place of an access token. RFC 9068 defines one particular JWT access-token profile with required typ at+jwt. A Keycloak deployment does not automatically implement that profile, so token-kind validation needs to reflect the actual issuer and agreed profile rather than assume every token uses the same header type.

**Diagram or worked example:** Two lanes: ID token goes to lesson-web, access token to notes-api; no crossing arrows.

**Self-check:** Can an API accept an ID token because Keycloak signed it?  
**Answer:** No.

**Sources:** Chapter §9; OIDC Core; RFC 9068. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 10 — JWKS caching and key rotation

**Learning objective:** Explain why two public keys may coexist.

**On-slide text**

- New active key signs new tokens
- older public key verifies older valid tokens
- caches refresh from trusted source.

**Teaching explanation:** During Keycloak key rotation, the issuer may start signing with key-B while still publishing key-A for verification of previously issued, unexpired tokens. JWKS caching is useful but must be refreshed in a controlled way. Do not allow unknown kid values to force unbounded remote fetches. Retire previous keys only when doing so is compatible with token, cookie, offline-token and refresh lifetimes. Key rotation is not equivalent to individual token revocation.

**Diagram or worked example:** Draw a timeline: key-A then key-B, with a JWKS overlap period containing both public keys.

**Self-check:** Why keep public key-A after key-B begins signing?  
**Answer:** To verify older tokens that are still valid.

**Sources:** Chapter §10; Keycloak Admin Guide. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 11 — Detect verification shortcuts

**Learning objective:** Identify attacks involving forged headers and wrong audiences.

**On-slide text**

- Decoding ≠ trust
- kid ≠ signature
- algorithm allowlist
- no arbitrary key URLs
- verify audience and scope.

**Teaching explanation:** A common failure is trusting an unverified token too early. Code must never accept the algorithm demanded by an attacker, fetch a key from an arbitrary token-provided URL, accept an ID token as an access token, or skip audience validation. Even after verifying the signature, it must enforce the actual resource permission. Each check is distinct, and the combined policy prevents token confusion and cross-API authorization errors.

**Diagram or worked example:** Display incorrect shortcuts on one side and the proper validation sequence on the other.

**Self-check:** Which single JWT header field proves the token trustworthy?  
**Answer:** None.

**Sources:** Chapter §§5, 7, 9 and 12; RFC 8725. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).


## Slide 12 — Safe Keycloak public-key lab

**Learning objective:** Explore trust metadata without exposing credentials.

**On-slide text**

- Start disposable local realm
- inspect discovery
- find jwks_uri
- read public keys
- trace API checks.

**Teaching explanation:** With a temporary local school-lab realm, inspect the OIDC discovery document and Keycloak certs endpoint using a local browser or curl. Identify the keys array, kid and key type. Compare the expected issuer URI to the discovery issuer, and discuss why a candidate key is not enough without verifying the signed token and authorization. No real access tokens, passwords, private keys or live customer URLs belong in educational screenshots or repositories.

**Diagram or worked example:** A diagram showing metadata, JWKS and the API's validation gates; use symbolic key-A/key-B values.

**Self-check:** Does finding key-A mean any token claiming kid key-A can be accepted?  
**Answer:** No. Verification and claim checks still follow.

**Sources:** Chapter §§7, 11–12; RFC 7517; Keycloak OIDC docs. [Canonical Chapter 15](../docs/15-jwt-vs-jwks-verification.md) · [RFC 7517](https://www.rfc-editor.org/rfc/rfc7517) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers).

