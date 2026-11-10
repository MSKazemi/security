# Technical slide outline — Realm, User, Client and Client Scope

**Audience:** beginners and engineers learning Keycloak configuration.  
**Canonical chapter:** [Keycloak realm, user, client and client scope](../docs/08-realm-client-user-client-scope.md).  
**Format:** 12 text-first educational slides; no animation, brand palette, platform-specific text or rendered deck.  
**Outcome:** identify each Keycloak object, explain why scopes affect claims, and distinguish token contents from API authorization.

All example accounts, clients and realms are fictional.

---

## Slide 01 — Four objects, four responsibilities

**Learning objective:** Distinguish realm, user, client and client scope.

**On-slide text**

**Realm**: identity/security boundary
**User**: account identity
**Client**: application registration
**Client scope**: reusable token-mapping configuration

**Teaching explanation:** Keycloak organizes identity administration in a realm. Alice's account is a user. The separately running portal has a Keycloak client registration that describes allowed OAuth/OIDC behavior. A client scope groups protocol mappers and role-scope mappings shared across registrations. Neither scope nor client registration is an API authorization decision.

**Diagram or worked example:** Four nested labeled cards: school-lab realm contains Alice, a lesson-web client registration and shared client scopes. Keep the separately running portal outside the realm box.

**Self-check:** Is a client scope another user?  
**Answer:** No. It is configuration affecting token issuance.

**Sources:** Chapter §§1–2; Keycloak Server Administration Guide. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 02 — Where the objects live

**Learning objective:** Read the structural hierarchy correctly.

**On-slide text**

Keycloak server → realm
Realm → users, groups, roles, clients, scopes
A resource API runs separately

**Teaching explanation:** A Keycloak server can host more than one realm. The realm owns its users, client registrations, realm-level roles, scope configuration and issuer policies. A client can also define client roles. An API like notes-api is running application code outside Keycloak; it might have a registration for role or audience settings, but a registration is not the API's deployment.

**Diagram or worked example:** Show the chapter §2 Mermaid hierarchy with a dashed outline separating Keycloak configuration from running services.

**Self-check:** Does creating a notes-api client registration deploy an API?  
**Answer:** No.

**Sources:** Chapter §2; Keycloak Server Administration Guide. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 03 — Who is Alice inside Keycloak?

**Learning objective:** Separate user identity, attributes, groups and roles.

**On-slide text**

User = account
Groups organize users
Roles are assigned capabilities or groupings
Claims are selected information

**Teaching explanation:** An account may have attributes, credentials, group memberships, realm roles and client roles. Group membership can carry role mappings. Not all account attributes should be emitted into every token; the effective client configuration controls which claims are included. The API subsequently decides access for particular resources.

**Diagram or worked example:** Alice's account card with three sections: account attributes, memberships, assigned roles. A small 'selected claims' arrow leads to token issuance.

**Self-check:** Does a user having an email mean every access token needs the email?  
**Answer:** No. Minimize claims.

**Sources:** Chapter §3 and §11; Keycloak Admin Guide. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 04 — Client code versus client registration

**Learning objective:** Explain two uses of the word client.

**On-slide text**

Running client = app code
Registration = Keycloak settings
The same client_id relates them
Registration ≠ deployment

**Teaching explanation:** The browser application, CLI, native app, or FastAPI backend implements OAuth/OIDC on the application side. Keycloak's Clients page has its client_id, redirect configuration, allowed flows, scopes and authentication settings. The two must agree, but Keycloak does not execute that application's business logic. Whether the client is public or confidential depends on its ability to safeguard client authentication credentials.

**Diagram or worked example:** Two adjacent boxes: 'lesson-web application process' and 'Keycloak / Clients / lesson-web registration', linked by client_id.

**Self-check:** Does registering lesson-web in Keycloak launch FastAPI?  
**Answer:** No.

**Sources:** Chapter §4; Keycloak OIDC documentation. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/) · [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html).

## Slide 05 — Why is scope confusing?

**Learning objective:** Distinguish OAuth scope, client scope and role.

**On-slide text**

OAuth scope = requested protocol values
Client scope = reusable Keycloak settings
Role = assigned capability grouping
API policy = concrete permission

**Teaching explanation:** An OAuth request might include scope=openid email. Keycloak's optional email client scope is a reusable collection of mapping settings. Roles belong to user/client role namespaces and can be filtered by role-scope mapping. None of those things automatically determines whether Alice may read Bob's notebook: the API must enforce object-level policy.

**Diagram or worked example:** Four columns from request → Keycloak mapping → token claim → API resource check. Avoid a single 'all-powerful scope' icon.

**Self-check:** Does the email scope grant permission to read emails or notebooks?  
**Answer:** No. It is not a blanket resource authorization.

**Sources:** Chapter §§5, 8 and 11; Keycloak Admin Guide. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 06 — Default client scopes

**Learning objective:** Explain why some mappings apply automatically.

**On-slide text**

Assigned as default
Effective for a client without explicit scope-name request
Mapper configuration still determines claims

**Teaching explanation:** Default client scopes normally supply their mappers and role-scope mappings when issuing tokens for a client. A scope may be effective even if its name was not typed into the authorization request. This does **not** mean every possible claim appears; each mapper's output settings, user data and applicable policies still matter. The exact assignment is a configuration choice, not a universal Keycloak profile.

**Diagram or worked example:** Illustrate lesson-web with profile set to default; two different requested scope values both use effective profile mappings.

**Self-check:** Must the client explicitly request profile if it is assigned as default?  
**Answer:** No, not to activate its default mappings.

**Sources:** Chapter §6; Keycloak Admin Guide, default client scopes. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 07 — Optional client scopes

**Learning objective:** Explain request-dependent scope activation.

