# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class MainNavigationBar(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.exit_button = page.locator("a#btn_login.btn_user")

        self.logout_button = self.page.locator('a:has-text("Log out")')

    # write down all the necessary actions performed on this page as def
    def exit(self):
        # self.page.locator('#overlay.active').wait_for(state='detached', timeout=10000)
        self.exit_button.click()
        self.wait_for_timeout(1000)

    def logout(self):
        self.logout_button.click()