"""Turn AlphAI responses into compact items that fit an LLM context."""

from __future__ import annotations

from typing import Any

JsonPayload = dict[str, Any]


def _ticker_sentiment(item: JsonPayload) -> list[JsonPayload]:
    enrichment = item.get("enrichment") or {}
    insights = enrichment.get("ai_trading_insights") or {}
    seen: dict[str, str | None] = {}
    for row in insights.get("ticker_analysis") or []:
        ticker = row.get("ticker")
        if ticker:
            seen[ticker] = (row.get("impact_analysis") or {}).get("sentiment")
    for ticker in enrichment.get("tickers") or []:
        seen.setdefault(ticker, None)
    return [{"ticker": ticker, "sentiment": sentiment} for ticker, sentiment in seen.items()]


def article(item: JsonPayload) -> JsonPayload:
    original = item.get("original") or {}
    enrichment = item.get("enrichment") or {}
    out: JsonPayload = {
        "title": original.get("title"),
        "summary": original.get("summary"),
        "url": original.get("url"),
        "source": original.get("source_domain"),
        "published_at": original.get("time_published"),
        "relevance_score": enrichment.get("relevance_score"),
        "category": enrichment.get("category"),
        "tickers": _ticker_sentiment(item),
    }
    if item.get("story_id"):
        out["story_id"] = item["story_id"]
        out["sources_count"] = item.get("sources_count")
    match = (item.get("search_match") or {}).get("context")
    if match:
        out["match"] = match.replace("**", "")
    return out


def insider_trade(item: JsonPayload) -> JsonPayload:
    original = item.get("original") or {}
    enrichment = item.get("enrichment") or {}
    insider = item.get("insider") or {}
    return {
        "title": original.get("title"),
        "tickers": enrichment.get("tickers") or [],
        "insider_name": insider.get("insider_name"),
        "insider_title": insider.get("insider_title"),
        "side": insider.get("side"),
        "transaction_code": insider.get("transaction_code"),
        "shares": insider.get("shares"),
        "avg_price_usd": insider.get("avg_price_usd"),
        "total_value_usd": insider.get("total_value_usd"),
        "is_10b5_1": insider.get("is_10b5_1"),
        "decision": insider.get("decision"),
        "transaction_date": insider.get("transaction_date"),
        "filed_at": insider.get("filed_at"),
        "filing_url": original.get("url"),
        "relevance_score": enrichment.get("relevance_score"),
    }


def feed(payload: JsonPayload, kind: str = "article") -> JsonPayload:
    make = insider_trade if kind == "insider" else article
    results = [make(item) for item in payload.get("results") or []]
    out: JsonPayload = {"count": len(results), "results": results}
    if payload.get("symbol_note"):
        out["note"] = payload["symbol_note"]
    return out


def brief(payload: JsonPayload) -> JsonPayload:
    """The brief is already compact: one entry per story, filings and earnings dates apart."""
    return payload