**On-slide text**

Optional scope must be assigned
Requested in OAuth scope parameter
Applied only when allowed
Claims depend on mappers

**Teaching explanation:** In the worked example, lesson-web has email assigned as optional, and only this scope contains a mapper that emits Alice's email. A request for scope=openid does not activate it. A request for scope=openid email can activate it when policy allows. This is not a guarantee that any email claim appears in every token: the mapper may target ID tokens or UserInfo but not access tokens, and user data may be missing.

**Diagram or worked example:** Compare two request lanes: openid → email mapper not selected; openid email → optional mapper may run.

**Self-check:** With only an optional email mapper, does scope=openid guarantee an email claim?  
**Answer:** No; the optional scope was not requested.

**Sources:** Chapter §6; Keycloak Admin Guide, optional client scopes. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 08 — What is a dedicated client scope?

**Learning objective:** Correct the dedicated-scope misconception.

**On-slide text**

Client-specific mappers and role-scope mappings
Visible in the Admin Console
Cannot be shared or unlinked
Not a separate reusable REST/storage object

**Teaching explanation:** The dedicated scope view shown for lesson-web represents mappers and role-scope mappings attached directly to that client's configuration. It is an administrative abstraction, not an independent realm-level scope that another client can link. For common mapping behavior across multiple clients, create a reusable client scope at realm level and assign it appropriately instead.

**Diagram or worked example:** One client with its dedicated settings inside a client box; reusable realm client scope outside, assignable to multiple clients.

**Self-check:** Can a second client reuse lesson-web's dedicated scope by linking it?  
**Answer:** No.

**Sources:** Chapter §6; Keycloak Admin Guide, dedicated client scope. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 09 — Protocol mappers choose emitted claims

**Learning objective:** Explain the mapper's role without implying authorization.

**On-slide text**

Attribute or role is available
Mapper selects and formats it
Choose token/UserInfo destinations
Scope policy controls eligibility

**Teaching explanation:** A protocol mapper can take Alice's email or an eligible role and emit an appropriate claim into an ID token, access token, or UserInfo response, according to configuration. Merely adding a mapper does not grant Alice the underlying role or authorize an action. For sensitive fields, configure only the necessary destinations and validate the resulting claim set in a disposable test realm.

**Diagram or worked example:** Follow the Chapter §7 diagram: attribute → email mapper → ID token; dotted optional arrows to access token and UserInfo.

**Self-check:** If a mapper emits 'reader', does that alone mean Alice can read every notebook?  
**Answer:** No; object-level policy remains separate.

**Sources:** Chapter §7; Keycloak Admin Guide, protocol mappers. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 10 — Roles, least privilege and token audience

**Learning objective:** Explain why claims still need limitations.

**On-slide text**

Realm role versus client role
Role-scope mappings limit exposure
Full Scope Allowed is deprecated
API checks audience and object permission

**Teaching explanation:** Client roles and realm roles belong to different namespaces. A token should expose only roles needed for that client's use; mapping rules and user membership both affect eligible claims. Keycloak currently marks Full Scope Allowed deprecated and recommends explicit role-scope mappings rather than broad exposure. At the API, verify intended audience and specific permission, not only that a signed JWT carries a familiar role label.

**Diagram or worked example:** Token with minimal note-reading role to notes-api; wrong audience rejected and Bob's private notes denied.

**Self-check:** Does a valid teacher role guarantee access to every tenant's documents?  
**Answer:** No; the API's resource/tenant policy decides.

**Sources:** Chapter §§8, 11; Keycloak Admin Guide, Full Scope Allowed and audience. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 11 — How objects interact during login

**Learning objective:** Follow a correct conceptual OIDC code flow.

**On-slide text**

Client requests login and scopes
Keycloak authenticates and resolves mapping
Client exchanges code and validates login
API validates access token and permissions

**Teaching explanation:** In Authorization Code with PKCE, the running client initiates an authorization request with client_id and requested scopes. Keycloak authenticates the user, processes the authorization request and returns a code through the browser redirect. The client exchanges the code with the verifier at the token endpoint. Keycloak determines which role mappings and protocol mappers apply. The client validates the OIDC result; the protected API validates the access token intended for it and authorizes the action.

**Diagram or worked example:** Use the Chapter §9 sequence diagram, noting internal Keycloak scope resolution is conceptual not extra network traffic.

**Self-check:** Does the API receive the OIDC ID token as its bearer authorization token?  
**Answer:** No.

**Sources:** Chapter §9; OIDC Core; RFC 6749; Keycloak OIDC docs. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/) · [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html) · [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749).

## Slide 12 — Review and practical test

**Learning objective:** Evaluate client scopes with no real credentials.

**On-slide text**

Inspect Clients → Client scopes → Evaluate
Compare openid and openid email
Check ID token versus access token claims
Verify access separately at the API

**Teaching explanation:** Create a fictional local school-lab realm and lesson-web registration in a disposable Keycloak environment. Assign profile as default and email as optional, inspect the effective mappers, then compare the two OIDC scope requests. Observe differences in token claims using the built-in evaluation interface without publishing tokens. Finish with the question: even if the email and reader claims appear, may Alice open Bob's private notebook? No; the API needs explicit resource-level authorization.

**Diagram or worked example:** A table showing the two input scopes, applicable mapping rules and permitted outputs; finish with a separate API decision gate.

**Self-check:** What is the strongest single mental model from this chapter?  
**Answer:** Client scope shapes token information; API policy decides resource access.

**Sources:** Chapter §§10–12; Keycloak Admin Guide. [Chapter](../docs/08-realm-client-user-client-scope.md) · [Keycloak Administration Guide](https://www.keycloak.org/docs/latest/server_admin/).

