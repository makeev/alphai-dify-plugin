# AlphAI Financial News

Financial news for agents and workflows, from the [AlphAI](https://alphai.io) API. Every article is tagged with the tickers it is about, scored from 1 to 10 for relevance, and carries the sentiment toward each tagged ticker. Coverage of one event from several outlets is grouped into a single story.

Source code: https://github.com/makeev/alphai-dify-plugin

## Tools

| Tool | What it returns |
| --- | --- |
| Ticker news | Latest news about one ticker, with a minimum relevance filter |
| Search news | Full-text search, for topics and events such as "chip export controls" |
| Watchlist brief | One brief for up to 100 tickers: news by story, SEC filings, upcoming earnings dates |
| Insider trades | SEC Form 4 purchases and sales for one ticker or the whole market, with a filter for sales the insider chose to make |

Symbols: `NVDA` for US stocks, `BTC-USD` for crypto, a Yahoo suffix such as `SAP.DE` or `VOD.L` for other markets. News is English only.

## Setup

1. Create an API key at [alphai.io/account/api-keys](https://alphai.io/account/api-keys). The free plan allows 20 requests a minute and 100 a day.
2. In Dify, install the plugin, open **Tools → AlphAI Financial News → Authorize** and paste the key.
3. Add any of the four tools to an agent or a workflow.

Each tool call is one API request. A wrong key, an exhausted quota or an unknown ticker comes back as a plain message instead of results.

## Example

An agent with **Ticker news** and **Insider trades**, asked "What happened with NVDA this week, and are insiders selling?", calls Ticker news with `symbol=NVDA` and Insider trades with `symbol=NVDA, decision=discretionary`, then answers from the scored items and links to the publishers.

## Links

- API reference: https://alphai.io/developers
- Terms: https://alphai.io/terms
- Privacy: [PRIVACY.md](PRIVACY.md)
- Support: info@alphai.io

AlphAI output is AI-generated financial information for research, not investment advice.
