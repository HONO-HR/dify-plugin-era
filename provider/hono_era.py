from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools._base import EraMcpError, mcp_request


class HonoEraProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # tools/list checks URL, key and workspace without touching any HR data.
        try:
            mcp_request(credentials, "tools/list", {})
        except EraMcpError as e:
            raise ToolProviderCredentialValidationError(str(e)) from None
