# Page Pulse Loom Walkthrough Script

## 0:00–0:30 — Introduction

Hi, I’m [your name], and this is Page Pulse, a full-stack webpage auditing application built with FastAPI and React. The application takes a webpage URL, fetches it asynchronously, and returns a focused set of content, accessibility, and response-time metrics. I’ll show the user interface first, then the backend parsing flow and the automated tests.

## 0:30–1:30 — Frontend demonstration

This is the Page Pulse interface. It is intentionally minimal: there is one URL input, an Analyze button, clear loading feedback, and a results card. The button is disabled while a request is running, so users cannot accidentally submit the same audit multiple times. The form also submits when I press Enter in the URL field.

I’ll enter `https://example.com` and select Analyze. This is a real, public webpage, so it is a good simple demonstration. Once the request finishes, the results card displays the final URL and the metrics returned by the API. If the URL is invalid, unreachable, too slow, or not an HTML page, the same area shows a clear error message instead.

## 1:30–2:30 — Explain the audit results

Let’s walk through the results. HTTP Status is the status returned by the website, and Response Time shows how long the fetch took in milliseconds. Page Title and Meta Description are useful SEO signals taken from the document head. H1 Count shows how many primary heading elements the page contains.

Images Missing Alt counts image elements without meaningful alternative text, which is a basic accessibility signal. Finally, Word Count measures the visible text content after non-visible script, style, and noscript elements are removed. Together these are a quick, practical first-pass audit rather than a full SEO crawler.

## 2:30–3:45 — Backend parsing logic

Now I’ll open `backend/app/services/audit_service.py`. The main `audit_webpage` function is kept in the service layer so the route itself remains thin. It creates an `httpx.AsyncClient` with redirect following enabled and a ten-second timeout, then measures the request with `time.perf_counter`.

After the response arrives, `_is_html_response` checks the Content-Type header. This prevents the parser from trying to analyse files such as PDFs or images. For HTML responses, `_build_audit_response` creates a BeautifulSoup document. It reads the title and description meta tag, then removes script, style, and noscript tags before counting visible words. It also counts H1 tags and image tags whose alt attribute is absent or empty.

The route in `backend/app/routers/audit.py` only validates the request model and delegates to this service. Error handling maps bad URLs to 400, timeouts to 408, non-HTML content to 415, and unexpected analysis issues to 500, giving frontend clients clear feedback.

## 3:45–4:35 — Automated tests

Next, I’ll open `backend/tests/test_audit_service.py`. These tests use pytest and patch `httpx.AsyncClient` with an async stub, so they never make real HTTP requests. That keeps them fast, deterministic, and safe to run anywhere.

The happy-path test supplies controlled HTML and checks the title, meta description, two H1 elements, two images missing alt text, and the expected word count. The remaining tests check an invalid URL through the API, reject a mocked PDF response with a 415, and verify that a mocked timeout produces a 408. Running `pytest` from the backend folder executes the full test suite.

## 4:35–5:15 — One further improvement

With one more day, I would add a small accessibility score built from additional signals such as document language, heading order, form labels, and descriptive image text. This would make the results more actionable than a single missing-alt count while still fitting the product’s quick-audit purpose. I left it out of this submission to keep the scope focused and to ensure the existing metrics, error handling, interface, and test coverage are polished.

## 5:15–5:30 — Closing

That concludes the Page Pulse walkthrough. Thank you for watching.
