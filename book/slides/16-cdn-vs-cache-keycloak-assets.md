# Detailed teaching slides — CDN, HTTP caching and OAuth sessions

**Audience:** developers and students learning web security infrastructure.  
**Canonical technical chapter:** [CDN, caches and protected sessions](../../docs/16-cdn-vs-cache-keycloak-assets.md).  
**Format:** 12 detailed text-first slides with explanations and self-checks; no branded slide assets, videos, animation or social copy.

All URLs and actors are fictional.

---

## Slide 01 — A CDN is not a login server

**Learning objective:** Identify asset delivery, HTTP caching and identity services.

**On-slide text**

- CDN serves public scripts and assets
- Browser cache may reuse previous HTTP responses
- Keycloak handles authentication
- API protects user resources

**Teaching explanation:** A Content Delivery Network distributes static files from servers close to users. A browser HTTP cache can store and reuse those responses according to HTTP rules. Neither of these components is the Keycloak authorization server. When a browser loads keycloak-js from a CDN or local server, the JavaScript can still initiate a separate OAuth/OIDC conversation with Keycloak. The intended API validates the resulting access token and resource authorization.

**Diagram or worked example:** Five boxes: CDN, browser HTTP cache, JS adapter, Keycloak issuer and notes-api. Label content delivery vs OAuth.

**Self-check:** Can a CDN issue Alice's OIDC ID token merely by serving keycloak-js?  
**Answer:** No.

**Sources:** Chapter §§1–2; MDN CDN; Keycloak docs. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 02 — A CDN and a browser cache can both hold a copy

**Learning objective:** Explain how cache hits affect asset requests.

**On-slide text**

- Browser checks fresh local response first
- If needed, browser requests CDN/origin
- CDN edge may cache public asset
- Origin is source on cache miss

**Teaching explanation:** A browser may retain a fresh JavaScript file on disk or in memory. If that copy is unavailable or stale, it sends a network request to an origin or configured CDN. The CDN might itself have a fresh cached copy or fetch from a source server. Therefore, a file served by a CDN is not necessarily downloaded on every page load, and a file served locally can still be browser-cached. Tools may report memory, disk or HTTP revalidation status.

**Diagram or worked example:** Chapter §2 Mermaid flow with two independent cache-decision diamonds.

**Self-check:** Does switching to local static hosting disable the browser's HTTP cache?  
**Answer:** No.

**Sources:** Chapter §§2–3; MDN HTTP caching. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 03 — Five stores, five different security models

**Learning objective:** Distinguish cache objects from identity credentials.

**On-slide text**

- CDN: public asset copies
- Browser cache: reusable HTTP responses
- Cookie: browser-held session credential
- Session DB: protected token and session state
- JWKS cache: trusted issuer public keys

**Teaching explanation:** Several systems can store values but do not become equivalent. A browser cookie is not an HTTP cache entry; it is a credential automatically attached according to scope and browser policy. A backend session store associates an opaque cookie identifier with protected session/token state. A JWKS cache contains public signing keys from a configured issuer. The CDN and HTTP cache should only reuse responses that are eligible under caching and privacy policy.

**Diagram or worked example:** A five-column purpose-and-trust table, not a single box labeled cache.

**Self-check:** Is an application session cookie a public JavaScript cache?  
**Answer:** No.

**Sources:** Chapter §§1 and 8; RFC 10017. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 04 — Cache-Control public and immutable

**Learning objective:** Understand safe long-lived caching for content-addressed static assets.

**On-slide text**

- public allows shared caches
- max-age sets freshness lifetime
- immutable avoids unnecessary revalidation while fresh
- Only use long lifetime with changed filename on update

**Teaching explanation:** A public JavaScript bundle with a fingerprint in the filename can be cached for a long period because a changed bundle will normally have a new URL. Cache-Control: public, max-age=31536000, immutable is a familiar choice for this case. Do not apply the same policy blindly to changing HTML pages or private user responses. Otherwise clients or shared caches may continue serving stale or private content for too long.

