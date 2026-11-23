from collections.abc import Callable, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.client import AlphAIClient, AlphAIError, JsonPayload


class AlphAITool(Tool):
    def _run(
        self, operation: Callable[[AlphAIClient], JsonPayload]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            payload = operation(AlphAIClient.from_credentials(self.runtime.credentials))
        except (AlphAIError, ValueError) as exc:
            yield self.create_text_message(str(exc))
            return
        yield self.create_json_message(payload)
