from collections.abc import Mapping
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError
from werkzeug import Request

from tools import _oauth
from tools._base import EraMcpError, mcp_request


class HonoEraProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # API-key sign-in: tools/list checks URL, key and workspace without touching any HR data.
        try:
            mcp_request(credentials, "tools/list", {})
        except EraMcpError as e:
            raise ToolProviderCredentialValidationError(str(e)) from None

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        try:
            return _oauth.authorization_url(redirect_uri)
        except EraMcpError as e:
            raise ToolProviderOAuthError(str(e)) from None

    def _oauth_get_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> ToolOAuthCredentials:
        try:
            creds, expires_at = _oauth.exchange_code(redirect_uri, dict(request.args))
        except EraMcpError as e:
            raise ToolProviderOAuthError(str(e)) from None
        return ToolOAuthCredentials(credentials=creds, expires_at=expires_at)

    def _oauth_refresh_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> ToolOAuthCredentials:
        try:
            creds, expires_at = _oauth.refresh(dict(credentials))
        except EraMcpError as e:
            raise ToolProviderOAuthError(str(e)) from None
        return ToolOAuthCredentials(credentials=creds, expires_at=expires_at)
