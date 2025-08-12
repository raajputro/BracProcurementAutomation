from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class OrdersPublicStore(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.search_order_input = page.locator('input[placeholder="Order Number/Reference No"]')
        self.initiator_toggle_button = page.locator('button[class="toggle-button collapsed-button btn"]')
        self.details_button = page.get_by_role("button", name="Details")
        self.order_search_button = page.locator('button[class="search-box-button"]')

    def search_order_no_or_reference_no(self, order_no):
        self.click_on_btn(self.search_order_input)
        self.input_in_element(self.search_order_input, order_no)
        self.click_on_btn(self.order_search_button)

    def order_info_view_by_toggle(self):
        self.initiator_toggle_button.first.click()

    def view_order_details(self):
        self.details_button.first.click()
        self.wait_for_timeout(2000)
