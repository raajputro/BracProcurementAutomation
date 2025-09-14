import re
from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class OrderManagement(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.order_management_menu = page.locator('i[class="nav-icon fas fa-shopping-cart"]')
        self.orders_submenu = page.locator('a[href="/Admin/Order/List"][class="nav-link"]')
        self.vendor_send_backs_submenu = page.locator('a[href="/Admin/Order/VendorSendBackList"]')
        self.shipments_submenu = page.locator('a[href="/Admin/Order/ShipmentList"]')
        self.shipment_receive_submenu = page.locator('a[href="/Admin/Order/CompleteShipmentList"]')

        self.item_received_list_submenu = page.locator('a[href="/Admin/Order/CompleteOrderItemReceivedList"]')
        self.order_settlement_submenu = page.locator('a[href="/Admin/Order/OrderSettlementList"]')

        self.icon_expand = page.locator('i[class="far fa-angle-down"]')
        self.order_input = page.locator('#OrderNo')
        self.search_button = page.locator('button[id="search-orders"]')
        # self.order = page.get_by_role("textbox", name="Order")
        # self.order_input = page.locator("#OrderNo")

        self.order_view_button = page.get_by_role("link", name="View")
        # self.acknowledge_button = page.get_by_role("link", name=re.compile(r"Acknowledge", re.I))
        # self.acknowledge_button = page.get_by_role("link", name="Acknowledge")
        # self.acknowledge_button = page.locator('div.float-right:nth-child(3) > a:nth-child(1)')
        # self.acknowledge_button = page.locator('a[onclick^="openAcknowledgementModal("]')
        self.acknowledge_button = page.get_by_role("link", name="Acknowledge")
        self.acknowledge_popup_title = page.locator("modal-title", has_text="Are you sure?")
        self.close_button = page.get_by_role("button", name="×")

        self.confirm_acknowledge_yes_button = page.locator('button[type="submit"][onclick="acknowledgeSubmit()"]')

        self.edit_review_button = page.locator('a[class="btn btn-success"][onclick^="setLocation"]')

        # self.framework_order_no = page.locator('h1[class="float-left"]')

    def goto_administration_order_list(self):
        self.click_on_btn(self.order_management_menu)
        self.click_on_btn(self.orders_submenu)
        self.wait_for_timeout(2000)

    def search_order(self, order_no):
        self.order_input.click()
        self.input_in_element(self.order_input, order_no)
        self.click_on_btn(self.search_button)

    def order_details_view(self):
        # self.click_on_btn(self.order_view_button.first())
        self.order_view_button.first.click()

    def vendor_acknowledgment(self):
        self.click_on_btn(self.acknowledge_button)

    # def confirmation_acknowledgment_by_yes(self):
    #     self.click_on_btn(self.acknowledge_button)
    #     self.click_on_btn(self.confirm_acknowledge_yes_button)
    #     self.wait_for_timeout(5000)
    #     # framework_order_number = self.page.locator("text=Order Details -").text_content()
    #     # # self.wait_to_load_element(self.order_locator)
    #     # get_framework_order_number = framework_order_number.split("-")[-1].strip()
    #     # print(get_framework_order_number)
    #     # return get_framework_order_number

        framework_order_number = self.page.locator(
            'div.card-body:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)').text_content()
        # self.wait_to_load_element(self.order_locator)
        get_framework_order_number = framework_order_number
        print(get_framework_order_number)
        return get_framework_order_number

    def click_order_management_menu(self):
        self.click_on_btn(self.order_management_menu)

    # Use for search grid open
    def open_search_grid(self):
        self.click_on_btn(self.icon_expand)

    # Use for test purpose
    def input_fill(self):
        # self.click_on_btn(self.order)
        # self.input_in_element(self.order, "Fill")
        # self.page.locator("i.far.fa-angle-down").click()
        self.page.wait_for_selector("#OrderNo", state="visible")
        # Optional: wait until not disabled
        self.page.wait_for_function(
            "document.querySelector('#OrderNo') && !document.querySelector('#OrderNo').disabled")

        # Click and fill
        self.order_input.click(force=True)  # force in case something is overlapping
        self.order_input.fill("2025/TRN-2668")
