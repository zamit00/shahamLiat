from contextlib import contextmanager

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.core.config import settings


@contextmanager
def browser_session() -> tuple[Browser, BrowserContext, Page]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        try:
            yield browser, context, page
        finally:
            context.close()
            browser.close()
