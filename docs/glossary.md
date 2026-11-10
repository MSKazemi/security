# Plain-English glossary

| Term | Meaning |
|---|---|
| Authentication | Checking who a user is |
| Authorization | Deciding which actions an identity may perform |
| OAuth 2.0 | Framework for delegated authorization |
| OIDC | Identity layer based on OAuth 2.0 |
| Keycloak | Identity and access management platform |
| Realm | Keycloak's identity/security boundary |
| OAuth client | Software requesting authorization; also registered at the authorization server |
| Resource server | API protecting resources |
| Authorization code | Short-lived artifact exchanged for tokens |
| Access token | Credential presented to protected APIs |
| ID token | OIDC token conveying authentication information to the client |
| Refresh token | Credential that may be used to obtain a new access token, subject to policy |
| PKCE | Proof Key for Code Exchange, protecting code redemption |
| JWT | JSON Web Token: format carrying claims |
| JWK | JSON representation of a key |
| JWKS | Set of JSON Web Keys |
| BFF | Backend-for-Frontend, a backend handling tokens on behalf of a browser |
| Bearer | Whoever possesses a token can present it |
