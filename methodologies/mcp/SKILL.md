---
name: mcp-local
description: Bundled audit methodology for a server exposing tools over the Model Context Protocol (MCP) to external LLM clients, and/or acting as the OAuth 2.1 authorization/resource server for those clients.
license: MIT
---

# MCP server audit

For a server that plays the **MCP server role**: exposes tools/resources
over MCP (stdio or Streamable HTTP) to external LLM clients (Claude
Desktop, ChatGPT, custom agents), and often also acts as its own OAuth 2.1
authorization server (Dynamic Client Registration, `/authorize`, `/token`)
rather than only as an OAuth client. Distinct from `ai` (this repo/agent
as an LLM *consumer* calling out to tools) and from generic `api` (no
DCR/PKCE/resource-indicator concerns, no third-party LLM as caller).

Resolve the shared protocols first:

- `audit/reference/bootstrap-lite.md`

Load conditionally: `audit/reference/persistence-protocol.md` only for
`--persist`/writes beyond the report; `audit/reference/finding-contract.md`
+ `audit/reference/formal-delta.md` + `audit/reference/output-contract.md`
only when the run is formal.

## Scope

Always inspect:

- **Token scope/audience separation**: does the MCP access token carry a
  distinct `aud`/`scope`/`token_use` from any other token issued by the
  same signing key (session/app tokens, admin tokens)? A token meant for
  MCP tool calls must never validate on the app's normal REST/session
  routes, and vice versa. Same signing secret across audiences is fine
  only if every verifier checks `aud` and rejects on mismatch.
- **Read/write scope enforcement**: if the product intent is read-only,
  confirm no tool, resource, or prompt handler performs a write, and that
  the token/scope model has no path to mint a write-capable token from a
  read-only flow.
- **DCR (RFC 7591) abuse surface**: is client registration open to anyone
  (no auth), and if so, is that intentional (public clients, PKCE-only)?
  Confirm no `client_secret` is both issued to a public client *and*
  trusted as a real secret; confirm registered `redirect_uris` are
  actually enforced (exact match) at `/authorize` and `/token`, not just
  stored.
- **PKCE**: `S256` required and enforced (not merely accepted-if-present);
  `plain` rejected; the authorization code is single-use and invalidated
  on first exchange regardless of PKCE outcome (no replay window).
- **Authorization code and refresh token storage**: codes/refresh tokens
  stored hashed, not plaintext; codes short-lived and consumed atomically;
  refresh tokens rotated on use (old one invalidated) or, if not rotated,
  a documented reason why.
- **Revocation actually revokes**: does revoking a connection/grant
  (e.g. a "connected apps" UI) invalidate already-issued access tokens
  before their JWT expiry, or only stop future refreshes? If access
  tokens are stateless JWTs, either keep their TTL short and accept the
  window, or verify a DB-backed revocation check (connection/grant id
  claim checked per call) actually runs on the tool-call path, not just
  at token-mint time.