**Diagram or worked example:** Public app.a1b2c3.js with long-lived header; contrast mutable app.js URL.

**Self-check:** Should a frequently overwritten app.js use year-long immutable caching?  
**Answer:** No.

**Sources:** Chapter §4; MDN Cache-Control. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 05 — No-cache, private, and no-store are different

**Learning objective:** State precise HTTP semantics.

**On-slide text**

- no-cache allows storage but requires revalidation
- private prohibits shared cache storage
- no-store instructs caches not to store
- Neither private nor no-cache equals no-store

**Teaching explanation:** The names are easy to misinterpret. no-cache means stored content must be validated before reuse; it does not prohibit storage. private blocks storage in shared caches but not necessarily in a browser's private cache. no-store tells caches not to store the response. These policies can be combined when justified. Treat each value as an HTTP directive, not as a promise of encryption or an API permission decision.

**Diagram or worked example:** Three labeled cache-control cards with storage allowed, shared cache allowed and revalidation rules.

**Self-check:** Does no-cache mean the response can never be stored?  
**Answer:** No.

**Sources:** Chapter §4; MDN HTTP caching. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 06 — Separate public static from private notebook data

**Learning objective:** Select caching behavior based on response sensitivity.

**On-slide text**

- Static fingerprinted JS → eligible public cache
- Private notes → no-store under this design
- OAuth token response → no-store
- Never share a session or Bearer token in a CDN cache

**Teaching explanation:** A fictional GET for app.a1b2c3.js can receive a long-lived public caching header. By contrast, a GET for Alice's private notebooks through a BFF should return only authorized content and use a policy preventing storage in shared caches; a no-store policy is appropriate in the highly sensitive teaching example. OAuth token responses should not be shared-cached. The browser's session cookie is sent to the BFF, not published in a CDN response body.

**Diagram or worked example:** Two HTTP examples side by side from Chapter §5, with the private response marked no-store.

**Self-check:** Can Alice's personalized notes be served from a shared public edge cache under this design?  
**Answer:** No.

**Sources:** Chapter §5; MDN Cache-Control; RFC 10017. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 07 — Follow the two request paths end to end

**Learning objective:** Explain where the browser and BFF send each request.

**On-slide text**

- Path A: browser → CDN → public asset origin
- Path B: browser cookie → BFF session store
- BFF → notes-api with access token
- API checks token and notebook permission

**Teaching explanation:** The public asset request can be satisfied by local/browser cache, CDN edge or origin based on freshness. After authentication, a different request for notebooks goes from the browser to the BFF with an application cookie. The BFF resolves a protected server-side session, obtains the appropriate access token and calls notes-api. The API validates the access token and authorizes the requested notebook. The CDN does not mediate OAuth credential trust.

**Diagram or worked example:** Chapter §6 full sequence diagram, visually split into public asset and private notebook phases.

**Self-check:** Is the BFF session store the source of JavaScript files?  
**Answer:** Not normally; it stores authenticated session state.

**Sources:** Chapter §6; RFC 10017. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 08 — Trusted JWKS caches are another category

**Learning objective:** Understand public key caching for JWT validation.

**On-slide text**

- API pins trusted issuer
- Fetch approved public JWKS
- Cache for performance and key rotation
- kid is untrusted lookup hint, not URL authority

**Teaching explanation:** A JWT-verifying resource server may cache public keys announced by a trusted Keycloak issuer so it does not fetch them for every request. These keys are public verification material, not user Bearer tokens. The server must bind the JWKS source to a configured trusted issuer and apply allowed algorithm policy. Unknown kid can prompt a bounded refresh of the approved source, but must never lead to fetching arbitrary jku URLs from attacker-controlled token headers.

**Diagram or worked example:** Chapter §7 trust cache diagram; show issuer trust separate from static-asset freshness.

**Self-check:** Could a JWT supplied jku redirect the API to any new key server?  
**Answer:** No.

**Sources:** Chapter §7; RFC 8725. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 09 — Browser cookie is a sensitive credential

