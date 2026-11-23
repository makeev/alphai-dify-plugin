"""Small HTTPS client for the AlphAI REST API (https://alphai.io/developers)."""

from __future__ import annotations

import re
from typing import Any

import requests

BASE_URL = "https://api.alphai.io"
TIMEOUT_SECONDS = 20
USER_AGENT = "alphai-dify-plugin/0.0.1"
MAX_PAGE = 20  # 1-20 works on every plan; larger pages need a Pro key
_SYMBOL = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,19}$")

JsonPayload = dict[str, Any]


class AlphAIError(Exception):
    """A request that reached AlphAI or the network and failed."""


def normalize_symbol(value: Any) -> str:
    symbol = str(value or "").strip().upper().lstrip("$")
    if not _SYMBOL.match(symbol):
        raise ValueError(
            f"'{value}' is not a ticker. Use NVDA for US stocks, BTC-USD for crypto, "
            "or a Yahoo suffix such as SAP.DE for other markets."
        )
    return symbol


def normalize_symbols(value: Any, maximum: int = 100) -> list[str]:
    raw = value if isinstance(value, list) else re.split(r"[\s,;]+", str(value or ""))
    symbols: list[str] = []
    for item in raw:
        if str(item).strip():
            symbol = normalize_symbol(item)
            if symbol not in symbols:
                symbols.append(symbol)
    if not symbols:
        raise ValueError("Give at least one ticker, for example NVDA,AAPL.")
    if len(symbols) > maximum:
        raise ValueError(f"At most {maximum} tickers per request.")
    return symbols


def clamp(value: Any, low: int, high: int, default: int) -> int:
    """Dify may hand form values over as numbers or as strings ("3", "3.0")."""
    try:
        number = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default
    return max(low, min(high, number))


def as_bool(value: Any, default: bool) -> bool:
    """Dify may hand a boolean over as True or as the string "True" / "false"."""
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower() if value is not None else ""
    if text in ("true", "1", "yes", "on"):
        return True
    if text in ("false", "0", "no", "off"):
        return False
    return default


class AlphAIClient:
    def __init__(self, api_key: str, session: requests.Session | None = None) -> None:
        self._api_key = api_key
        self._session = session or requests.Session()

    @classmethod
    def from_credentials(cls, credentials: dict[str, Any]) -> AlphAIClient:
        api_key = str(credentials.get("api_key") or "").strip()
        if not api_key:
            raise ValueError("An AlphAI API key is required.")
        return cls(api_key)

    def _get(self, path: str, params: dict[str, Any]) -> JsonPayload:
        query = {key: value for key, value in params.items() if value is not None and value != ""}
        try:
            response = self._session.get(
                BASE_URL + path,
                params=query,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Accept": "application/json",
                    "User-Agent": USER_AGENT,
                },
                timeout=TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            raise AlphAIError(f"Could not reach AlphAI ({exc.__class__.__name__}).") from None
        if response.status_code >= 400:
            raise AlphAIError(f"AlphAI returned {response.status_code}: {_error_message(response)}")
        try:
            return response.json()
        except ValueError:
            raise AlphAIError("AlphAI returned a response that is not JSON.") from None

    def ticker_news(
        self, symbol: str, min_relevance: Any = 4, limit: Any = 10, collapse: Any = True
    ) -> JsonPayload:
        return self._get(
            "/api/news/",
            {
                "symbol": normalize_symbol(symbol),
                "min_relevance": clamp(min_relevance, 1, 10, 4),
                "page_size": clamp(limit, 1, MAX_PAGE, 10),
                "collapse": "story" if as_bool(collapse, True) else None,
            },
        )

    def search(
        self,
        query: str,
        symbol: str | None = None,
        min_relevance: int | None = None,
        limit: int = 10,
        collapse: bool = True,
    ) -> JsonPayload:
        text = str(query or "").strip()
        if not text:
            raise ValueError("Give a search query, for example 'chip export controls'.")
        return self._get(
            "/api/news/search/",
            {
                "q": text[:200],
                "symbol": normalize_symbol(symbol) if symbol else None,
                "min_relevance": clamp(min_relevance, 1, 10, 4) if min_relevance else None,
                "page_size": clamp(limit, 1, MAX_PAGE, 10),
                "collapse": "story" if as_bool(collapse, True) else None,
            },
        )

    def brief(self, tickers: Any, hours: int = 24, limit: int = 10) -> JsonPayload:
        return self._get(
            "/api/news/brief/",
            {
                "tickers": ",".join(normalize_symbols(tickers)),
                "hours": clamp(hours, 1, 168, 24),
                "limit": clamp(limit, 1, 20, 10),
            },
        )

    def insider(
        self, symbol: str | None = None, decision: str | None = None, limit: int = 10
    ) -> JsonPayload:
        if decision not in (None, "", "discretionary", "plan_like", "unknown"):
            raise ValueError("decision must be discretionary, plan_like or unknown.")
        return self._get(
            "/api/news/insider/",
            {
                "symbol": normalize_symbol(symbol) if symbol else None,
                "decision": decision or None,
                "page_size": clamp(limit, 1, MAX_PAGE, 10),
            },
        )


def _error_message(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.reason or "request failed"
    if isinstance(body, dict):
        for key in ("message", "detail", "error"):
            if isinstance(body.get(key), str) and body[key]:
                return body[key]
    return response.reason or "request failed"
