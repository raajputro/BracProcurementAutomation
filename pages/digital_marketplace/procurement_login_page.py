# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
import re
from utils.basic_actionsdm import BasicActionsDM
from typing import Optional
from contextlib import suppress
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class ProcurementLoginPage(BasicActionsDM):
    def __init__(self, page, logger=None):
        super().__init__(page)
        self.logger = logger
        # write down all the elements here with locator format
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_label('Password')
        # self.signBtn = page.get_by_role('button', name=re.compile(r"^(Sign In|login)$", re.I))
        self.signBtn = page.locator('xpath=//input[@id="kc-login"]')
        # self.signBtn = page.locator('//*[@id="kc-login"]')

        self.advModal = page.locator('#modals')
        self.advCloseBtn = page.locator('xpath=//*[@id="modals"]/div[1]/button')
        self.overlayModal = page.locator('div#overlay.active')
        # self.overlayModal = page.locator('#overlay.active')
        self.modal_close_button = page.locator("//div[@class='modals-header']//button[@class='close-button']")

        self.officeDropdown = page.locator('#officeIdDiv_arrow')
        self.goBtn = page.locator('//input[@type="button" and @value="Go"]')
        self.logoutBtn = page.locator('//input[@type="button" and @value="Logout"]')

        self.exit_button = page.locator("a#btn_login.btn_user")
        self.logout_button = self.page.locator('a:has-text("Logout")')

    ##################### small helper so we can log easily #####################
    def _log(self, message: str):
        if self.logger:
            self.logger.step(message)

    def perform_logout(self):
        self.wait_to_load_element(self.exit_button)
        self.exit_button.click()
        self.wait_to_load_element(self.logout_button)
        self.logout_button.click()

    def perform_login(
            self,
            given_url: str,
            user_name: str,
            pass_word: str,
            branch_code: Optional[str] = "0",
            timeout: Optional[int] = 50_000,
            post_login_selector: Optional[str] = None,  # fallback dashboard shell
    ) -> None:
        # -----
        # ------
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

        # 3) If branch code given, then select branch code
        if branch_code != "0":
            self.wait_to_load_element(self.officeDropdown)
            self.officeDropdown.click()
            self.page.get_by_text(branch_code).click()
            self.click_on_btn(self.goBtn)

        # # After selecting branch code, we expected an overlay should be seen
        # # But this overlay is not available in all Test Environments or have
        # # different loading time in different network speed or environment
        # # therefore, a reload is being introduced, just to bypass it........

        # # 4) Reload the page
        self.page.wait_for_timeout(2000)
        self.page.reload()
        self.page.wait_for_timeout(2000)

    # write down all the necessary actions performed on this page as def
    # def perform_login(
    #         self,
    #         given_url: str,
    #         user_name: str,
    #         pass_word: str,
    #         timeout: Optional[int] = 50_000,
    #         post_login_selector: Optional[str] = None,  # fallback dashboard shell
    # ) -> bool:
    #
    #     # -----
    #     # ------
    #     """Log in robustly; handle post-login overlay; verify success."""
    #     user_name = (user_name or "").strip()
    #     pass_word = (pass_word or "").strip()
    #
    #     # 1) Navigate and wait for form
    #     self.page.goto(given_url, wait_until="domcontentloaded", timeout=timeout)
    #     self.userName.wait_for(state="visible", timeout=timeout)
    #     self.userName.clear()
    #     self.userName.fill(user_name, timeout=timeout)
    #     self.passWord.clear()
    #     self.passWord.fill(pass_word, timeout=timeout)
    #
    #     # 2) Click login
    #     self.signBtn.click(timeout=timeout)
    #
    #     # 3) Wait for either overlay or dashboard
    #     overlay_seen = False
    #     try:
    #         self.overlayModal.wait_for(state="visible", timeout=6000)
    #         overlay_seen = True
    #     except PlaywrightTimeoutError:
    #         pass
    #
    #     if overlay_seen:
    #         # Close overlay
    #         try:
    #             # self.click_on_btn(self.advCloseBtn, timeout=timeout)
    #             self.click_on_btn(self.modal_close_button, timeout=timeout)
    #         except PlaywrightTimeoutError:
    #             with suppress(Exception):
    #                 self.page.keyboard.press("Escape")
    #
    #     # 4) Final success check
    #     if post_login_selector:
    #         try:
    #             self.page.wait_for_selector(post_login_selector, timeout=timeout)
    #             return True
    #         except PlaywrightTimeoutError:
    #             return False
    #
    #     # Fallback: URL change and login button gone
    #     return self.page.url != given_url and not self.signBtn.is_visible()

