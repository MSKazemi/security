# Technical slide outline — OAuth 2.0 vs OIDC vs Keycloak

**Audience:** curious beginners, computer-science students and software engineers.  
**Level:** beginner through intermediate.  
**Source of truth:** [OAuth 2.0 vs OIDC vs Keycloak](../../docs/09-oauth2-oidc-keycloak-relationship.md).  
**Learning outcome:** distinguish identity, delegated access, client registration, token purpose, and API authorization without conflating them.

Every slide below is **technical teaching material**, not a finished designed deck. The explanations are reusable as classroom notes. All examples are fictional.

---

## Slide 01 — Why is login not the same as permission?

**Learning objective:** Separate authentication and authorization.

**On-slide text**

- **Authentication:** Who are you?
- **Authorization:** May you do this action?
- A successful login does not grant access to every resource.

**Teaching explanation:** Consider Alice signing in to a school notes application. Keycloak can authenticate Alice, but the application still needs a policy to decide whether Alice may open a specific notebook. Permissions can differ by user, notebook, tenant, role, or current context. Login success is an identity event, not universal permission.

**Illustration:** Two gates: an identity check at the entrance and a second, notebook-specific permission decision. Label both decisions explicitly.

**Self-check:** Can Alice read Bob's private notebook after authenticating? **Only with explicit authorization.**

