from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LoginWorker:
    def __init__(self, page: Page):
        self.page = page

    def login_noya(self) -> None:
        if not settings.noya_username or not settings.noya_password:
            raise ValueError("Missing credentials. Set NOYA_USERNAME and NOYA_PASSWORD in .env")

        logger.info("opening_login_page", url=settings.noya_url)
        self.page.goto(settings.noya_url, wait_until="domcontentloaded")

        email_selector = "input#input_1[name='username'], input[name='username'], input#email[data-testid='login-email']"
        password_selector = "input#input_2[name='password'], input[name='password'], input#password[data-testid='login-password']"
        self._ensure_login_form_ready(email_selector, password_selector)

        self._fill_controlled_input(email_selector, settings.noya_username)
        self._fill_controlled_input(password_selector, settings.noya_password)

        logger.info("credentials_filled_waiting_for_manual_submit")

    def _handle_otp_if_present(self) -> None:
        otp_input = self.page.locator(
            "input[name='otp'], input[inputmode='numeric'], input[autocomplete='one-time-code']"
        ).first
        try:
            otp_input.wait_for(timeout=5000)
        except PlaywrightTimeoutError:
            logger.info("otp_not_detected")
            return

        logger.info("otp_detected_waiting_for_user", timeout_seconds=settings.otp_wait_seconds)
        otp = input("Enter OTP from SMS/Auth app: ").strip()
        if not otp:
            raise ValueError("OTP is required to continue login flow.")

        otp_input.fill(otp)
        self.page.locator("button:has-text('Verify'), button[type='submit']").first.click()
        self.page.wait_for_timeout(2000)

    def _fill_controlled_input(self, selector: str, value: str) -> None:
        field = self.page.locator(selector).first
        field.wait_for(state="visible", timeout=30000)
        field.click()
        field.fill(value)

        # React-like controlled forms sometimes need real input/change events.
        handle = field.element_handle()
        if handle:
            self.page.evaluate(
                """([el, nextValue]) => {
                    el.value = nextValue;
                    el.dispatchEvent(new Event("input", { bubbles: true }));
                    el.dispatchEvent(new Event("change", { bubbles: true }));
                }""",
                [handle, value],
            )

        current_value = field.input_value()
        if current_value != value:
            raise RuntimeError(f"Failed to set value for selector: {selector}")

    def _handle_new_session_gate(self) -> None:
        try:
            self.page.locator("#newSessionDIV").first.wait_for(state="visible", timeout=3000)
            logger.info("new_session_gate_detected_clicking_link", source="newSessionDIV")
            self.page.locator("#newSessionDIV a:has-text('לחץ כאן')").first.click()
            self.page.wait_for_load_state("domcontentloaded")
            return
        except PlaywrightTimeoutError:
            pass

        # Fallback for variants of the same error screen.
        fallback_link = self.page.locator("a:has-text('לחץ כאן'), a[href='/']").first
        try:
            fallback_link.wait_for(state="visible", timeout=3000)
            logger.info("new_session_gate_detected_clicking_link", source="fallback_link")
            fallback_link.click()
            self.page.wait_for_load_state("domcontentloaded")
        except PlaywrightTimeoutError:
            logger.info("new_session_gate_not_detected")

    def _ensure_login_form_ready(self, email_selector: str, password_selector: str) -> None:
        for attempt in range(1, 5):
            email_ready = self.page.locator(email_selector).first.is_visible()
            password_ready = self.page.locator(password_selector).first.is_visible()
            if email_ready and password_ready:
                logger.info("login_form_ready", attempt=attempt)
                return

            self._handle_new_session_gate()
            self.page.wait_for_timeout(700)

        raise RuntimeError("Login form was not available after handling session gate.")

    def save_debug_screenshot(self, filename: str = "post_login.png") -> Path:
        out = Path(settings.storage_dir) / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(out), full_page=True)
        logger.info("screenshot_saved", path=str(out))
        return out
