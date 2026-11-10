# Technical teaching slides — PKCE, verifier and S256 challenge

**Format:** detailed text-first slide source.  
**Canonical chapter:** [PKCE: verifier, challenge and code exchange](../../docs/10-pkce-generation.md).  
**Audience:** beginner developers through protocol implementers. **Slides:** 12.

No animation, branded visuals or finished presentation is included.

---

## Slide 01 — What problem does PKCE solve?

**Learning objective:** Explain PKCE as defense against intercepted-code redemption.

**On-slide text**

- An authorization code is a redeemable grant.
- PKCE adds a per-login secret proof.
- Code alone is not enough to redeem when PKCE applies.

**Teaching explanation:** A client initiates an OAuth Authorization Code request and later receives an authorization code through a redirect. If another party steals that code, PKCE helps keep it from redeeming the code at the token endpoint unless it also has the matching secret verifier. The client generates that secret itself. PKCE does not prove Alice's identity and does not grant API permissions.

**Diagram or worked example:** Claim-ticket analogy with a separate secret proof; label the analogy's limit.

**Self-check:** Does PKCE replace user authentication?  
**Answer:** No; it protects code redemption.

**Sources:** Chapter §1; RFC 7636. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 02 — Five values and their creators

**Learning objective:** Recognize verifier, challenge, method, code and state.

**On-slide text**

- Verifier = client secret for this request.
- Challenge = client-derived public value.
- Method = S256.
- Code = issued by Keycloak.
- State = request/callback correlation.

**Teaching explanation:** The client generates a cryptographically random verifier and a derived challenge before the authorization request. It sets S256 to tell the server which transform to check. Keycloak later issues a short-lived code after the authorization request succeeds. The separate state value lets the client correlate its callback to the initiating transaction; OIDC nonce may add ID-token transaction binding.

**Diagram or worked example:** Five labeled cards with creator and destination; avoid collapsing code into verifier.

**Self-check:** Does Keycloak generate the code_verifier?  
**Answer:** No, the client does.

**Sources:** Chapter §2; RFC 7636 §§4.1–4.4. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 03 — S256: a precise formula

**Learning objective:** Learn the cryptographic transform and valid verifier format.

**On-slide text**

- Verifier = 43–128 unreserved characters.
- Recommended entropy ≥256 bits.
- Challenge = Base64URL(SHA256(ASCII(verifier))).
- Strip '=' Base64 padding.

**Teaching explanation:** A cryptographically secure random generator can create 32 bytes; Base64URL without padding produces a 43-character verifier. The allowed alphabet is letters, numbers and -._~. Hash the ASCII verifier with SHA-256, then Base64URL-encode its digest with no padding. Base64URL is merely an encoding, not encryption. S256 ensures the challenge does not reveal the verifier in practice when the verifier is sufficiently random.

**Diagram or worked example:** Use the chapter §3 S256 flow diagram; show challenge output to authorization endpoint and verifier retained privately.

**Self-check:** Should the challenge be encrypted or is it derived from the verifier?  
**Answer:** It is derived by hashing and encoding.

**Sources:** Chapter §3; RFC 7636 §4.2. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 04 — Generate a pair locally with Python

**Learning objective:** Understand safe implementation and self-testing.

**On-slide text**

- Use secrets.token_urlsafe(32).
- Use hashlib.sha256.
- Use urlsafe_b64encode without '='.
- Keep generated verifier secret.

**Teaching explanation:** The example Python lab uses the standard library and generates a fresh 32-byte random verifier for every request. It computes its corresponding S256 challenge. The default CLI displays only the challenge; printing a verifier requires an explicit classroom-only flag. In production, keep the verifier bound to the login transaction, not in logs or source control. The lab includes an offline --self-test based on RFC 7636.

**Diagram or worked example:** Show concise Python expressions and a local terminal self-test output; do not display real generated secrets.

**Self-check:** Which library should generate the random verifier?  
**Answer:** A cryptographically secure generator such as Python secrets.

