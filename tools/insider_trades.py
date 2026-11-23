from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools import base, shape


class InsiderTradesTool(base.AlphAITool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        yield from self._run(
            lambda client: shape.feed(
                client.insider(
                    symbol=tool_parameters.get("symbol") or None,
                    decision=tool_parameters.get("decision") or None,
                    limit=tool_parameters.get("limit", 10),
                ),
                kind="insider",
            )
        )
