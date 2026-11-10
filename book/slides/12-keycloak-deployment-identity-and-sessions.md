# Detailed teaching slides — Keycloak deployment and identity continuity

**Audience:** developers and students learning secure Keycloak deployment concepts.  
**Canonical chapter:** [HTTPS, stable subject IDs, issuer and sessions](../../docs/12-keycloak-deployment-identity-and-sessions.md).  
**Format:** 12 detailed **text-first** educational slides. No rendered deck, branding, social publishing or animation.

Fictional examples: `school-lab`, Alice, `lesson-web`, and `notes-api`. No real operational source is disclosed.

---

## Slide 01 — Why deployment affects identity security

**Learning objective:** Identify the five operational requirements behind correct OAuth.

**On-slide text**

- HTTPS and browser secure contexts
- Trusted issuer and exact callbacks
- Persistent identity database
- Controlled realm migrations
- Session lifecycle and API policy

**Teaching explanation:** Even flawless Authorization Code and PKCE logic can fail when an application is served on an insecure origin, Keycloak advertises an unexpected issuer, or the identity database is lost. Production readiness requires stable URLs, durable subject identifiers, trust-pinned JWKS keys, controlled configuration updates and separate session/application authorization. Successful localhost login is evidence about one configuration, not proof of these properties.

**Diagram or worked example:** Chapter §1 table mapping each deployment concern to a concrete verification test.

**Self-check:** Does a successful developer laptop login prove Keycloak production security?  
**Answer:** No, it tests only a narrow behavior.

**Sources:** Chapter §1; Keycloak hostname and production docs. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 02 — Why localhost can work when VM HTTP fails

**Learning objective:** Explain secure context and Web Crypto origin rules.

**On-slide text**

- Loopback origins may be potentially trustworthy
- Ordinary HTTP VM origin is not secure
- Web Crypto may be unavailable
- HTTPS is required for network login

**Teaching explanation:** Browsers commonly treat localhost and loopback as potentially trustworthy origins, even over HTTP, but they do not usually grant that exception to a remote HTTP address. Client-side libraries relying on crypto.subtle can therefore succeed locally and fail when served from an ordinary VM IP. Moving PKCE hashing to Python reduces that browser feature dependency but does not secure transmission of cookies, codes or credentials. Use trusted HTTPS for remote deployment.

**Diagram or worked example:** Chapter §2 decision diagram: loopback, remote HTTP, trusted HTTPS; mark risk and Web Crypto availability separately.

**Self-check:** Is moving PKCE to Authlib an alternative to using HTTPS?  
**Answer:** No.

**Sources:** Chapter §2; MDN Secure Contexts. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 03 — Exact issuer and public hostname

**Learning objective:** Explain why identity metadata must agree with deployed URLs.

**On-slide text**

- Issuer appears in discovery and JWT iss
- API pins exact trusted issuer
- Keycloak hostname drives public links
- Wrong Host/forwarded header can poison URLs

**Teaching explanation:** The issuer identifier is part of the token trust boundary. Keycloak advertises its public identity through OIDC discovery and token claims. A resource API should require the exact configured issuer, not accept a similar-looking private URL. The hostname setting and trusted proxy routing must be deliberate because dynamically accepting untrusted forwarded host values can lead to malicious callback or generated links. The public user-facing origin and protected network routes may differ under controlled configuration.

**Diagram or worked example:** Chapter §3 diagram with browser, public issuer, BFF, API and trusted JWKS address.

**Self-check:** Can the API accept any iss value from a server it can reach?  
**Answer:** No, issuer is an exact configured trust anchor.

**Sources:** Chapter §3; Keycloak hostname v2. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 04 — JWKS and audience are different settings

**Learning objective:** Disambiguate verification key source and intended API.

**On-slide text**

- JWKS supplies trusted public keys
- iss identifies the trusted issuer
- aud identifies intended API
- kid is only a key lookup hint

**Teaching explanation:** A resource server can fetch public signing keys from an approved issuer's JWKS, sometimes via an internal route that remains tied to the expected public issuer. This does not change the issuer string in accepted tokens. An API also checks that its own audience is in the access token; creating a client registration or using Keycloak's public keys cannot replace the aud check. Never follow a JWT-supplied arbitrary JWKS URL.

