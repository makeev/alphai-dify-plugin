# Privacy policy

This plugin connects Dify to the AlphAI API (`https://api.alphai.io`).

## What is sent

- Your AlphAI API key, in the `Authorization` header of each request.
- The tool inputs you or your agent provide: ticker symbols, search keywords, the look-back window and the number of items.
- The plugin's user agent, `alphai-dify-plugin/<version>`.

Nothing else from your Dify workspace, conversations or files is sent.

## What the plugin stores

The plugin keeps no data of its own. Dify stores the API key in its encrypted credential storage.

## What AlphAI keeps

- Request logs: for each request made with an API key, AlphAI records the key and account, the endpoint and query parameters, the response status and timing, the client IP address and user agent. Every failed request and a sample of successful ones are kept, for support, debugging and abuse prevention, and deleted after about 90 days.
- Search log: the keywords sent with **Search news** are also kept with the account and key in a search log used to measure and improve search quality, for up to 400 days.

The AlphAI privacy policy applies: https://alphai.io/privacy

## Contact

info@alphai.io
