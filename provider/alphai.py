from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.client import AlphAIClient, AlphAIError


class AlphAIProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            AlphAIClient.from_credentials(credentials).ticker_news("AAPL", limit=1)
        except (AlphAIError, ValueError) as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
