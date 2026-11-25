# AlphAI Financial News

Financial news for agents and workflows, from the [AlphAI](https://alphai.io/?utm_source=dify&utm_medium=partner) API. Every article is tagged with the tickers it is about, scored from 1 to 10 for relevance, and carries the sentiment toward each tagged ticker. Coverage of one event from several outlets is grouped into a single story.

Source code: https://github.com/makeev/alphai-dify-plugin

## Tools

| Tool | What it returns |
| --- | --- |
| Ticker news | Latest news about one ticker, with a minimum relevance filter |
| Search news | Full-text search, for topics and events such as "chip export controls" |
| Watchlist brief | One brief for up to 100 tickers: news by story, SEC filings, upcoming earnings dates |
| Insider trades | SEC Form 4 purchases and sales for one ticker or the whole market, with a filter for sales the insider chose to make |

Symbols: `NVDA` for US stocks, `BTC-USD` for crypto. A company with a US listing is tagged under its US ticker (`SAP`, not `SAP.DE`); other markets use a Yahoo suffix such as `0700.HK`. News is English only.

## Setup

1. Create an API key at [alphai.io/account/api-keys](https://alphai.io/account/api-keys?utm_source=dify&utm_medium=partner). The free plan allows 20 requests a minute and 100 a day.
2. In Dify, install the plugin, open **Tools → AlphAI Financial News → Authorize** and paste the key.
3. Add any of the four tools to an agent or a workflow.

Each tool call is one API request. A wrong key, an exhausted quota or an unknown ticker comes back as a plain message instead of results.

## Connection requirements

The plugin connects to one endpoint, `https://api.alphai.io`, over HTTPS and to nothing else. A self-hosted Dify behind a firewall needs outbound access to `api.alphai.io` on port 443. No inbound connection or callback URL is needed.

## Example

An agent with **Ticker news** and **Insider trades**, asked "What happened with NVDA this week, and are insiders selling?", calls Ticker news with `symbol=NVDA` and Insider trades with `symbol=NVDA, decision=discretionary`, then answers from the scored items and links to the publishers.

## Links

- API reference: https://alphai.io/developers?utm_source=dify&utm_medium=partner
- Terms: https://alphai.io/terms
- Privacy: [PRIVACY.md](PRIVACY.md)
- Support: info@alphai.io

AlphAI output is AI-generated financial information for research, not investment advice.
