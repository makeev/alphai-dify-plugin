from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools import base, shape


class TickerNewsTool(base.AlphAITool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        yield from self._run(
            lambda client: shape.feed(
                client.ticker_news(
                    tool_parameters.get("symbol"),
                    min_relevance=tool_parameters.get("min_relevance", 4),
                    limit=tool_parameters.get("limit", 10),
                    collapse=tool_parameters.get("collapse_stories", True) is not False,
                )
            )
        )
