import re

from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage

from playwright.sync_api import expect


class AllOrderForAdminPage(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # Search order reference number
        # self.search_order_number = page.get_by_placeholder('Order Number/Reference No')
        self.search_order_number = page.locator('input[class="searchOrderInput"]')
        self.search_button = page.locator('button[class="search-box-button"][type="submit"]')

        # Go to order details page from all orders
        self.details_button = page.get_by_role("button", name="Details")
        # self.details_button = page.locator('button[class="search-box-button"]')
        self.preview_button = page.locator("a[class='button-2 print-order-button']")

        self.click_administration_link = page.locator('a[class="administration"]')
        self.admin_view_toggle_button = page.locator('button[class="toggle-button collapsed-button btn"]')

    def admin_order_search(self, search_number):
        self.search_order_number.click()
        # self.wait_for_timeout(5000)
        self.input_in_element(self.search_order_number, search_number)
        # self.wait_for_timeout(5000)
        # self.wait_for_timeout(2000)
        self.click_on_btn(self.search_button)
        self.wait_for_timeout(2000)

    def admin_goes_to_order_details(self):
        self.details_button.first.click()
        self.wait_for_timeout(5000)
        # vendor_username = self.page.locator("//div[@class='order-overview']//table//tr[2]/td[2]")
        # vendor_username = self.page.locator("//td[normalize-space(text())='Vendor Name:']/following-sibling::td/text()")

        # vendor_username = self.page.locator(
        #     "body > div.master-wrapper-page > div.master-wrapper-content > div > div > div > div.page-body > div.order-overview > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(2)"
        # )
        # print(vendor_username)
        # return vendor_username

    def view_order_info_for_admin(self):
        self.admin_view_toggle_button.first.click()

    def goto_admin_dashboard(self):
        self.click_on_btn(self.click_administration_link)
        self.wait_for_timeout(5000)
