# Technical slide outline — Keycloak fundamentals

**Audience:** software developers and students unfamiliar with identity management.  
**Level:** beginner through intermediate.  
**Source of truth:** [Keycloak fundamentals](../docs/01-keycloak-fundamentals.md).  
**Learning outcome:** identify where users, client registrations, roles, credentials, session cookies and API permissions actually belong.

All names are generic and fictional. This document supplies technical slide text and fuller learning explanations, not narration or animation production scripts.

---

## Slide 01 — What is Keycloak?

**Learning objective:** Define Keycloak's core role accurately.

**On-slide text**

- Identity and access management software
- Can act as an OAuth 2.0 authorization server
- Can act as an OpenID Connect provider
- Not your web application or protected API

**Teaching explanation:** Keycloak provides identity, authentication and token-issuance capabilities. Applications integrate with it through configured protocols. A separate application may use Keycloak to authenticate a student and receive tokens, while its API enforces authorization for notebooks. Keycloak is an identity infrastructure component, not the code of every application using it.

**Diagram/example:** Three boxes: user, app, Keycloak; separate fourth box: protected API.

**Self-check:** Does Keycloak run the application's business logic? **Not simply by hosting the client's registration.**

**Sources:** [Chapter §1](../docs/01-keycloak-fundamentals.md); [Keycloak docs](https://www.keycloak.org/documentation).

## Slide 02 — Identify four actors

**Learning objective:** Distinguish user, client app, identity provider and resource server.

**On-slide text**

| Actor | Example |
| --- | --- |
| User | Alice |
| OAuth/OIDC client | `lesson-web` |
| Identity provider | Keycloak |
| Protected API | `notes-api` |

**Teaching explanation:** Alice interacts with a frontend. The app initiates login at Keycloak, which authenticates Alice under realm policy. After credentials are issued, the application may contact an API. The API determines whether the request may access the specific notes resource. The browser's role depends on whether the architecture is browser-only or backend-managed.

**Diagram/example:** Use the [chapter §1 relationship diagram](../docs/01-keycloak-fundamentals.md).

**Self-check:** Who must validate access permission for a particular notebook? **The protected resource API.**

**Sources:** [Chapter §1](../docs/01-keycloak-fundamentals.md); [OAuth roles RFC 6749 §1.1](https://www.rfc-editor.org/rfc/rfc6749.html#section-1.1).

## Slide 03 — What is a realm?

**Learning objective:** Understand the realm as a security and administration boundary.

**On-slide text**

- Realm = an identity/security namespace
- Contains users, clients, roles and policies
- Has its own issuer URL and signing configuration

**Teaching explanation:** One Keycloak server can host several realms. Within a realm, administrators configure users, client registrations and related policies. A realm has an issuer identity and security settings. Choosing the correct realm matters because a token issued by an untrusted realm must not be accepted merely because its format looks valid.

**Diagram/example:** Server containing the fictional `school-lab` realm, with labeled internal objects.

**Self-check:** Is a realm the same as an API endpoint? **No, although the realm has issuer-related endpoints.**

**Sources:** [Chapter §2](../docs/01-keycloak-fundamentals.md); [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 04 — Users, groups and roles

**Learning objective:** Distinguish account identity, group membership and role assignment.

**On-slide text**

- User = account identity
- Group = collection of users
- Realm role = realm-defined role
- Client role = role under one client

**Teaching explanation:** Alice and Bob are users. Both may belong to `students`, while a teacher account may have a different role. Groups can carry role mappings. Realm roles and client roles live in different namespaces. Even when a token includes a role, the API needs to check whether the exact operation and resource are permitted.

**Diagram/example:** Alice → Students group → role mapping; API makes separate notebook-level access decision.

**Self-check:** Does the presence of `reader` always authorize reading every object? **No.**

**Sources:** [Chapter §§2, 7](../docs/01-keycloak-fundamentals.md); [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/).

## Slide 05 — Running client vs Keycloak registration

**Learning objective:** Correct the most common “client” misconception.

**On-slide text**

- **Running client:** the application code
- **Client registration:** Keycloak configuration
- Both use the same `client_id`
- Registration does not deploy application code

**Teaching explanation:** A JavaScript SPA, native CLI or Python backend runs the OAuth/OIDC protocol on the application side. Inside Keycloak, the client registration specifies settings such as redirect URLs, authentication options, flows and scopes. The same registered identity connects them; they are not two running applications.

**Diagram/example:** Side-by-side boxes: `lesson-web` app code and Keycloak → Clients → `lesson-web`.

**Self-check:** Does creating the client in Keycloak launch the app? **No.**

**Sources:** [Chapter §3](../docs/01-keycloak-fundamentals.md); [Keycloak OIDC integration](https://www.keycloak.org/securing-apps/oidc-layers).

## Slide 06 — What does Authlib do?

**Learning objective:** Locate a Python OAuth client library in the architecture.

**On-slide text**

- Authlib is a Python protocol library.
- FastAPI + Authlib can be the running OAuth/OIDC client.
- Keycloak separately hosts the client registration.
- The API independently checks permissions.

**Teaching explanation:** In a backend application, Authlib helps implement OAuth/OIDC redirect and token operations. The application initiates the authorization request and handles the callback. Calling `oauth.register(...)` configures local client code; it does not contact Keycloak's administration interface to create a registration. Actual secure deployment needs configured redirect URIs, session protection, client authentication where appropriate and correct token storage.

**Diagram/example:** Use the [chapter §3 app/Keycloak diagram](../docs/01-keycloak-fundamentals.md).

**Self-check:** Does Authlib automatically keep all OAuth tokens on the server? **No; storage is an application design decision.**

**Sources:** [Chapter §4](../docs/01-keycloak-fundamentals.md); [Authlib Web Clients](https://docs.authlib.org/en/latest/oauth2/client/web/).

## Slide 07 — Public vs confidential clients

**Learning objective:** Classify client credential-protection abilities.

**On-slide text**

- Public: cannot securely maintain a shared secret
- Confidential: trusted backend can protect credentials
- Public clients use Authorization Code with PKCE
- Never embed a client secret in browser or installed CLI code

**Teaching explanation:** Browser-delivered code, mobile apps and distributable CLIs cannot reliably hide shared client secrets. A properly secured backend can authenticate itself as a confidential client. RFC 9700 requires PKCE for public clients using the authorization-code flow and recommends it for confidential clients. Client Credentials fits service-to-service access; Device Flow fits input-constrained devices.

**Diagram/example:** Two columns with a browser icon and a backend server; lock icon only on the trusted backend.

**Self-check:** Can an SPA safely hide an OAuth client secret in JavaScript? **No.**

**Sources:** [Chapter §6](../docs/01-keycloak-fundamentals.md); [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 08 — Browser SPA vs Backend-for-Frontend

**Learning objective:** Trace where tokens and sessions live.

**On-slide text**

| Architecture | OAuth client location | Browser carries |
| --- | --- | --- |
| SPA | JavaScript application | Tokens according to design |
| BFF | Trusted backend | Application session cookie |

**Teaching explanation:** A browser SPA performs the OAuth flow in the browser and needs public-client protections. In a full Backend-for-Frontend design, the backend conducts OAuth operations, manages access/refresh tokens in server-controlled storage and uses an application session with the browser. This changes trust boundaries but does not remove requirements for CSRF defense, session expiry, logout or API authorization.

**Diagram/example:** Two separate architecture drawings; never show both patterns mixed into one unlabeled diagram.

**Self-check:** Does a full BFF typically send access tokens to browser JavaScript? **No.**

**Sources:** [Chapter §5](../docs/01-keycloak-fundamentals.md).

## Slide 09 — Signed cookie vs server-side token storage

**Learning objective:** Avoid a subtle but important session-security mistake.

**On-slide text**

- A signed browser cookie is not necessarily secret.
- Starlette's default session contents can be read.
- Full BFF: server-side token store + opaque session cookie.

**Teaching explanation:** Starlette's default `SessionMiddleware` signs cookie session data, protecting against unauthorized modification but not ensuring confidentiality. If access or refresh tokens are stored directly in such a session, those tokens are present in a browser-readable cookie. A full BFF instead keeps tokens in server-controlled storage and sends the browser an opaque session identifier using Secure, HttpOnly and appropriately SameSite cookie settings, with CSRF and lifecycle defenses.

**Diagram/example:** Browser has “opaque session ID”; trusted backend has access/refresh token store. Draw a clear trust boundary.

**Self-check:** Does `request.session` automatically imply backend-only storage? **No.**

**Sources:** [Chapter §5](../docs/01-keycloak-fundamentals.md); [Starlette SessionMiddleware](https://www.starlette.io/middleware/#sessionmiddleware).

## Slide 10 — API validates and authorizes separately

**Learning objective:** Explain why login is insufficient for API access.

**On-slide text**

- Verify the credential and intended API audience.
- Check issuer, signature or trusted introspection and validity.
- Enforce required scopes/roles and object-level permission.
- Common responses: 401 invalid, 403 forbidden.

**Teaching explanation:** Alice may be authenticated and carry a valid access token yet lack permission to read Bob's private notebook. The resource API must check the token's intended audience and applicable security constraints, then evaluate the exact requested action on the exact resource. Receiving a signed JWT does not automatically grant access to anything.

**Diagram/example:** Decision tree: credential valid? → action permitted? → accept, 401 or 403.

**Self-check:** Is a valid signature sufficient to authorize the action? **No.**

**Sources:** [Chapter §7](../docs/01-keycloak-fundamentals.md); [OAuth security RFC 9700](https://www.rfc-editor.org/rfc/rfc9700).

## Slide 11 — Why are some diagram lines dashed?

**Learning objective:** Read technical diagrams without drawing false security conclusions.

**On-slide text**

- Sequence vertical dashed line = lifeline/time
- Sequence solid arrow = often a request
- Sequence dotted arrow = often a response
- Flowchart dotted arrow = relationship as defined by author

**Teaching explanation:** Mermaid sequence and flowchart diagrams use similar-looking syntax for different visual conventions. A participant lifeline represents its presence through time. A dotted response arrow does not mean that the message is weakly protected or insecure. A flowchart's `---` is a solid, unheaded association. Always read the diagram legend.

**Diagram/example:** One request arrow and one return arrow between client and Keycloak, with vertical lifelines.

**Self-check:** Does a dashed arrow indicate failed authentication? **No.**

**Sources:** [Chapter §8](../docs/01-keycloak-fundamentals.md); [Mermaid sequence docs](https://mermaid.js.org/syntax/sequenceDiagram.html).

## Slide 12 — Keycloak mental model and review questions

**Learning objective:** Recall the full relationship in one diagram.

**On-slide text**

- Keycloak manages identities and protocol settings.
- The running client requests login and handles its result.
- APIs validate access tokens and resource permission.
- Registrations, roles, scopes and cookies are different objects.

**Teaching explanation:** A correct identity architecture separates the user, the running app, the Keycloak realm, client registrations and protected APIs. It also separates token purpose from token format and login from authorization. Developers should be able to identify where credentials live and who trusts whom before implementing any flow.

**Diagram/example:** User ↔ application ↔ Keycloak; application → protected API, with distinct labels for session cookie, code and access token.

**Self-check:** Explain where Authlib runs, where a `client_id` is registered, where a refresh token belongs, and where object permission is enforced.

**Sources:** [Full Keycloak fundamentals chapter](../docs/01-keycloak-fundamentals.md); [Keycloak docs](https://www.keycloak.org/documentation).
