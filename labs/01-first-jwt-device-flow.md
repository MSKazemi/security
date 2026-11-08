# Lab: understand the Device Authorization Flow

**Environment:** disposable local Keycloak test realm and entirely fictional user. No production accounts, hosts, or tokens.

1. Follow the [official Keycloak documentation](https://www.keycloak.org/documentation) to start a local disposable server and register an OAuth public client with Device Authorization enabled.
2. Retrieve discovery metadata from `http://localhost:8080/realms/school-lab/.well-known/openid-configuration` after creating the example realm.
3. Using the advertised device authorization endpoint, request authorization with the example client identifier.
4. Read `verification_uri`, `user_code`, and `device_code`. Treat all as sensitive temporary data.
5. Sign in using a different browser tab and the user code. Poll according to `interval`; handle `authorization_pending` and `slow_down`.
6. Inspect the **locally generated test** access and ID token roles. Never paste tokens into online decoders or commit them.
7. Verify expiry and failure behavior, then destroy the disposable realm.

For exact configuration steps use your installed Keycloak version's guides. The steps above describe the learning sequence, not a complete configuration script.
