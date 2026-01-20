from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class MainNavigationMenu(HomePage, BasicActionsDM):
    def __init__(self, page, logger=None):
        super().__init__(page)
        self.logger = logger
        # Logout from public side
        self.logout_button = page.locator('a:has-text("Log out")')

        # Logout from admin side
        self.logout_from_administration_button = page.locator('a:has-text("Logout")')

        self.public_tore = page.locator('a:has-text("Public store")')

    ##################### small helper so we can log easily #####################
    def _log(self, message: str):
        if self.logger:
            self.logger.step(message)

    def perform_logout(self):
        self.logout_button.click()
        # self.wait_for_timeout(2000)

    def logout_from_administration(self):
        self.logout_from_administration_button.click()

    def goto_public_store(self):
        self.public_tore.click()
