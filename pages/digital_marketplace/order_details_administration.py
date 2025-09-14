import re
from pages.digital_marketplace.order_management import OrderManagement
from pages.digital_marketplace.vendor_dashboard import VendorDashboard
from utils.basic_actionsdm import BasicActionsDM


class OrderDetailsAdministration(VendorDashboard, OrderManagement, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # self.acknowledge_button = page.locator('a[onclick^="openAcknowledgementModal("]')
        self.acknowledge_button = page.get_by_role("link", name="Acknowledge")
        self.acknowledge_popup_title = page.locator("modal-title", has_text="Are you sure?")
        self.close_button = page.get_by_role("button", name="×")

        # self.confirm_acknowledge_yes_button = page.locator('button[type="submit"][onclick^="acknowledgeSubmit"]')
        self.yes_button = page.get_by_role("button", name="Yes")
        self.edit_review_button = page.locator('a[class="btn btn-success"][onclick^="setLocation"]')

        self.back_to_order_list = page.get_by_role("link", name="back to order list")

    def vendor_acknowledgment(self):
        self.click_on_btn(self.acknowledge_button)

    def confirmation_acknowledgment_by_yes(self):
        self.click_on_btn(self.acknowledge_button)
        self.click_on_btn(self.yes_button)
        # self.wait_for_timeout(5000)
        framework_order_number = self.page.locator(
            'div.card-body:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)').text_content()
        # self.wait_to_load_element(self.order_locator)
        get_framework_order_number = framework_order_number
        print("Get work order number: " + get_framework_order_number)
        self.wait_for_timeout(5000)
        order_status_vendor_acknowledged = self.page.locator(
            '//*[@id="order-info"]/div[5]/div[1]/div/div[5]/div[2]/div').text_content()
        order_status = order_status_vendor_acknowledged
        print("Order status: " + order_status)
        # //*[@id="order-info"]/div[5]/div[1]/div/div[5]/div[2]/div
        return get_framework_order_number

    def click_back_to_order_list(self):
        self.back_to_order_list.click()
        print("Navigated back to order list")

    def click_order_management_menu(self):
        self.click_on_btn(self.order_management_menu)
