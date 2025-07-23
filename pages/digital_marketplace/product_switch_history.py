from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class ProductSwitchHistory(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page



    # def view_product_history(self, product_id: str):
    #     # # product_id = "2960"
    #     # page.locator('a[href*="Requisition/History?requisitionProductId="]').click()
    #     # # self.click_on_btn(self.product_history)
    #     # # self.wait_for_timeout(2000)
    #     # product_id = "2960"
    #     history_link = page.locator(f'a[href*="Requisition/History?requisitionProductId={product_id}"]')
    #
    #     if history_link.is_visible():
    #         print("History link is visible")
    #         self.history_link.click()
    #         self.wait_for_timeout(2000)
    #     else:
    #         print("History link is not visible")
