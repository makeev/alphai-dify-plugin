from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools import base, shape


class WatchlistBriefTool(base.AlphAITool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        yield from self._run(
            lambda client: shape.brief(
                client.brief(
                    tool_parameters.get("tickers"),
                    hours=tool_parameters.get("hours", 24),
                    limit=tool_parameters.get("limit", 10),
                )
            )
        )
