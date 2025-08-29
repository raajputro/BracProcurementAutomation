import re
from utils.basic_actions import BasicActions
from typing import Optional
from contextlib import suppress
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class EtenderLoginPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)

        # Elements
        self.login_button = page.get_by_role("button", name="LOGIN")  # Opens modal
        self.userName = page.locator("#userName")
        self.passWord = page.locator("#password")
        self.signBtn = page.locator("#loginForm > div.modal-footer > button.btn.btn-primary")  # Inside modal

    def perform_login(
        self,
        given_url: str,
        user_name: str,
        pass_word: str,
        timeout: Optional[int] = 30_000,
        post_login_selector: Optional[str] = None,
    ) -> bool:
        """Perform login using modal, wait for new page or selector to confirm success."""

        user_name = (user_name or "").strip()
        pass_word = (pass_word or "").strip()

        # Step 1: Navigate to login page
        self.page.goto(given_url, wait_until="domcontentloaded", timeout=timeout)

        # Step 2: Click "LOGIN" to open the modal
        self.login_button.wait_for(state="visible", timeout=timeout)
        self.login_button.click()

        # Step 3: Fill username and password inside modal
        self.userName.wait_for(state="visible", timeout=timeout)
        self.userName.fill(user_name, timeout=timeout)
        self.passWord.fill(pass_word, timeout=timeout)

        # Step 4: Click the actual sign-in button inside the modal
        with self.page.expect_navigation(wait_until="domcontentloaded", timeout=timeout):
            self.signBtn.click()

        # Step 5: Optionally check a selector on the post-login page
        if post_login_selector:
            try:
                self.page.wait_for_selector(post_login_selector, timeout=timeout)
                return True
            except PlaywrightTimeoutError:
                return False

        # Step 6: Fallback - basic checks
        return self.page.url != given_url and not self.signBtn.is_visible()