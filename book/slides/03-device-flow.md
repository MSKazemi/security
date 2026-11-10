# Teaching slides — OAuth Device Authorization Grant

**Audience:** beginners and developers building constrained-input clients.  
**Canonical source:** [Device Flow tutorial](../../docs/03-device-flow.md).  
**Format:** 12 detailed teaching outlines. No animations, branding, timed scenes, platform copy or rendered presentation.

Examples use only fictional learning devices and synthetic credentials.

---

## Slide 01 — Why Device Flow exists

**Learning objective:** Explain constrained-input authorization without sharing a password.

**On-slide text**

- TV/CLI cannot easily show browser login
- User uses a separate trusted device
- Client never collects Alice's password
- Device polls for authorization result

**Teaching explanation:** Device Authorization helps applications with limited input capabilities or no suitable browser-based redirect. The constrained client obtains a device and user code; Alice signs in through a second trusted browser and approves the request. The device polls Keycloak for a result. The password stays on the identity-provider page, but this does not make the cross-device request intrinsically safe: a user may be tricked into approving someone else's request.

**Diagram or worked example:** Smart TV, Alice's phone and Keycloak diagram; highlight separate devices and trust context.

**Self-check:** Does the smart TV need to know Alice's password?  
**Answer:** No.

**Sources:** Chapter §1; RFC 8628. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 02 — Device Flow is request-response, not push

**Learning objective:** Follow an accurate OAuth protocol sequence.

**On-slide text**

- Client requests device authorization
- Server returns two codes and metadata
- User approves in separate browser
- Client polls token endpoint for response

**Teaching explanation:** The Device Flow client starts a request at the device authorization endpoint and obtains the codes and verification URI. Alice completes authentication and authorization through a separate browser. The client later polls at the server's prescribed interval; an access token may be returned only in a successful polling response after approval. Keycloak does not unsolicitedly push an access token to the device. Other terminal outcomes include denial, expiry or other errors.

**Diagram or worked example:** Use Chapter §2 sequence diagram, with loop label and terminal outcomes.

**Self-check:** Does Keycloak automatically push a token to the TV the instant Alice approves?  
**Answer:** No, it responds to a later valid poll.

**Sources:** Chapter §2; RFC 8628 §3. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 03 — What does device authorization return?

**Learning objective:** Recognize the six important response fields.

**On-slide text**

- device_code: private polling credential
- user_code: human-entry code
- verification_uri: issuer page
- expires_in: deadline; interval: pacing

**Teaching explanation:** A device authorization response typically includes a sensitive device_code, a human-readable user_code and a trusted verification_uri. The device client also receives expires_in and possibly interval for pacing. An optional verification_uri_complete may help with a prefilled or QR-style user interaction. These values have different roles: the user code is not a token, and the device code is not an API access credential. Default interval is five seconds if omitted.

**Diagram or worked example:** An annotated synthetic JSON response, not any live device or token values.

**Self-check:** If a device response has user_code, is that value a Bearer access token?  
**Answer:** No.

**Sources:** Chapter §3; RFC 8628 §3.2. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 04 — User code and device code: who holds which?

**Learning objective:** Avoid substituting one code for the other.

**On-slide text**

- User enters user_code on verification page
- Device keeps device_code private
- Device polls token endpoint with device_code
- Neither is an API access token

**Teaching explanation:** The user_code is a short, human-friendly value displayed by the constrained client and typed into the authorization device's trusted verification page. The device_code is the underlying sensitive credential that binds the polling client to the pending authorization request. The user should never be asked to hand an unexpected code to a stranger or unauthorized service. The device should not display or log device_code.

**Diagram or worked example:** Two-column table with code, holder, endpoint and what not to do.

**Self-check:** Which code is sent in the device's token-polling request?  
**Answer:** device_code, not user_code.

**Sources:** Chapter §3; RFC 8628. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 05 — Alice's approval is a separate event

**Learning objective:** Make the cross-device trust boundary visible.

**On-slide text**

- Alice opens the trusted issuer page
- Checks she started this request
- Reviews requesting client and intended access
- Approves or declines

**Teaching explanation:** The legitimate user authorizes on a device different from the one that requested the grant. The verification URL and user code may be displayed as text or QR. Their mere presence does not authenticate the request's source. Alice should confirm that she initiated the request, that the displayed client matches her device and that the requested permissions make sense. System designers must add appropriate safeguards beyond expecting users to detect every social-engineering attempt.

**Diagram or worked example:** Device-to-phone code transfer marked as an unauthenticated context channel.

**Self-check:** Does scanning an official-looking QR automatically prove the request is safe?  
**Answer:** No.

**Sources:** Chapter §5; RFC 10027. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 06 — First endpoint: device authorization

**Learning objective:** Find the initial request and avoid confusing endpoints.

**On-slide text**

- Discover device_authorization_endpoint
- Client sends client_id and requested scope
- Server returns device grant metadata
- No access token issued yet

**Teaching explanation:** Device Flow starts at the authorization server's device authorization endpoint, typically discovered through OIDC/OAuth metadata. The client sends an application/x-www-form-urlencoded request with its client identifier and scope and authenticates if required by its client type. The server responds with codes, verification URLs, expiration and polling information. The exact Keycloak paths should be discovered rather than hardcoded for a deployment.

**Diagram or worked example:** HTTP POST to /auth/device and JSON fields; mark token endpoint as a different endpoint.

**Self-check:** Does the device authorization endpoint return a usable access token immediately?  
**Answer:** No.

**Sources:** Chapter §4; Keycloak OIDC docs; RFC 8628. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 07 — Second endpoint: poll with device_code

