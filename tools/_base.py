"""Shared MCP client for the ERA by HONO Dify plugin.

Every tool is a thin call to the user's own ERA MCP endpoint (JSON-RPC
`tools/call`, stateless Streamable HTTP). The API key is only ever sent to a
HONO host, over HTTPS, and is never logged or echoed back.
"""
import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Generator
from typing import Any

ALLOWED_HOST_SUFFIXES = ("hono.ai", "honohr.com")
TIMEOUT_SECONDS = 55  # the server caps every tool at 45s


class EraMcpError(Exception):
    pass


def check_credentials(credentials: dict[str, Any]) -> tuple[str, str]:
    url = str(credentials.get("mcp_url") or "").strip()
    key = str(credentials.get("api_key") or "").strip()
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not any(host == s or host.endswith("." + s) for s in ALLOWED_HOST_SUFFIXES):
        raise EraMcpError("ERA MCP URL must be an https:// address on a HONO domain (hono.ai or honohr.com).")
    if not parsed.path.rstrip("/").endswith("/mcp") or parsed.query or parsed.fragment:
        raise EraMcpError("ERA MCP URL must end in /mcp. Copy it from ERA > Profile > MCP keys.")
    if not key.startswith("hno_live_"):
        raise EraMcpError("API key must be an ERA MCP key (starts with hno_live_).")
    return url, key


def mcp_request(credentials: dict[str, Any], method: str, params: dict[str, Any]) -> dict[str, Any]:
    url, key = check_credentials(credentials)
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        hint = {
            401: "the API key was rejected (revoked, expired or for another workspace)",
            403: "MCP access is not enabled for this ERA workspace, or this IP is not allowed",
            429: "ERA rate limit reached, try again in a minute",
        }.get(e.code, "the ERA server returned an error")
        raise EraMcpError(f"ERA request failed: HTTP {e.code}, {hint}.") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise EraMcpError(f"Could not reach ERA: {getattr(e, 'reason', e)}") from None
    if "error" in payload:
        raise EraMcpError(f"ERA error: {payload['error'].get('message', 'unknown error')}")
    return payload.get("result") or {}


class EraMcpMixin:
    """Mixed into each generated Tool class, which sets MCP_TOOL_NAME (and JSON_PARAMS
    for array/object params, which Dify passes as JSON text)."""

    MCP_TOOL_NAME = ""
    JSON_PARAMS: tuple[str, ...] = ()

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        args = {k: v for k, v in tool_parameters.items() if v is not None and v != ""}
        for name in self.JSON_PARAMS:
            if isinstance(args.get(name), str):
                try:
                    args[name] = json.loads(args[name])
                except ValueError:
                    yield self.create_text_message(f"Parameter {name} must be JSON text.")
                    return
        try:
            result = mcp_request(self.runtime.credentials, "tools/call", {"name": self.MCP_TOOL_NAME, "arguments": args})
        except EraMcpError as e:
            yield self.create_text_message(str(e))
            return
        text = "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
        if result.get("isError"):
            yield self.create_text_message(text or "The ERA tool returned an error.")
            return
        try:
            data = json.loads(text)
        except ValueError:
            data = None
        if isinstance(data, dict):
            yield self.create_json_message(data)
        yield self.create_text_message(text)