**Diagram or worked example:** Trust chain diagram: configured issuer → metadata → approved keys → signature; separate aud gate.

**Self-check:** If a token is correctly signed, is it valid for any API?  
**Answer:** No, the API must be its intended audience.

**Sources:** Chapter §3; RFC 8725; Keycloak docs. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 05 — Remote redirect is not a local callback

**Learning objective:** Explain exact redirect URIs and browser network location.

**On-slide text**

- localhost means the current requesting machine
- Remote app needs public registered callback
- Redirect URI must match the actual client setup
- Native loopback apps are a separate exception

**Teaching explanation:** A remote web application may be hosted on a server while Alice uses a laptop browser. A redirect URI pointing to localhost points back to the browser's machine, not to the remote server. Configure the true HTTPS callback and ensure Keycloak's allowlist matches it. Native apps with loopback callbacks have a special registered pattern under RFC 8252, but that does not excuse insecure remote HTTP redirects. Check browser origins and post-logout redirects too.

**Diagram or worked example:** Two machines shown with localhost labels; highlight which device handles each address.

**Self-check:** Does localhost on Alice's laptop refer to a remote BFF server?  
**Answer:** No.

**Sources:** Chapter §4; RFC 8252. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 06 — Persistent subject IDs protect ownership

**Learning objective:** Trace why lost identity state can hide existing resources.

**On-slide text**

- Resource record stores issuer plus subject
- Alice's old sub may be A123
- Recreated account may have new sub B456
- Same username is not identity continuity

**Teaching explanation:** A notebook API may associate each record with a trusted issuer and subject identifier. If Keycloak's database is destroyed and an account is recreated with the same visible username, its new sub can differ. The notebook can remain in the application database but no longer appear in owner-filtered queries. Treat user ID migration and ownership reassociation as security-sensitive operations requiring explicit verification; do not assume an email match proves identity equivalence.

**Diagram or worked example:** Chapter §5 old/new subject flow: A123 notebook and B456 new account, resulting in rejected owner match.

**Self-check:** Can a recreated Alice account automatically inherit all resources by email match?  
**Answer:** No.

**Sources:** Chapter §5; OIDC Core; Keycloak database docs. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 07 — Restart and recreate are not the same

**Learning objective:** Compare persistence scenarios safely.

**On-slide text**

- Process restart keeps DB if preserved
- Container recreation may preserve external DB
- Ephemeral DB deletion loses identity
- Backup/restore needs consistency tests

**Teaching explanation:** An application restart can reuse the same persistent identity database; recreating a container with a supported external database can also preserve subjects. By contrast, rebuilding a development instance with ephemeral storage may reset users, credentials and identity relationships. Testing only restart is weaker than testing recreation and recovery. Avoid destructive volume-removal commands in a shared environment. Realm JSON exports cannot replace consistent backups of all identity and session state.

**Diagram or worked example:** Chapter §6 deployment-event table with green continuity and warning loss scenarios.

**Self-check:** Is exported realm JSON automatically a complete backup of all Keycloak state?  
**Answer:** No.

**Sources:** Chapter §6; Keycloak import/export guide. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 08 — Startup realm import vs live migration

**Learning objective:** Explain why JSON edits may be skipped on restart.

**On-slide text**

- --import-realm initializes absent realm
- Existing realm is skipped
- New JSON does not overwrite live realm
- Use reviewed Admin API/config migrations

**Teaching explanation:** Keycloak's startup --import-realm process reads initial realm JSON but skips any realm already present in its database. Updating a mounted file followed by restart may not change a live client callback, role or protocol mapper. Administrators should use controlled, versioned migration mechanisms and verify the resulting realm via trusted APIs or Admin Console. The separate offline import command has different overwrite behavior and must not be conflated with startup import.

**Diagram or worked example:** Chapter §7 decision flow: exists? skip else import; separate migration for existing realm.

**Self-check:** Does --import-realm reapply edits to an already existing realm every restart?  
**Answer:** No.

**Sources:** Chapter §7; Keycloak import/export. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 09 — 401, 403 and 404 after identity changes

