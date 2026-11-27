"""Sign in with HONO: OAuth 2.1 against ERA's public connector (mcp.hono.ai).

No setup for the user: the plugin registers itself (RFC 7591 public client,
PKCE S256) for the redirect URI Dify hands it. The HONO consent page asks for
the workspace and the HONO login, so one URL works for every tenant. The
provider object is stateless between the two OAuth steps, so the client_id and
PKCE verifier travel in `state`; the code is single-use, bound to Dify's exact
redirect URI and redeemed by Dify's server straight away.
"""
import base64
import hashlib
import json
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from tools._base import TIMEOUT_SECONDS, EraMcpError

AUTH_BASE = "https://mcp.hono.ai/era/oauth"
SCOPE = "hono:extended"


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _post(url: str, data: dict[str, Any], as_json: bool = False) -> dict[str, Any]:
    body = json.dumps(data).encode() if as_json else urllib.parse.urlencode(data).encode()
    ctype = "application/json" if as_json else "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": ctype, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode())
            msg = detail.get("error_description") or detail.get("error") or ""
        except ValueError:
            msg = ""
        raise EraMcpError(f"HONO sign-in failed: HTTP {e.code} {msg}".strip()) from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise EraMcpError(f"Could not reach HONO: {getattr(e, 'reason', e)}") from None


def authorization_url(redirect_uri: str) -> str:
    reg = _post(
        f"{AUTH_BASE}/register",
        {
            "client_name": "Dify (ERA by HONO plugin)",
            "redirect_uris": [redirect_uri],
            "token_endpoint_auth_method": "none",
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
        },
        as_json=True,
    )
    client_id = reg["client_id"]
    verifier = secrets.token_urlsafe(64)
    state = _b64url(json.dumps({"c": client_id, "v": verifier}).encode())
    query = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPE,
        "state": state,
        "code_challenge": _b64url(hashlib.sha256(verifier.encode()).digest()),
        "code_challenge_method": "S256",
    })
    return f"{AUTH_BASE}/authorize?{query}"


def _credentials(tok: dict[str, Any], client_id: str) -> tuple[dict[str, str], int]:
    access = str(tok.get("access_token") or "")
    if not access.startswith("hno_oat_"):
        raise EraMcpError("HONO sign-in returned no access token.")
    creds = {"access_token": access, "refresh_token": str(tok.get("refresh_token") or ""), "client_id": client_id}
    # Refresh a minute early so a tool call never lands on an expired token.
    return creds, int(time.time()) + int(tok.get("expires_in") or 3600) - 60


def exchange_code(redirect_uri: str, args: dict[str, str]) -> tuple[dict[str, str], int]:
    if args.get("error"):
        raise EraMcpError(f"HONO sign-in was not completed: {args.get('error_description') or args['error']}")
    try:
        state = json.loads(base64.urlsafe_b64decode(args.get("state", "") + "==="))
        client_id, verifier = state["c"], state["v"]
    except (ValueError, KeyError, TypeError):
        raise EraMcpError("HONO sign-in returned an invalid state. Please try again.") from None
    code = args.get("code") or ""
    if not code:
        raise EraMcpError("HONO sign-in returned no authorization code.")
    tok = _post(f"{AUTH_BASE}/token", {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": verifier,
    })
    return _credentials(tok, client_id)


def refresh(credentials: dict[str, Any]) -> tuple[dict[str, str], int]:
    client_id = str(credentials.get("client_id") or "")
    tok = _post(f"{AUTH_BASE}/token", {
        "grant_type": "refresh_token",
        "refresh_token": str(credentials.get("refresh_token") or ""),
        "client_id": client_id,
    })
    return _credentials(tok, client_id)
