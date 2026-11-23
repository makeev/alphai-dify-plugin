from tools import shape

ARTICLE = {
    "story_id": "abc123",
    "sources_count": 3,
    "original": {
        "title": "Dell expands its AI Factory with NVIDIA",
        "summary": "Dell added an agentic data gateway.",
        "url": "https://example.com/dell",
        "source_domain": "example.com",
        "time_published": "2026-11-23T06:36:51Z",
        "banner_image": "https://example.com/img.jpg",
    },
    "enrichment": {
        "relevance_score": 6,
        "category": "technology",
        "tickers": ["DELL", "NVDA"],
        "ai_trading_insights": {
            "ticker_analysis": [
                {"ticker": "DELL", "impact_analysis": {"sentiment": "positive"}},
            ]
        },
    },
    "search_match": {"context": "…the **AI Factory** with NVIDIA…"},
}

INSIDER = {
    "original": {"title": "Jane Doe sold $846K of AAPL", "url": "https://www.sec.gov/x"},
    "enrichment": {"tickers": ["AAPL"], "relevance_score": 5},
    "insider": {
        "side": "sell",
        "transaction_code": "S",
        "shares": "2398",
        "avg_price_usd": "352.77",
        "total_value_usd": "845942.46",
        "is_10b5_1": True,
        "insider_name": "Jane Doe",
        "insider_title": "SVP",
        "transaction_date": "2026-11-17",
        "filed_at": "2026-11-19T23:30:21Z",
        "decision": "plan_like",
    },
}


def test_article_is_compact():
    item = shape.article(ARTICLE)
    assert item["title"] == "Dell expands its AI Factory with NVIDIA"
    assert item["source"] == "example.com"
    assert item["tickers"] == [
        {"ticker": "DELL", "sentiment": "positive"},
        {"ticker": "NVDA", "sentiment": None},
    ]
    assert item["story_id"] == "abc123" and item["sources_count"] == 3
    assert item["match"] == "…the AI Factory with NVIDIA…"
    assert "banner_image" not in item


def test_feed_counts_and_insider_shape():
    out = shape.feed({"results": [INSIDER]}, kind="insider")
    assert out["count"] == 1
    trade = out["results"][0]
    assert trade["insider_name"] == "Jane Doe"
    assert trade["total_value_usd"] == "845942.46"
    assert trade["decision"] == "plan_like"
    assert trade["filing_url"] == "https://www.sec.gov/x"


def test_symbol_note_is_kept():
    out = shape.feed({"results": [], "symbol_note": "BTC resolves to BTC-USD"})
    assert out == {"count": 0, "results": [], "note": "BTC resolves to BTC-USD"}
