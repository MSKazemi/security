# Self-check questions and answers

1. **Q:** What's the difference between authentication and authorization? **A:** Authentication identifies a user; authorization decides permitted actions.
2. **Q:** Does OIDC replace OAuth 2.0? **A:** No. OIDC adds authentication/identity conventions on top of OAuth 2.0.
3. **Q:** Which token is intended for an API? **A:** An access token with appropriate audience and authorization.
4. **Q:** Can an API accept an ID token as its bearer token? **A:** No. ID tokens are intended for OIDC clients, not as API access tokens.
5. **Q:** Why PKCE? **A:** It binds the code exchange to the client instance that initiated authorization.
6. **Q:** What's a refresh token? **A:** A credential used to request a new access token when allowed by the issuer.
7. **Q:** Is a JWT automatically encrypted? **A:** No; many are signed but readable.
8. **Q:** What should happen when a token audience is wrong? **A:** Reject it, even if the signature is valid.
9. **Q:** Is a Keycloak client registration the running application? **A:** No, it is registration metadata.
10. **Q:** What does a JWKS provide? **A:** Public keys for supported verification operations, not private signing keys.