# # this is an object of samplePage to automate, which contains all elements
# # and actions could be performed, like input, verify, etc.
# import re
# from utils.basic_actionsdm import BasicActionsDM
# from typing import Optional
# from contextlib import suppress
# from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
#
#
# class ProcurementLoginPage(BasicActionsDM):
#     def __init__(self, page):
#         super().__init__(page)
#         # write down all the elements here with locator format
#         self.userName = page.get_by_label('Username')
#         self.passWord = page.get_by_label('Password')
#         # self.signBtn = page.get_by_role('button', name=re.compile(r"^(Sign In|login)$", re.I))
#         self.signBtn = page.locator('xpath=//input[@id="kc-login"]')
#         # self.signBtn = page.locator('//*[@id="kc-login"]')
#
#         self.advModal = page.locator('#modals')
#         self.advCloseBtn = page.locator('xpath=//*[@id="modals"]/div[1]/button')
#         self.overlayModal = page.locator('#overlay.active')
#
#     # write down all the necessary actions performed on this page as def
#     def perform_login(
#             self,
#             given_url: str,
#             user_name: str,
#             pass_word: str,
#             timeout: Optional[int] = 40_000,
#             post_login_selector: Optional[str] = None,  # fallback dashboard shell
#     ) -> bool:
#         """Log in robustly; handle post-login overlay; verify success."""
#         user_name = (user_name or "").strip()
#         pass_word = (pass_word or "").strip()
#
#         # 1) Navigate and wait for form
#         self.page.goto(given_url, wait_until="domcontentloaded", timeout=timeout)
#         self.userName.wait_for(state="visible", timeout=timeout)
#         self.userName.clear()
#         self.userName.fill(user_name, timeout=timeout)
#         self.passWord.clear()
#         self.passWord.fill(pass_word, timeout=timeout)
#
#         # 2) Click login
#         self.signBtn.click(timeout=timeout)
#
#         # 3) Wait for either overlay or dashboard
#         overlay_seen = False
#         try:
#             self.overlayModal.wait_for(state="visible", timeout=6000)
#             overlay_seen = True
#         except PlaywrightTimeoutError:
#             pass
#
#         if overlay_seen:
#             # Close overlay
#             try:
#                 self.click_on_btn(self.advCloseBtn, timeout=timeout)
#             except PlaywrightTimeoutError:
#                 with suppress(Exception):
#                     self.page.keyboard.press("Escape")
#
#         # 4) Final success check
#         if post_login_selector:
#             try:
#                 self.page.wait_for_selector(post_login_selector, timeout=timeout)
#                 return True
#             except PlaywrightTimeoutError:
#                 return False
#
#         # Fallback: URL change and login button gone
#         return self.page.url != given_url and not self.signBtn.is_visible()
# # Previous code
# # import re
# #
# # from utils.basic_actionsdm import BasicActionsDM
# #
# #
# # class ProcurementLoginPage(BasicActionsDM):
# #     def __init__(self, page):
# #         super().__init__(page)
# #         # write down all the elements here with locator format
# #         self.userName = page.get_by_label('Username')
# #         self.passWord = page.get_by_label('Password')
# #         self.signBtn = page.get_by_role('button', name=re.compile("Sign In", re.IGNORECASE))
# #         self.advModal = page.locator('#modals')
# #
# #     # write down all the necessary actions performed in this page as def
# #     def perform_login(self, user_name, pass_word):
# #         self.input_in_element(self.userName, user_name)
# #         self.input_in_element(self.passWord, pass_word)
# #         self.click_on_btn(self.signBtn)
# #         self.wait_to_load_element(self.advModal)
# #         self.page.keyboard.press('Enter')
