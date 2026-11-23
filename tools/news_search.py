from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools import base, shape


class NewsSearchTool(base.AlphAITool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        yield from self._run(
            lambda client: shape.feed(
                client.search(
                    tool_parameters.get("query"),
                    symbol=tool_parameters.get("symbol") or None,
                    limit=tool_parameters.get("limit", 10),
                )
            )
        )
