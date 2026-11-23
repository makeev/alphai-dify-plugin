from unittest import mock

import pytest
import requests

from tools.client import AlphAIClient, AlphAIError, normalize_symbol, normalize_symbols


def _client(status=200, body=None):
    response = mock.Mock(status_code=status, reason="Too Many Requests")
    response.json.return_value = body if body is not None else {"results": []}
    session = mock.Mock()
    session.get.return_value = response
    return AlphAIClient("ak_live_test", session=session), session


def test_symbols_are_normalized():
    assert normalize_symbol(" $nvda ") == "NVDA"
    assert normalize_symbol("btc-usd") == "BTC-USD"
    assert normalize_symbols("nvda, AAPL;nvda  sap.de") == ["NVDA", "AAPL", "SAP.DE"]
    with pytest.raises(ValueError):
        normalize_symbol("not a ticker")
    with pytest.raises(ValueError):
        normalize_symbols(",".join(f"T{i}" for i in range(101)))


def test_ticker_news_sends_key_and_clamps():
    client, session = _client()
    client.ticker_news("nvda", min_relevance=99, limit=500)
    args, kwargs = session.get.call_args
    assert args[0] == "https://api.alphai.io/api/news/"
    assert kwargs["headers"]["Authorization"] == "Bearer ak_live_test"
    assert kwargs["params"] == {
        "symbol": "NVDA",
        "min_relevance": 10,
        "page_size": 20,
        "collapse": "story",
    }


def test_optional_params_are_dropped():
    client, session = _client()
    client.insider()
    assert session.get.call_args.kwargs["params"] == {"page_size": 10}
    client.ticker_news("AAPL", collapse=False)
    assert "collapse" not in session.get.call_args.kwargs["params"]


def test_brief_joins_tickers():
    client, session = _client()
    client.brief("NVDA AAPL", hours=500, limit=0)
    assert session.get.call_args.kwargs["params"] == {
        "tickers": "NVDA,AAPL",
        "hours": 168,
        "limit": 1,
    }


def test_api_error_uses_message():
    client, _ = _client(status=429, body={"message": "Daily quota reached."})
    with pytest.raises(AlphAIError, match="429: Daily quota reached."):
        client.ticker_news("AAPL")


def test_network_error_does_not_leak_details():
    client, session = _client()
    session.get.side_effect = requests.ConnectionError("Bearer ak_live_test")
    with pytest.raises(AlphAIError) as caught:
        client.ticker_news("AAPL")
    assert "ak_live_test" not in str(caught.value)


def test_missing_key_is_a_value_error():
    with pytest.raises(ValueError):
        AlphAIClient.from_credentials({"api_key": "  "})


def test_bad_decision_is_refused():
    client, _ = _client()
    with pytest.raises(ValueError):
        client.insider(decision="everything")


def test_dify_string_values_are_understood():
    client, session = _client()
    client.ticker_news("NVDA", min_relevance="6", limit="3.0", collapse="False")
    assert session.get.call_args.kwargs["params"] == {
        "symbol": "NVDA",
        "min_relevance": 6,
        "page_size": 3,
    }
    client.ticker_news("NVDA", collapse="True")
    assert session.get.call_args.kwargs["params"]["collapse"] == "story"
