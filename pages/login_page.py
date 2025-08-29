# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
import re
from utils.basic_actions import BasicActions
from typing import Optional
from contextlib import suppress
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_label('Password')
        #self.signBtn = page.get_by_role('button', name=re.compile(r"^(Sign In|login)$", re.I))
        self.signBtn = page.locator('xpath=//input[@id="kc-login"]')

        self.advModal = page.locator('#modals')
        self.advCloseBtn = page.locator('xpath=//*[@id="modals"]/div[1]/button')
        self.overlayModal = page.locator('#overlay.active')
        self.officeDropdown = page.locator('#officeIdDiv_arrow')
        self.goBtn = page.locator('//input[@type="button" and @value="Go"]')
        self.logoutBtn = page.locator('//input[@type="button" and @value="Logout"]')

        self.exit_button = page.locator("a#btn_login.btn_user")
        self.logout_button = self.page.locator('a:has-text("Logout")')

        # Navigation Locators
        self.main_nav = self.page.locator('//*[@class="top_nav_container"]')


    def navigate_to_page(self, main_nav_val, sub_nav_val):
        # Navigate via Main Nav
        self.main_nav.get_by_text(main_nav_val).click()
        self.page.wait_for_timeout(5000)

        '''Sub menu level is 2, then we go from parent to first child'''
        try:
            # Navigate to Parent Sub Menu
            parent_item = self.page.locator(
                f'xpath=//li[@class="menu-parent"]/div[contains(text(),"{sub_nav_val[0]}")]')
            self.wait_to_load_element(parent_item)
            parent_item.click()
            if len(sub_nav_val) == 3:
                sub_item_1 = self.page.locator(
                    f'xpath=//li[@class="sub_arrow"]//child::div/span[text()="{sub_nav_val[1]}"]').first
                sub_item_2 = self.page.get_by_role("link", name=sub_nav_val[2])
                self.wait_to_load_element(sub_item_1)
                sub_item_1.hover()
                self.wait_to_load_element(sub_item_2)
                sub_item_2.click()
            elif len(sub_nav_val) == 2:
                sub_item_1 = self.page.get_by_role("link", name=sub_nav_val[1])
                self.wait_to_load_element(sub_item_1)
                sub_item_1.click()
            else:
                print(f"Please check your sec_menu list and update it properly!")

            self.page.wait_for_timeout(5000)
            self.get_full_page_screenshot(f"{main_nav_val} Navigation Success")
            print(f"{main_nav_val} Navigation Success!!")
        except Exception as e:
            print(f"Missing {e}")


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
            timeout: Optional[int] = 30_000,
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
        # self.page.reload()

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


#     def perform_login(
#     self,
#     given_url: str,
#     user_name: str,
#     pass_word: str,
#     timeout: Optional[int] = 30_000,
#     post_login_selector: Optional[str] = None,  # fallback dashboard shell
# ) -> bool:
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
#         self.page.reload()
#         # 3) Wait for either overlay or dashboard
#         overlay_seen = False
#         try:
#             self.overlayModal.wait_for(state="visible", timeout=5000)
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

