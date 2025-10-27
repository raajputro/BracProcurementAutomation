# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
import re
from utils.basic_actionsdm import BasicActionsDM
from typing import Optional
from contextlib import suppress
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class ProcurementLoginPage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_label('Password')
        # self.signBtn = page.get_by_role('button', name=re.compile(r"^(Sign In|login)$", re.I))
        self.signBtn = page.locator('xpath=//input[@id="kc-login"]')
        # self.signBtn = page.locator('//*[@id="kc-login"]')

        self.advModal = page.locator('#modals')
        self.advCloseBtn = page.locator('xpath=//*[@id="modals"]/div[1]/button')
        self.overlayModal = page.locator('#overlay.active')

    # write down all the necessary actions performed on this page as def
    def perform_login(
            self,
            given_url: str,
            user_name: str,
            pass_word: str,
            timeout: Optional[int] = 40_000,
            post_login_selector: Optional[str] = None,  # fallback dashboard shell
    ) -> bool:
        """Log in robustly; handle post-login overlay; verify success."""
        user_name = (user_name or "").strip()
        pass_word = (pass_word or "").strip()

        # 1) Navigate and wait for form
        self.page.goto(given_url, wait_until="domcontentloaded", timeout=timeout)
        self.userName.wait_for(state="visible", timeout=timeout)
        self.userName.clear()
        self.userName.fill(user_name, timeout=timeout)
        self.passWord.clear()
        self.passWord.fill(pass_word, timeout=timeout)

        # 2) Click login
        self.signBtn.click(timeout=timeout)

        # 3) Wait for either overlay or dashboard
        overlay_seen = False
        try:
            self.overlayModal.wait_for(state="visible", timeout=6000)
            overlay_seen = True
        except PlaywrightTimeoutError:
            pass

        if overlay_seen:
            # Close overlay
            try:
                self.click_on_btn(self.advCloseBtn, timeout=timeout)
            except PlaywrightTimeoutError:
                with suppress(Exception):
                    self.page.keyboard.press("Escape")

        # 4) Final success check
        if post_login_selector:
            try:
                self.page.wait_for_selector(post_login_selector, timeout=timeout)
                return True
            except PlaywrightTimeoutError:
                return False

        # Fallback: URL change and login button gone
        return self.page.url != given_url and not self.signBtn.is_visible()
# Previous code
# import re
#
# from utils.basic_actionsdm import BasicActionsDM
#
#
# class ProcurementLoginPage(BasicActionsDM):
#     def __init__(self, page):
#         super().__init__(page)
#         # write down all the elements here with locator format
#         self.userName = page.get_by_label('Username')
#         self.passWord = page.get_by_label('Password')
#         self.signBtn = page.get_by_role('button', name=re.compile("Sign In", re.IGNORECASE))
#         self.advModal = page.locator('#modals')
#
#     # write down all the necessary actions performed in this page as def
#     def perform_login(self, user_name, pass_word):
#         self.input_in_element(self.userName, user_name)
#         self.input_in_element(self.passWord, pass_word)
#         self.click_on_btn(self.signBtn)
#         self.wait_to_load_element(self.advModal)
#         self.page.keyboard.press('Enter')
