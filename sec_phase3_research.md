# SEC Phase 3 Research Notes

Source 1: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- data.sec.gov provides unauthenticated REST APIs for company submissions and extracted XBRL data.
- Submissions endpoint: https://data.sec.gov/submissions/CIK##########.json
- Company facts endpoint: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
- APIs include filing forms such as 10-Q, 10-K, 8-K, 20-F, 40-F, 6-K and variants.
- Data updates throughout the day; CIK must be 10 digits with leading zeroes.
- data.sec.gov does not support CORS; automated access must comply with SEC privacy/security policy.

Source 2: https://www.sec.gov/about/developer-resources
- SEC provides JSON REST APIs and HTTPS access to EDGAR filing data.
- SEC recommends efficient access and downloading only required data.
- Fair-access guideline limits each user to no more than 10 requests per second.
- SEC may block unclassified bots or excessive automated requests.
- SEC also exposes RSS feeds and daily/index files as official alternatives.

Implementation implications:
- Use an identified User-Agent and rate limiter below 10 requests/second.
- Prefer submissions and companyfacts JSON for structured facts; fetch filing HTML only when required for 8-K/Form 4/material-event details.
- Never use web search as Phase 3 fallback; fallback must remain an official SEC source.
- Store source URL, form, filing date, accession number, CIK, period, and raw tag/label for AI handoff.