**Sources:** Chapter §4; RFC 7636; labs/pkce_generate.py. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 05 — First request: send challenge, not verifier

**Learning objective:** Trace the authorization endpoint stage.

**On-slide text**

- Client generates V and H=S256(V).
- Browser sends challenge H and method S256.
- Server binds H to authorization request/code.
- Verifier V stays with client.

**Teaching explanation:** The client prepares the authorization request with client_id, redirect_uri, state, scope and the S256-derived code_challenge. The browser follows a redirect to Keycloak; Keycloak does not need the original verifier at this stage. It records an association between the challenge/method and the eventual authorization code. Alice may then authenticate and authorize the request. Do not insert verifier V into the browser URL.

**Diagram or worked example:** Two separate boxes: Authorization GET carries challenge H, client private store retains verifier V.

**Self-check:** When does Keycloak receive V?  
**Answer:** Only at the token endpoint in the later exchange.

**Sources:** Chapter §5; RFC 7636 §§4.3–4.4. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 06 — Second request: prove knowledge of verifier

**Learning objective:** Trace the redemption and Keycloak's decision.

**On-slide text**

- Client receives one-use code.
- Client submits code plus original verifier V.
- Keycloak recalculates S256(V).
- Match plus other checks → issue tokens.

**Teaching explanation:** After the browser callback, the client verifies the transaction (including state as applicable), loads the verifier bound to it, and posts the code and verifier to the token endpoint. The authorization server computes the S256 challenge and compares it with the saved value, while also validating code expiry, single-use, client and redirect binding. Confidential clients authenticate separately. A successful verifier comparison is necessary in a PKCE-bound exchange but never sufficient by itself.

**Diagram or worked example:** Show the Chapter §7 decision flow: valid code? calculate challenge? match? other checks?

**Self-check:** Does an expired code pass just because S256 matches?  
**Answer:** No, independent validity checks still apply.

**Sources:** Chapter §§5–7; RFC 7636 §§4.5–4.6; RFC 6749. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 07 — Stolen code: the attacker lacks V

**Learning objective:** Explain both the protection and its limits.

**On-slide text**

- Attacker captures code A only.
- Attacker sends wrong verifier.
- Token endpoint rejects.
- Legitimate client may still redeem if valid.

**Teaching explanation:** PKCE is designed to stop an intercepted authorization code being used by someone who lacks the original verifier. The attacker may receive an invalid_grant result. This does not guarantee the legitimate exchange eventually succeeds: the code can expire or become invalid. If both code and verifier are stolen, or the initiating application is compromised, PKCE alone cannot save the flow. No production code or network details are needed for this conceptual scenario.

**Diagram or worked example:** Two-lane sequence: attacker has code only; legitimate client has matching verifier. Mark outcomes as conditional.

**Self-check:** Does PKCE guarantee protection when both code and verifier are stolen?  
**Answer:** No.

**Sources:** Chapter §8; RFC 7636; RFC 9700. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 08 — PKCE vs state, nonce and client secret

**Learning objective:** Distinguish independent protections.

**On-slide text**

- PKCE → code exchange proof.
- State → callback transaction correlation.
- Nonce → OIDC ID-token binding.
- Client auth → trusted backend identity.

**Teaching explanation:** PKCE protects a grant against interception or injection attacks through a transaction-specific challenge/verifier. State helps tie an authorization response to its originating user-agent session, while OIDC nonce binds authentication results when used. A confidential client still authenticates at the token endpoint. HTTPS, exact redirect validation, issuer pinning and API token checks remain necessary. Do not teach one of these mechanisms as a substitute for all the others.

**Diagram or worked example:** Four-column responsibility matrix, each with a protected boundary and a common misconception.

**Self-check:** Is a code verifier the confidential client's password?  
**Answer:** No, it is a short-lived request-specific proof.

**Sources:** Chapter §9; RFC 9700; OIDC Core. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 09 — How to configure and observe PKCE in Keycloak

