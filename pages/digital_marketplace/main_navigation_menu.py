from utils.basic_actionsdm import BasicActionsDM


class MainNavigationMenu(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # Logout from public side
        self.logout_button = page.locator('a:has-text("Log out")')

        # Logout from admin side
        self.logout_from_administration_button = page.locator('a:has-text("Logout")')

    def perform_logout(self):
        self.logout_button.click()
        # self.wait_for_timeout(2000)

    def logout_from_administration(self):
        self.logout_from_administration_button.click()