**Learning objective:** Explain why BFF cookie is not a cache hit.

**On-slide text**

- Opaque cookie selects server session
- Secure, HttpOnly and SameSite matter
- Backend store holds protected OAuth tokens
- Session expiry is not HTTP cache expiry

**Teaching explanation:** An application session cookie identifies a browser session to a BFF. Its security depends on appropriate cookie attributes, unguessable values, transport and server-side validation. The backend session store may hold or reference OAuth access/refresh tokens, but a browser HTTP cache does not. Session records need TTLs, rotation, logout and authorization controls rather than only cache freshness headers. Signed client-side cookies are readable and must not contain a refresh token in the strict server-storage design.

**Diagram or worked example:** Cookie → protected session store → token state, separate from browser HTTP-cache box.

**Self-check:** Is a signed Starlette session cookie an encrypted server token vault?  
**Answer:** No.

**Sources:** Chapter §8; Starlette middleware; RFC 10017. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 10 — CDN choice does not fix insecure origins

**Learning objective:** Separate asset source from browser Web Crypto restrictions.

**On-slide text**

- Local script source removes external CDN fetch
- Page origin still determines secure context
- Remote HTTP VM origin normally not trusted
- BFF PKCE in Python still needs HTTPS

**Teaching explanation:** A browser may load the exact same JavaScript bytes from a CDN or an app's local static route. Its secure-context classification depends on the web page's origin and browser policy, not the script's download host alone. crypto.subtle may work for a localhost test and fail on a remote HTTP address. Bundling keycloak-js locally removes one external runtime dependency, but not the need for TLS. A backend Authlib BFF can avoid browser-side PKCE hashing without converting insecure HTTP transport into secure communication.

**Diagram or worked example:** Two independent axes: script source and page origin; show no causal line from local bundle to secure context.

**Self-check:** Will bundling keycloak-js make an ordinary HTTP VM-IP page secure?  
**Answer:** No.

**Sources:** Chapter §9; MDN Secure Contexts. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 11 — External CDN versus local build: risks

**Learning objective:** Compare availability and supply chain without oversimplifying.

**On-slide text**

- Remote CDN adds runtime external dependency
- Local bundle still needs dependency review
- Both can be browser cached
- Neither changes OAuth protocol actors

**Teaching explanation:** An external CDN can serve public assets efficiently but creates dependency on a third-party origin and its availability/integrity. A local build removes that runtime CDN request but still relies on a supply chain during packaging. Both should use supported libraries, pinned versions and appropriate CSP/integrity controls. CDN choice does not decide whether keycloak-js or FastAPI is the OAuth client; that is an application-architecture decision.

**Diagram or worked example:** Risk comparison from Chapter §10 with availability, supply chain, caching, credential exposure.

**Self-check:** Does a local JS bundle automatically eliminate every supply-chain risk?  
**Answer:** No.

**Sources:** Chapter §10; MDN CDN. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

## Slide 12 — DevTools experiment without leaking credentials

**Learning objective:** Interpret Network status and caching headers safely.

**On-slide text**

- Inspect Request URL and Cache-Control
- Look for memory/disk or 304 status
- Compare reload behavior
- Hide Cookie, Authorization and Set-Cookie
- Distinguish session and API from asset

**Teaching explanation:** In a disposable learning app, reload a page and inspect the browser's Network panel. Public JavaScript files may be served from a CDN or local static route, returned as 200, revalidated as 304, or reused from browser cache. For private API requests, inspect only the presence and semantics of headers, never their secret values. Explain the difference between an HTTP cache policy and an application's session lifetime. This is a test plan, not a report of actual browser observations.

**Diagram or worked example:** Chapter §11 safe exercise checklist plus final conceptual question.

**Self-check:** If a response says no-cache, may it still be stored and revalidated?  
**Answer:** Yes.

**Sources:** Chapter §§11–12; MDN Caching. [Chapter](../../docs/16-cdn-vs-cache-keycloak-assets.md) · [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) · [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017).