**Sources:** [Chapter §§1, 9](../../docs/09-oauth2-oidc-keycloak-relationship.md); [OAuth framework RFC 6749](https://www.rfc-editor.org/rfc/rfc6749).

## Slide 02 — What does OAuth 2.0 provide?

**Learning objective:** Define OAuth as a delegated authorization framework rather than a user-identity protocol.

**On-slide text**

- A client can obtain permission to access a resource.
- The authorization server issues access credentials.
- The resource server enforces the access decision.

**Teaching explanation:** OAuth defines roles and protocol flows for applications obtaining access on behalf of users, or sometimes without an end user. A client may receive an access token restricted by scope and audience. OAuth alone does not standardize the identity information required for a reliable user sign-in experience. Do not teach “access token = proof of who signed in.”

**Illustration:** Client → authorization server → access token → protected API; label every actor.

**Self-check:** Does an OAuth access token automatically function as a login ID card? **No.**

**Sources:** [Chapter §§2, 3](../../docs/09-oauth2-oidc-keycloak-relationship.md); [RFC 6749 §1.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-1.1).

## Slide 03 — What does OpenID Connect add?

**Learning objective:** Explain why OIDC builds on OAuth 2.0.

**On-slide text**

- OIDC adds a standardized authentication layer.
- The client requests `openid`.
- The client receives and validates an **ID token**.

**Teaching explanation:** OIDC reuses OAuth authorization requests and token endpoints, adding rules for authentication and identity claims. A client can learn which user authenticated and information about the authentication event. The OIDC relying party validates the ID token. The API still uses appropriate access credentials and applies resource authorization independently.

**Illustration:** OAuth authorization foundation, OIDC identity layer above it, and two distinct token destinations.

**Self-check:** Does OIDC eliminate the need for API authorization? **No.**

**Sources:** [Chapter §6](../../docs/09-oauth2-oidc-keycloak-relationship.md); [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html).

## Slide 04 — Where does Keycloak fit?

**Learning objective:** Distinguish a product from the protocols it implements.

**On-slide text**

- **OAuth 2.0** = authorization framework
- **OIDC** = identity protocol on top of OAuth
- **Keycloak** = identity and access management software

**Teaching explanation:** Keycloak can act as an OAuth authorization server and an OIDC OpenID Provider. It manages realms, accounts, client registrations, roles, identity federation and authentication policies. Neither Keycloak nor JWT is a competing alternative to OAuth/OIDC; they occupy different architectural categories.

**Illustration:** Three labeled layers: protocol framework, identity extension, implementing software. Draw arrows “extends” and “implements”; do not depict all three as equal alternatives.

**Self-check:** Is Keycloak itself an OAuth token format? **No.**

**Sources:** [Chapter §§2, 3](../../docs/09-oauth2-oidc-keycloak-relationship.md); [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers).

## Slide 05 — Who are the participants?

**Learning objective:** Identify user, client, identity provider, and API.

**On-slide text**

- Alice = user
- `lesson-web` = running client application
- Keycloak = authorization server / identity provider
- `notes-api` = protected resource server

**Teaching explanation:** The browser, application, Keycloak and API have different trust responsibilities. Keycloak stores the `lesson-web` client registration, but that does not run the application. The resource server is the destination for appropriate access tokens and must verify and authorize operations.

**Illustration:** Four boxes with one arrow for login redirection and another for access-token API calls. Add an explicit separation line between the browser and backend in a BFF design.

**Self-check:** Is the registered `client_id` equivalent to deploying the application? **No.**

**Sources:** [Chapter §§3, 5](../../docs/09-oauth2-oidc-keycloak-relationship.md); [Keycloak fundamentals](../../docs/01-keycloak-fundamentals.md).

## Slide 06 — Four credentials, four jobs

**Learning objective:** Identify the correct recipient and purpose of each credential.

**On-slide text**

| Credential | Intended job |
| --- | --- |
| Authorization code | Redeem at token endpoint |
| Access token | Present to intended API |
| ID token | Describe authentication to OIDC client |
| Refresh token | Request renewed access from token endpoint |

**Teaching explanation:** An authorization code is short-lived and normally single-use. Access tokens are for protected resources and need audience and authorization checks. ID tokens convey authenticated identity information to the OIDC client. Refresh tokens are not API credentials; they can request new access tokens if the issuer's policy allows. Access tokens may be opaque or JWT-formatted, whereas OIDC ID tokens are JWTs.

**Illustration:** Four labeled token cards traveling to **different** recipients. Never draw an ID token entering the protected API as authorization.

**Self-check:** Can an ID token replace an API access token because both may be signed? **No.**

**Sources:** [Chapter §4](../../docs/09-oauth2-oidc-keycloak-relationship.md); [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html).

## Slide 07 — Authorization Code with PKCE

**Learning objective:** Understand why the client exchanges a code and how PKCE protects redemption.

**On-slide text**

1. Client initiates authorization and sends an S256 challenge.
2. Keycloak redirects with an authorization code.
3. Client sends the original verifier to the token endpoint.
4. Server verifies the binding before issuing tokens.

**Teaching explanation:** The client creates a high-entropy `code_verifier` and sends an S256-derived `code_challenge` during authorization. At the token endpoint, it sends the original verifier alongside the code. Keycloak checks that the verifier matches the stored challenge. PKCE helps prevent intercepted authorization codes from being redeemed by a party that lacks the verifier. It does not replace HTTPS, redirect URI validation, transaction state or proper client authentication where required.

**Illustration:** Two linked paths: initial challenge and later verifier; show the SHA-256/Base64URL relationship between them.

**Self-check:** Is the original verifier sent in the initial authorization URL? **No.**

**Sources:** [Chapter §8](../../docs/09-oauth2-oidc-keycloak-relationship.md); [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636).

## Slide 08 — A complete login with a backend

**Learning objective:** Trace the BFF version of an OIDC login.

**On-slide text**

`Browser → Backend → Keycloak → Backend → API`

- Browser follows redirects.
- Backend exchanges the code and holds OAuth tokens.
- API validates an access token and the requested operation.

**Teaching explanation:** In a Backend-for-Frontend architecture, the browser visits the application and is redirected to Keycloak. After authentication, the browser follows a redirect back carrying an authorization code and state. The trusted backend verifies the transaction, exchanges the code, validates the OIDC result and creates a server-managed session. When the browser requests notes, the backend calls the separate API with an appropriate access token.

**Illustration:** Use the [complete BFF sequence diagram in chapter §5](../../docs/09-oauth2-oidc-keycloak-relationship.md) as the authoritative technical diagram. Keep the browser session cookie distinct from the OAuth token.

**Self-check:** Does the browser necessarily receive the access token in this BFF design? **No.**

**Sources:** [Chapter §5](../../docs/09-oauth2-oidc-keycloak-relationship.md); [Keycloak OIDC documentation](https://www.keycloak.org/securing-apps/oidc-layers).

## Slide 09 — JWT, JWKS and Bearer are not synonyms

**Learning objective:** Distinguish token format, key representation, and presentation.

**On-slide text**

- **JWT:** format for claims
- **JWKS:** set of keys used for supported verification
- **Bearer:** a token that can be presented by its possessor

**Teaching explanation:** A signed JWT typically contains readable claims plus a cryptographic signature. JWKS exposes JSON Web Keys such as trusted public verification keys; it is not the credential being sent to the API. Bearer describes how many access tokens are presented, usually in the HTTP Authorization header, and does not imply JWT serialization or encryption.

**Illustration:** One signed letter (JWT), a directory of verification keys (JWKS), and a ticket that whoever possesses it may present (Bearer). Clearly label the limits of each analogy.

**Self-check:** Is every OAuth access token a JWT? **No.**

**Sources:** [Chapter §§2, 11](../../docs/09-oauth2-oidc-keycloak-relationship.md); [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519); [JWK RFC 7517](https://www.rfc-editor.org/rfc/rfc7517).

## Slide 10 — Scopes, roles and resource policies

**Learning objective:** Avoid confusing token claims with authorization decisions.

**On-slide text**

- **Scope:** requested delegated access
- **Role:** assigned capability grouping
- **Client scope:** server-side token-mapping configuration
- **Resource policy:** decision for this action and object

**Teaching explanation:** `notes:read` can indicate a type of access being requested or granted, but it does not prove Alice owns every notebook. A Keycloak client scope influences which protocol mappers and role-scope mappings apply. The resource API must independently enforce object ownership, tenant boundaries and policy, using trustworthy token claims and current state as appropriate.

**Illustration:** An allowed request for Alice's notebook next to a denied request for Bob's notebook, even though the same role is present.

**Self-check:** Does a valid `notes:read` scope authorize every notebook? **No.**

**Sources:** [Chapter §7](../../docs/09-oauth2-oidc-keycloak-relationship.md); [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 11 — What must the API verify?

**Learning objective:** Understand token validation and denial.

**On-slide text**

- Correct credential type and trusted issuer
- Signature / trusted validation and intended audience
- Time validity and appropriate scope or role
- Permission for the requested resource

**Teaching explanation:** Signature validation does not by itself establish API access. In a JWT deployment the API validates an allowed signing algorithm, trusted key, issuer, audience, expiration and other applicable constraints. With opaque tokens it may use trusted introspection. It must then check authorization for the concrete resource and action. Incorrect credentials commonly result in HTTP 401; authenticated but forbidden operations commonly result in HTTP 403.

**Illustration:** A decision tree with validation stages leading to **Accept**, **401**, or **403**, matching [chapter §9](../../docs/09-oauth2-oidc-keycloak-relationship.md).

**Self-check:** Would an otherwise valid JWT addressed to another API be accepted? **No.**

**Sources:** [Chapter §9](../../docs/09-oauth2-oidc-keycloak-relationship.md); [OAuth Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 12 — Put it all together

**Learning objective:** Summarize the correct mental model.

**On-slide text**

**OAuth = delegated access**  
**OIDC = authentication identity layer**  
**Keycloak = implementation**  
**API = final resource permission enforcement**

**Teaching explanation:** The authorization server and identity provider manage the identity and credential issuance roles; the application requests the relevant protocol flow and validates the login result; the resource API validates access credentials and permissions. The code, access token, ID token and refresh token are not interchangeable. A good security design keeps both credential purpose and trust boundaries visible.

**Illustration:** One four-actor model showing User → Application ↔ Keycloak and Application → Protected API, with distinct identity and access paths.

**Self-check:** Describe in one minute which component validates the user's login and which component authorizes opening Bob's notebook. **The OIDC client validates the login result; the API enforces the notebook permission.**

**Sources:** [Complete chapter](../../docs/09-oauth2-oidc-keycloak-relationship.md); [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749); [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html); [Keycloak OIDC docs](https://www.keycloak.org/securing-apps/oidc-layers).
