# Lab 1: Issue your first JWT using Keycloak Device Flow

**Goal:** observe a real JWT access-token issuance from Keycloak and learn which component creates the claims and signature.

**Scope:** local Docker lab only; disposable user/realm. Nothing here should be deployed as-is to production. Do **not** paste actual tokens, passwords, device codes or private keys into GitHub, chat, browser-based JWT decoders or screenshots.

**Related chapters:** [Device Authorization Flow](../docs/03-device-flow.md), [How Keycloak issues a signed JWT](../docs/04-jwt-issuance.md) and [JWT vs JWK vs JWKS](../docs/15-jwt-vs-jwks-verification.md). All names (Alice, `school-lab`, `notes-tv`) are fictional.

## Prerequisites

- Docker installed and port 8080 available on loopback.
- `curl`, optionally `jq` for viewing responses.
- Modern browser for Keycloak Admin Console.

## Step 1 — Start a pinned local Keycloak

Use the current stable Keycloak release from the official Docker getting-started page (this lab was first written against 26.8.1 on 2026-11-02) and set it once:

```bash
export KEYCLOAK_VERSION="<current stable tag>"

docker run --rm --name keycloak-school-lab \
  -p 127.0.0.1:8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=local-lab-only \
  quay.io/keycloak/keycloak:"$KEYCLOAK_VERSION" start-dev
```

Open `http://localhost:8080/admin/` and log in as `admin` using the **local example password**. `start-dev` and the bootstrap account are explicitly **not** production security settings.

## Step 2 — Create realm, test user and OIDC client

1. Create a realm called `school-lab`.
2. `Users → Add user`, username `alice`.
3. `Users → alice → Credentials`: assign a **throwaway lab password** and unset “Temporary” if you want normal reusable local login.
4. `Clients → Create client`:
   - Client type: **OpenID Connect**
   - Client ID: `notes-tv`
   - **Client authentication: Off** (public client)
   - Enable **OAuth 2.0 Device Authorization Grant** under capability/authentication-flow configuration.
   - Save. UI names can differ by version; check current Keycloak docs.
5. Optionally inspect `Realm settings → Keys` and `Realm settings → Tokens`.

**Do not enable Password/Direct Access Grant merely for this lab**: we are learning Device Flow, where the CLI does not receive Alice's password.

## Step 3 — Discover metadata and public keys

```bash
curl -sS http://localhost:8080/realms/school-lab/.well-known/openid-configuration
curl -sS http://localhost:8080/realms/school-lab/protocol/openid-connect/certs
```

These publish realm metadata and public signing keys. **Never** expect private signing keys here.

## Step 4 — Request device authorization

```bash
curl -sS -X POST \
  http://localhost:8080/realms/school-lab/protocol/openid-connect/auth/device \
  -d 'client_id=notes-tv' \
  -d 'scope=openid'
```

Keycloak responds with fields like this (**fictional values**):

```json
{
  "device_code": "secret-for-this-local-login",
  "user_code": "ABCD-EFGH",
  "verification_uri": "http://localhost:8080/realms/school-lab/device",
  "expires_in": 600,
  "interval": 5
}
```

At this moment the device has only a pending request; the **first access JWT has not been issued**.

- `user_code` is meant to be typed by Alice.
- `device_code` must stay with the requesting CLI and be protected.

## Step 5 — Log in using another browser tab

Open the `verification_uri` returned by your actual Keycloak server and enter the corresponding `user_code`. Authenticate as Alice and approve the pending request. Only approve a request you knowingly initiated.

## Step 6 — Exchange the device code for tokens

Poll the real token endpoint using the actual `device_code` (do not put real values into GitHub). For a single manual attempt:

```bash
curl -sS -X POST \
  http://localhost:8080/realms/school-lab/protocol/openid-connect/token \
  -d 'client_id=notes-tv' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code' \
  --data-urlencode 'device_code=PASTE_YOUR_OWN_LOCAL_DEVICE_CODE'
```

- If Alice is still logging in: expect `{"error":"authorization_pending"}`.
- If Keycloak responds `slow_down`, **increase** the interval by at least 5 seconds.
- If expired or denied: stop. Restart only when the user initiates a new authorization.
- After approval, the token response contains an `access_token` and possibly `id_token`/`refresh_token` depending on scope and configuration. Keep these secret.

**Important:** A real polling implementation must honor `interval` and deadline, and use backoff on transient errors. Do not run an unbounded tight loop.

## Step 7 — Inspect the token locally without uploading it

A signed JWT consists of header, payload and signature. You may inspect its claims locally, but **decoding does not validate its signature**.

To avoid putting the token into command history, run the following Python snippet and **paste the temporary JWT only into the private terminal prompt**:

```bash
python3 - <<'PY'
import base64, getpass, json
token = getpass.getpass("Paste local LAB access JWT (not echoed): ").strip()
parts = token.split(".")
if len(parts) != 3:
    raise SystemExit("Expected a 3-part signed JWT")
def dec(seg):
    return json.loads(base64.urlsafe_b64decode(seg + "=" * (-len(seg) % 4)))
header, payload = dec(parts[0]), dec(parts[1])
print("Header:")
print(json.dumps(header, indent=2))
print("Payload (UNVERIFIED):")
print(json.dumps(payload, indent=2))
print("This is decoding only, NOT cryptographic verification.")
PY
```

Inspect `iss`, `sub`, `aud`, `exp`, `iat`, `azp` and possible role claims. The actual values depend on your realm, client and client scopes. Do **not** assume `aud` automatically contains an API client you have not configured.

## Step 8 — Understand the cryptographic check

For real API verification use a maintained OIDC/JWT library configured with:
- Exact expected issuer `http://localhost:8080/realms/school-lab` for this **lab only**.
- Correct expected API audience; configure an audience mapper/client role mapping if needed.
- Allowed algorithms and JWKS from the exact trusted realm.
- Expiry, time and token-purpose/type checks.
- Proper scopes, roles and request-level permissions.

A public JWKS allows **verification**, not signing. Never implement custom production signature validation from scratch.

## Expected learning outcomes

1. Realm and client creation do not immediately yield an Alice access token.
2. The Device Authorization endpoint issues two *codes*, not access tokens.
3. Alice's approval lets the client redeem the `device_code` at the token endpoint.
4. Keycloak creates claims and signs the JWT.
5. The API validates the correct access token independently.
6. The **OIDC client** is `notes-tv`, the **user** is Alice, and Keycloak is the **issuer**.

## Cleanup

Stop the terminal/container (or `docker stop keycloak-school-lab` from another terminal). Because this example uses ephemeral `start-dev` storage and `--rm`, the lab data is disposable.

Official sources: [Keycloak Docker guide](https://www.keycloak.org/getting-started/getting-started-docker), [Keycloak endpoints](https://www.keycloak.org/securing-apps/oidc-layers), [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628).
