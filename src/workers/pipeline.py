from src.automation.browser import browser_session
from src.workers.login_worker import LoginWorker


def run_pipeline() -> None:
    with browser_session() as (_, __, page):
        login_worker = LoginWorker(page=page)
        login_worker.login_noya()
        login_worker.save_debug_screenshot()
