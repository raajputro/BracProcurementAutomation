# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
import re
from utils.basic_actions import BasicActions

class LoginPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_label('Password')
        self.signBtn = page.get_by_role('button', name=re.compile(r"^(Sign In|login)$", re.I))

        self.advModal = page.locator('#modals')
        self.advCloseBtn = page.locator('xpath=//*[@id="modals"]/div[1]/button')
        self.overlayModal = page.locator('#overlay.active')


    # write down all the necessary actions performed in this page as def
    # def perform_login(self, given_url, user_name, pass_word):
    #     self.navigate_to_url(given_url)
    #     self.input_in_element(self.userName, user_name)
    #     self.input_in_element(self.passWord, pass_word)
    #     self.click_on_btn(self.signBtn)
    #     # self.page.wait_for_timeout(5000)
    #     while True:
    #         try:
    #             if self.overlayModal.is_visible():
    #                 print("Advertise modal is visible")
    #                 self.click_on_btn(self.advCloseBtn)
    #                 break
    #             # else:
    #             #     self.page.keyboard.press("Enter")
    #         except Exception as e:
    #             print(e)

    def perform_login(self, given_url, user_name, pass_word):
        # Navigate & fill creds
        self.navigate_to_url(given_url)
        self.input_in_element(self.userName, user_name)
        self.input_in_element(self.passWord, pass_word)

        # Submit
        self.click_on_btn(self.signBtn)

        # --- Dismiss optional overlays if they show up, else move on ---
        # 1) Try overlayModal first (fast poll)
        try:
            # wait briefly for overlay to become visible
            self.overlayModal.wait_for(state="visible", timeout=1500)
            # if visible, click the close button (same close used for adv modal)
            self.click_on_btn(self.advCloseBtn)
            return
        except Exception:
            pass

        # 2) Try advModal
        try:
            self.advModal.wait_for(state="visible", timeout=1500)
            # Close if button is present/visible
            try:
                if self.advCloseBtn.is_visible():
                    self.click_on_btn(self.advCloseBtn)
            except Exception:
                # fallback: try pressing Escape if close button isn’t visible
                try:
                    self.page.keyboard.press("Escape")
                except Exception:
                    pass
        except Exception:
            # Neither modal appeared — just continue with the next steps
            pass
