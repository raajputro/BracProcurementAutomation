# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
import re
from utils.basic_actionsdm import BasicActionsDM


class LoginPage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.first_common_login_btn = page.locator("//button[@type='button']")
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_placeholder('password')
        self.second_common_login_btn = page.locator("//button[@type='submit']")

        # BRAC SSO
        self.sso_button = page.locator('input[type="button"][value="BRAC SSO"]')
        self.sso_user_name = page.locator("input[id='username']")
        self.sso_password = page.locator("input[id='password']")
        self.sign_in_button = page.locator("input[id='kc-login']")

        # Vendor login
        self.vendor_login_btn = page.locator("//button[@type='button']")
        self.vendor_user_name_1 = page.locator("//input[@id='Username']")
        self.vendor_password = page.locator("//input[@id='Password']")
        self.second_vendor_login_btn = page.locator("//button[@type='submit']")

    # write down all the necessary actions performed in this page as def
    def perform_login_for_common_login(self, user_name, pass_word):
        self.click_on_btn(self.first_common_login_btn)
        self.input_in_element(self.userName, user_name)
        self.input_in_element(self.passWord, pass_word)
        self.click_on_btn(self.second_common_login_btn)

    def perform_login_for_sso_login(self, user_name, pass_word):
        self.click_on_btn(self.sso_button)
        self.input_in_element(self.sso_user_name, user_name)
        self.input_in_element(self.sso_password, pass_word)
        self.click_on_btn(self.sign_in_button)

    def perform_vendor_login(self, user_name, pass_word):
        self.click_on_btn(self.vendor_login_btn)
        self.input_in_element(self.vendor_user_name_1, user_name)
        self.input_in_element(self.vendor_password, pass_word)
        self.click_on_btn(self.second_vendor_login_btn)