**Learning objective:** Interpret API error codes without leaking resources.

**On-slide text**

- 401: credential invalid or missing
- 403: authenticated but forbidden
- 404: absent or deliberately hidden resource
- Subject drift may produce owner-filtered 404

**Teaching explanation:** An API may return 401 when an access token is invalid or missing. It generally returns 403 when a valid caller lacks permission. When revealing the existence of a resource would be sensitive, RFC 9110 allows 404 as an alternative to disclose less. A lost Keycloak identity database can generate a different subject and cause an owner-scoped notebook query to find nothing even though the notebook record remains. Investigate identity continuity and disclosure policy, not just the numeric status code.

**Diagram or worked example:** Decision diagram linking token validity, owner-sub match and 401/403/404 outcomes.

**Self-check:** Can 404 indicate an authorization decision?  
**Answer:** Yes, if policy hides resource existence.

**Sources:** Chapter §8; RFC 9110. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 10 — Session state is broader than JWT validity

**Learning objective:** Separate BFF session, Keycloak SSO, access and refresh tokens.

**On-slide text**

- BFF cookie/session is app-owned
- Keycloak SSO session is issuer-owned
- Access JWT may stay valid until expiry
- Refresh grant and logout have own semantics

**Teaching explanation:** An application may maintain an opaque session cookie while Keycloak keeps its own single-sign-on state. The OAuth access token is another credential with its own lifetime, and a refresh token may allow renewal until invalidated or expired. Local logout removes an app session; IdP logout has separate protocol effects; existing self-contained access JWTs may remain valid until expiry unless the API checks current status. Session, issuer, identity persistence and authorization deserve distinct tests.

**Diagram or worked example:** Four swimlanes: app cookie, protected session record, Keycloak SSO, access/refresh tokens.

**Self-check:** Does deleting app cookie always revoke an unexpired access JWT?  
**Answer:** No.

**Sources:** Chapter §9; RFC 9700; BFF chapter. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 11 — Protect management and sensitive stores

**Learning objective:** Describe administrative and reverse-proxy hardening.

**On-slide text**

- Protect admin UI and REST API
- Do not commit bootstrap/DB credentials
- Overwrite untrusted proxy headers
- Keep session/identity stores off public networks

**Teaching explanation:** Keycloak needs controlled network access to its administrator endpoints, identity database, session stores and key material. A separate admin hostname is useful for routing but does not automatically hide admin REST endpoints on the frontend origin. Trust only proxy-set headers from a controlled reverse proxy and provide proper TLS. Restrict public exposure of database/cache/management services and test secret handling and backups. A single login success or refused weak password does not establish full hardening.

**Diagram or worked example:** Threat-boundary diagram with public OIDC routes and restricted admin/data-plane routes.

**Self-check:** Does a dedicated hostname alone block unwanted admin REST access?  
**Answer:** No.

**Sources:** Chapter §10; Keycloak hostname and reverse proxy docs. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

## Slide 12 — Course acceptance matrix for deployments

**Learning objective:** Turn concepts into a safe validation plan.

**On-slide text**

- Compare exact issuer and JWT iss
- Test stable sub across safe recreate
- Verify approved JWKS and exact callbacks
- Test 401/403/404 and logout behavior

**Teaching explanation:** Students should be able to explain why their deployment uses HTTPS, which issuer is trusted, where keys come from, how identity data remains persistent, and how realm configuration changes take effect. A disposable test should check subject continuity after a non-destructive recreate, deny unexpected tokens, handle private notebooks correctly, and keep admin surfaces isolated. No claims of tested production behavior are made just because this document lists expected results.

**Diagram or worked example:** Chapter §11 table with test case, expected observation and trust boundary.

**Self-check:** What would you test beyond a simple Keycloak restart?  
**Answer:** Recreation/restore identity continuity, redirects, issuer and session behavior.

**Sources:** Chapter §§11–12; Keycloak docs. [Canonical chapter](../../docs/12-keycloak-deployment-identity-and-sessions.md) · [Keycloak Hostname](https://www.keycloak.org/server/hostname) · [Realm Import/Export](https://www.keycloak.org/server/importExport) · [MDN Secure Contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

