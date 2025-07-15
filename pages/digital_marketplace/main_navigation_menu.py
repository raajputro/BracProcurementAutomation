from utils.basic_actionsdm import BasicActionsDM


class MainNavigationMenu(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.exit_button = page.locator("a#ico-logout./logout")

        self.logout_button = self.page.locator('a:has-text("Log out")')
        # self.first_common_login_btn = page.locator("//button[@type='button']")

    def perform_logout(self, logout_button):
        # self.click_on_btn(self.logout_button)
        self.logout_button.click()
        # self.exit_button.click()
        self.wait_for_timeout(1000)
        # self.logout_button.click()
