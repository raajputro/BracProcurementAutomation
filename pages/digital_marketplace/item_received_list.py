from pages.digital_marketplace.order_management import OrderManagement
from utils.basic_actionsdm import BasicActionsDM


class ItemReceivedList(OrderManagement, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.item_received_list_submenu = page.locator('a[href="/Admin/Order/CompleteOrderItemReceivedList"]')

        self.order_number_input = page.locator('#OrderNo')
        self.search_button_for_received_item = page.locator('button[id="search-complete-order-item-received-list"]')
        self.order_view_button = page.get_by_role("link", name="View")
        self.challan_no_input = page.locator('input[id="ChallanNo"]')

    def goto_received_order_list(self):
        # self.click_on_btn(self.order_management_menu)
        self.click_on_btn(self.item_received_list_submenu)
        self.wait_for_timeout(2000)

    def search_received_order(self, received_order_number):
        self.order_number_input.click()
        self.input_in_element(self.order_number_input.nth(0), received_order_number)
        self.click_on_btn(self.search_button_for_received_item)

    def received_order_view(self):
        # self.click_on_btn(self.order_view_button.first())
        self.order_view_button.first.click()
        # self.order_view_button.nth(0).click()

    def searched_received_order(self, challan_no):
        self.input_in_element(self.challan_no_input.nth(0), challan_no)
