import re
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage

from playwright.sync_api import expect


class PendingApprovalOrders(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        # write down all the elements here with locator format
        # multiselect order approve
        self.pending_approval_orders = page.locator("a[href='/customer/pendingApprovalOrders']",
                                                    has_text="Pending Approval Orders")
        # Pending Approval Order Checkbox
        self.pending_approval_checkbox = page.locator("input#pendingApprovalOrder")

        # Search order reference number
        self.search_order_number = page.get_by_placeholder('Order Reference Number')
        # self.search_order_input = page.locator("input.searchOrderInput")
        self.search_button = page.locator('button[class="button"][type="submit"]')

        # Select approve button for multiselect approval
        self.click_multiselect_approve = page.locator('button[id="pendingApprovalOrder-selected"]')

    def goto_pending_approval_orders_list(self):
        self.click_on_btn(self.pending_approval_orders)
        self.wait_for_timeout(2000)
        # self.pending_approval_checkbox.check()
        # self.wait_for_timeout(2000)
        # self.pending_approval_checkbox.uncheck()
        # self.wait_for_timeout(2000)

    def check_pending_approval(self):
        self.pending_approval_checkbox.check()
        self.wait_for_timeout(2000)

    def uncheck_pending_approval(self):
        self.pending_approval_checkbox.uncheck()
        self.wait_for_timeout(2000)

    def search_order_input(self, order_reference_number):
        self.input_in_element(self.search_order_number, order_reference_number)
        self.wait_for_timeout(2000)
        self.click_on_btn(self.search_button)
        self.wait_for_timeout(2000)

    def multiselect_approve(self):
        self.click_on_btn(self.click_multiselect_approve)
        self.wait_for_timeout(2000)
