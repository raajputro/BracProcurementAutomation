import re
from utils.basic_actions import BasicActions

class ProcurementLoginPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.userName = page.get_by_label('Username')
        self.passWord = page.get_by_label('Password')
        self.signBtn = page.get_by_role('button', name=re.compile("Sign In", re.IGNORECASE))
        self.advModal = page.locator('#modals')

    # write down all the necessary actions performed in this page as def
    def perform_login(self, user_name, pass_word):
        self.input_in_element(self.userName, user_name)
        self.input_in_element(self.passWord, pass_word)
        self.click_on_btn(self.signBtn)
        self.wait_to_load_element(self.advModal)
        self.page.keyboard.press('Enter')