**Learning objective:** Trace the exact OAuth device-code grant.

**On-slide text**

- POST token endpoint
- grant_type = urn:ietf:params:oauth:grant-type:device_code
- Send sensitive device_code and client ID
- Stop after terminal outcome

**Teaching explanation:** The client later sends device_code to the token endpoint along with the correct grant_type URI and registered client information. While Alice has not approved, the response is an OAuth error such as authorization_pending. After approval and all server checks, a later poll can return the access token; if denied or expired, the client stops. The human user_code never replaces the secret device_code in this request.

**Diagram or worked example:** HTTP request fields with a synthetic device code and URL-safe form encoding.

**Self-check:** Which endpoint handles a device_code grant token exchange?  
**Answer:** The token endpoint.

**Sources:** Chapter §6; RFC 8628 §3.4. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 08 — Polling: pending and slow_down arithmetic

**Learning objective:** Calculate compliant polling intervals.

**On-slide text**

- Initial interval = 5 seconds when specified or omitted default
- authorization_pending: wait at least current interval
- slow_down: add at least 5 seconds
- Repeated slow_down: keep increasing

**Teaching explanation:** Suppose the initial interval is 5 seconds. After authorization_pending, the client waits at least five seconds before the next poll. When slow_down arrives, the device increases the minimum interval by five seconds for that and all later polls: 5 becomes 10. If the server sends slow_down a second time, it becomes at least 15. These are minimum waits, not fixed required timing; the client may back off further.

**Diagram or worked example:** 5 → 10 → 15 seconds horizontal timeline with server error labels.

**Self-check:** What is minimum new interval after slow_down when current interval is 5?  
**Answer:** 10 seconds.

**Sources:** Chapter §7; RFC 8628 §3.5. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 09 — Terminal errors: know when to stop

**Learning objective:** Distinguish pending from denial, expiry and network failure.

**On-slide text**

- access_denied → stop
- expired_token → stop
- Successful token response → stop
- Timeout → backoff; don't busy-loop

**Teaching explanation:** authorization_pending and slow_down are transient responses that permit continued polling while the authorization remains valid. access_denied and expired_token are terminal outcomes; the client must stop. A successful token response also ends polling. Network timeouts require reducing polling frequency and respecting expiration rather than retrying at unlimited speed. Any unexpected protocol error should be handled safely rather than interpreted as approval.

**Diagram or worked example:** Chapter §7 decision diagram with separate waiting, backoff, accepted and refused branches.

**Self-check:** Should a client continue polling after expired_token?  
**Answer:** No.

**Sources:** Chapter §7; RFC 8628 §3.5. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 10 — Cross-device consent phishing is real

**Learning objective:** Learn the August 2026 security guidance.

**On-slide text**

- Device code/QR context may be unauthenticated
- An attacker can initiate a request for someone else to approve
- Risk assessment is mandatory
- Use mitigations or another flow

**Teaching explanation:** Cross-device flow security BCP RFC 10027 describes how attackers can obtain their own authorization request and manipulate the context in which a victim sees a user code or QR. A trustworthy-looking web page or code alone does not establish which device asked for authorization. Implementers must assess the risk and apply appropriate mitigations such as proximity, registered devices, time-limited one-time codes and robust consent UX; avoid Device Flow when residual risk is excessive.

**Diagram or worked example:** Two-device diagram with unauthenticated user-code transfer; note the difference between client/issuer and physical source.

**Self-check:** Is Device Flow always a safe default for high-value resources?  
**Answer:** No, a risk assessment and stronger alternatives may be needed.

**Sources:** Chapter §9; RFC 10027. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 11 — From codes to an API access token

**Learning objective:** Explain the separation between device artifacts and resource authorization.

**On-slide text**

- device_code and user_code belong to pending grant
- After approval, token endpoint may issue access token
- Client presents access token to intended API
- API validates audience and notebook permission

**Teaching explanation:** The client never uses its device authorization response codes as resource credentials. If Alice approves and polling succeeds, the client receives an access token subject to issuer, audience and scope restrictions. It presents that token to notes-api under an appropriate scheme. notes-api still checks the token purpose, signature or introspection, expiry and the specific notebook permission. Device Flow does not turn a user approval into blanket permission for every resource.

**Diagram or worked example:** Chapter §8 flowchart ending with an independent API validation and resource-policy gate.

**Self-check:** Can user_code authorize a notes-api request?  
**Answer:** No.

**Sources:** Chapter §8; RFC 8628; RFC 9700. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

## Slide 12 — Review: device, codes, polling and trust

**Learning objective:** Summarize the flow and a safe design decision.

**On-slide text**

- Use Device Flow for genuinely constrained clients
- User authenticates on trusted separate device
- Poll with device_code and correct pacing
- Account for phishing and API authorization

**Teaching explanation:** Ask the learner to narrate the entire flow: TV starts device authorization, receives two different codes, shows a trusted verification URL and user code, Alice signs in separately and approves only the request she initiated, and the client polls until success or a terminal error. Apply five-second increments for slow_down and stop on denial or expiry. Then explain why an access token for the wrong API or wrong notebook must still be rejected.

**Diagram or worked example:** Five-step summary with one extra red security gate for phishing and one API-permission gate.

**Self-check:** What are the next minimum intervals after two slow_down errors starting from 5?  
**Answer:** 10 seconds, then 15 seconds.

**Sources:** Chapter §§1–12; RFC 8628; RFC 10027. [Canonical chapter](../../docs/03-device-flow.md) · [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) · [RFC 10027](https://www.rfc-editor.org/rfc/rfc10027).

