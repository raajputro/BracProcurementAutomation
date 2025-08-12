from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class MainNavigationMenu(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # Logout from public side
        self.logout_button = page.locator('a:has-text("Log out")')

        # Logout from admin side
        self.logout_from_administration_button = page.locator('a:has-text("Logout")')

        self.public_tore = page.locator('a:has-text("Public store")')

    def perform_logout(self):
        self.logout_button.click()
        # self.wait_for_timeout(2000)

    def logout_from_administration(self):
        self.logout_from_administration_button.click()

    def goto_public_store(self):
        self.public_tore.click()