- **Transport auth wiring**: for Streamable HTTP/SSE mounted as a raw
  ASGI/WSGI sub-app (not through the main framework's route decorators),
  confirm the bearer-auth middleware is actually on the request path for
  every tool call, not only for the initial handshake. A session
  established once and reused for later `tools/call` messages must
  re-validate the token per call if the SDK/library supports long-lived
  sessions, or the session lifetime must be bounded to the token's TTL.
- **DNS-rebinding / Host-header protections**: MCP SDKs (e.g. the
  official Python SDK) often default to a loopback-only allowlist that
  silently rejects legitimate traffic behind a reverse proxy (`421`), or
  can be disabled outright. Confirm the effective setting matches the
  real deployment (loopback-only for local stdio-adjacent HTTP; explicit
  host validation or reliance on TLS+reverse-proxy+token auth for a real
  public host) and isn't a copy-pasted default nobody re-checked.
- **Rate limiting reaches this mount**: if the app has a framework-level
  rate limiter (decorator/middleware bound to normal routes), confirm it
  actually wraps the MCP mount too. A raw ASGI/WSGI sub-app frequently
  falls outside it silently. Check the limiter key: per-connection/token
  is required if the goal is per-user fairness; per-IP alone is
  insufficient once multiple users can share an egress IP, and pure
  per-IP with no fallback lets an unauthenticated caller with no/garbage
  token bypass limiting entirely.
- **Tool output data minimization**: every tool's actual return value
  (not just its docstring/description) contains only what the product
  intends to expose to a third-party LLM. Check for accidental inclusion
  of free-text fields (descriptions, notes, names) the product explicitly
  decided to exclude, and for aggregates with `n=1` that reveal a single
  underlying record.
- **Cross-tenant isolation**: every tool resolves its data scope (user/
  subject/tenant id) from the verified token's claims, never from a
  client-supplied parameter. Grep for tool parameters that look like an
  id/scope and confirm they aren't trusted as the authorization boundary.
- **Audit logging without payload leakage**: tool-call logs capture
  which tool, when, and which principal/connection, but never arguments
  or results (which may carry the same sensitive data the tool reads).
- **Confused-deputy via tool descriptions**: tool/resource descriptions
  and error messages returned to the calling LLM don't leak internal
  paths, other tenants' identifiers, or instructions that could be
  interpreted as prompt injection back into the calling agent's context.
- **Metadata endpoints** (`/.well-known/oauth-authorization-server`,
  `/.well-known/oauth-protected-resource`): issuer/resource URLs in the
  served metadata match the real deployment host, not a dev-time default
  silently left unset in production config.
- **Session-manager/process lifecycle bugs specific to MCP SDKs**: some
  Streamable HTTP session managers are single-use per instance/process
  cycle; a module-level singleton built once at import time breaks on the
  second ASGI lifespan cycle in the same process (test suites, or a
  worker reload without a full process restart). Confirm the server
  object is (re)built per lifecycle, not frozen at import.

## Workflow

1. Identify the MCP transport (stdio vs Streamable HTTP vs SSE) and
   whether this codebase is the MCP *server*, an OAuth *client* to some
   other MCP server, or both.
2. If this codebase issues its own OAuth tokens for MCP clients, read the
   authorize/token/register handlers end to end; do not assume framework
   defaults cover DCR/PKCE just because the app already does OAuth
   elsewhere for its own login flow — that is almost always a different
   role (client, not authorization server).
3. Trace one full tool call from the transport entry point to the data
   access layer, noting every point where the caller's identity/scope is
   established, re-checked, or silently dropped.
4. Diff the token/scope model used by MCP against the one used by the
   product's normal user-facing API; confirm they cannot be swapped.
5. Check whether the MCP mount inherits the app's standard middleware
   stack (auth, rate limit, CORS, logging) or bypasses it structurally.
6. Return a severity-ordered report with concrete file references.

## Recommended commands

```bash
rg -n "streamable_http|StreamableHTTP|stdio_server|sse_server|FastMCP|MCPServer|mcp\\.server" .
rg -n "register_client|dynamic.?client.?registration|/register\\b" .
rg -n "code_challenge|code_verifier|PKCE|S256" .
rg -n "authorization_code|refresh_token|/authorize\\b|/token\\b" .
rg -n "token_verifier|verify_token|TokenVerifier|AccessToken" .
rg -n "well-known/oauth-authorization-server|well-known/oauth-protected-resource" .
rg -n "rate.?limit|Limiter|slowapi|throttle" .
rg -n "@server\\.tool|@mcp\\.tool|add_tool|tools/call" .
```

Before step 3, identify the actual MCP SDK/library in use and its
specific auth-hook and session-lifecycle API (names vary by SDK/language
and by SDK major version); adapt the grep patterns above accordingly
instead of assuming one SDK's naming.

## Output

Standard mode: per `bootstrap-lite.md`'s 4-section format. Formal mode:
follow `audit/reference/output-contract.md`.

Generate: `tool x scope x auth x rate-limit x logging x tests`

## Standard

- Prefer fewer high-confidence findings over many speculative ones.
- Distinguish "the SDK's secure-by-default behavior was overridden" from
  "the SDK never had a safeguard here to begin with" — the remediation
  and severity differ.
- Call out any read/write boundary that depends only on which endpoint a
  client happens to call, rather than on an enforced scope check.
