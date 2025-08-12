import re
from pages.digital_marketplace.order_management import OrderManagement
from utils.basic_actionsdm import BasicActionsDM


class ReceivableOrderListPage(OrderManagement, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # self.order_management_menu = page.locator('i[class="nav-icon fas fa-shopping-cart"]')
        self.receivable_order_list_submenu = page.locator('a[href="/Admin/Order/ReceivableOrderList"]')
        self.order_input = page.locator('#OrderNo')
        self.search_button = page.locator('button[id="search-orders"]')
        self.order_view_button = page.get_by_role("link", name="View")

        self.challan_no = page.locator('input[id="challanNumber"]')
        self.item_select = page.locator('input[type="checkbox"]')
        self.quantity_to_receive = page.locator('input[type="number"]')
        self.received_remarks = page.locator('input[id="receivedRemarksText"]')
        self.submit_received_items = page.locator('button[id="receiveAllItems"]')

        self.x_icon = page.locator('button[class="close"]')
        self.cancel_button = page.get_by_role("button", name=re.compile(r"Cancel", re.I))
        self.confirm_button = page.locator('button[onclick="confirmReceiveSettlement()"]')

    def goto_receivable_order_list(self):
        # self.click_on_btn(self.order_management_menu)
        self.click_on_btn(self.receivable_order_list_submenu)
        self.wait_for_timeout(2000)

    def search_receivable_order(self, receivable_order_number):
        self.order_input.click()
        self.input_in_element(self.order_input, receivable_order_number)
        self.click_on_btn(self.search_button)

    def receivable_order_view(self):
        # self.click_on_btn(self.order_view_button.first())
        self.order_view_button.first.click()

    def challan_no_input(self, fill_challan_no):
        self.click_on_btn(self.challan_no)
        self.input_in_element(self.challan_no, fill_challan_no)

    def receivable_item_select(self):
        # self.item_select.nth(0).click()
        self.item_select.nth(1).check()

    def input_quantity_to_receive(self, received_quantity):
        self.quantity_to_receive.nth(1).click()
        self.quantity_to_receive.nth(1).clear()
        self.input_in_element(self.quantity_to_receive.nth(1), received_quantity)
        self.wait_for_timeout(2000)

    def input_received_remarks(self, receiving_remarks):
        self.click_on_btn(self.received_remarks)
        self.input_in_element(self.received_remarks, receiving_remarks)
        self.wait_for_timeout(2000)

    def open_item_receive_popup(self):
        self.click_on_btn(self.submit_received_items)

    def close_item_receive_popup(self):
        self.click_on_btn(self.cancel_button)

    def confirm_receivable_order(self):
        self.click_on_btn(self.confirm_button)
        self.wait_for_timeout(5000)
        # self.navigate_to_url("https://stgmarketplace.brac.net/Admin/Order/CompleteOrderItemReceivedList")
        self.navigate_to_url("https://qamarketplace.bracits.com/Admin/Order/CompleteOrderItemReceivedList")
        self.wait_for_timeout(2000)