**Learning objective:** Explain a safe, version-aware learning workflow.

**On-slide text**

- Use a disposable realm/client.
- Enable Standard Flow.
- Require S256 where supported.
- Verify browser request includes challenge.
- Verify token request contains verifier.

**Teaching explanation:** Keycloak commonly exposes a PKCE requirement setting under the client's advanced configuration, though navigation changes by release. Use a fictional public-client test with an exact loopback redirect or a secure browser client, and ensure no client secret is embedded in distributable code. Inspect the request **fields**, not real secret values, and verify that a missing or wrong verifier is rejected. For a confidential Authlib BFF, configure S256 while keeping client authentication and session storage as separate concerns.

**Diagram or worked example:** A safe checklist based on Chapter §10; do not reproduce real screenshots, keys or tokens.

**Self-check:** If Keycloak supports PKCE but does not require it, is the client necessarily protected?  
**Answer:** No; the client and server must actually use and enforce it.

**Sources:** Chapter §10; Keycloak Admin Guide; Authlib Web Clients. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 10 — Learn from rejection cases

**Learning objective:** Distinguish code and verifier validity.

**On-slide text**

- Correct verifier + expired code → reject.
- Wrong verifier + valid code → reject.
- Reused code → reject.
- All code, client and PKCE checks valid → possible tokens.

**Teaching explanation:** The verifier is only one of several required checks. Code lifetime and one-time use, registered client, matching redirect URI and transaction binding must all be verified. A matching PKCE hash does not override code expiry or previous consumption. Expose this in a fail-closed decision tree instead of suggesting authentication itself grants unlimited API rights.

**Diagram or worked example:** Chapter §11 failure matrix rendered conceptually as a table with each condition and outcome.

**Self-check:** Code expired at 10:05; V matches at 10:05:10. Are tokens issued?  
**Answer:** No.

**Sources:** Chapter §§7, 11; RFC 6749 §5.2. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 11 — Prove your implementation with a test vector

**Learning objective:** Use the official RFC 7636 vector and format checks.

**On-slide text**

- RFC public verifier:
- dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
- Expected challenge:
- E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM

**Teaching explanation:** A standard vector protects against subtle hash/encoding errors such as accidentally keeping Base64 '=' padding, using normal Base64 instead of URL-safe characters, or hashing the wrong input bytes. Run python3 labs/pkce_generate.py --self-test in a local development environment. This public vector is not a live authentication secret and can safely appear in teaching material. The actual verifier used for sign-in must still be freshly generated.

**Diagram or worked example:** Place fixed public verifier and challenge in two labeled rows and add a 'PASS' indicator for local self-test.

**Self-check:** Should a production app reuse the published RFC verifier?  
**Answer:** Never; it is a known demonstration value.

**Sources:** Chapter §4; RFC 7636 Appendix B. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 12 — Review the full PKCE mental model

**Learning objective:** Combine timing, destinations and defenses.

**On-slide text**

- Client creates V and H.
- Authorization request carries H.
- Callback carries code.
- Token request carries code + V.
- API uses access token, not PKCE values.

**Teaching explanation:** For every PKCE-enabled authorization-code login, the client keeps a fresh secret verifier, sends only its derived challenge through authorization and later proves that verifier while redeeming the code at the token endpoint. Keycloak validates that proof and all other grant conditions before issuing tokens. Neither the code nor verifier is a resource-server credential, and API authorization remains a separate decision. This is the core distinction to retain before designing browser, native or backend integrations.

**Diagram or worked example:** One final sequence map with five labels: verifier, challenge, code, access token and intended API.

**Self-check:** Who generates V, and which endpoint first receives V?  
**Answer:** The OAuth client generates V; only the token endpoint receives it.

**Sources:** Chapter §§1–12; RFC 7636; RFC 9700. [Canonical chapter](../../docs/10-pkce-generation.md) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) · [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

