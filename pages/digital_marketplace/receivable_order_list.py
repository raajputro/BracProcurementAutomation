import re
from pages.digital_marketplace.order_management import OrderManagement
from pathlib import Path

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

        self.challan_no = page.locator('textarea[id="challanNumber"]')
        self.all_item_select = page.locator('input[id="allItemSelect"]')
        self.item_select = page.locator('input[type="checkbox"]')
        self.quantity_to_receive = page.locator('input[class="qty-input commonInput"][type="number"]')
        self.received_remarks = page.locator('input[id="receivedRemarksText"]')
        self.submit_received_items = page.locator('button[id="receiveAllItems"]')

        self.x_icon = page.locator('button[class="close"]')
        self.cancel_button = page.get_by_role("button", name=re.compile(r"Cancel", re.I))
        self.confirm_button = page.locator('button[onclick="confirmReceiveSettlement()"]')

        self.receiving_attachment_upload_input = page.locator('input[id="itemAttachment"]')

    def goto_receivable_order_list(self):
        # self.click_on_btn(self.order_management_menu)
        self.click_on_btn(self.receivable_order_list_submenu)
        self.wait_for_timeout(2000)

    def search_receivable_order(self, receivable_order_number):
        self.order_input.click()
        self.input_in_element(self.order_input, receivable_order_number)
        self.click_on_btn(self.search_button)

    def receivable_order_view(self):
        self.order_view_button.first.click()

    def challan_no_input(self, fill_challan_no):
        self.click_on_btn(self.challan_no)
        self.input_in_element(self.challan_no, fill_challan_no)
        self.wait_for_timeout(2000)

    def receivable_item_select(self):
        # self.item_select.nth(0).click()
        self.item_select.nth(1).check()

    def input_quantity_to_receive(self, received_quantity):
        self.quantity_to_receive.click()
        self.quantity_to_receive.clear()
        self.input_in_element(self.quantity_to_receive, received_quantity)
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

    # def upload_file_1(self, file_path: str, container: str = "#receivedRemarksDiv", index: int = 0,
    #                   timeout: int = 30000):
    #     p = Path(file_path).expanduser().resolve()
    #     if not p.exists():
    #         raise FileNotFoundError(f"File not found: {p}")
    #
    #     file_input = self.page.locator(f"{container} input[type='file']")
    #     file_input.wait_for(state="attached", timeout=timeout)
    #     file_input.set_input_files(str(p))
    #
    #     return True

    def receiving_upload_attachment(self, file_path: str, timeout: int = 10000) -> bool:
        try:
            # Ensure file exists
            p = Path(file_path).expanduser().resolve(strict=True)
            print(f"Uploading file path: {p}")

            # Wait for input to be attached in DOM
            self.receiving_attachment_upload_input.wait_for(state="attached", timeout=timeout)

            # Upload file
            self.receiving_attachment_upload_input.set_input_files(str(p))

            # Debug: check the value after upload
            input_value = self.receiving_attachment_upload_input.input_value()
            print(f"File input value: {input_value}")

            # Success if input has any non-empty value
            if input_value.strip():
                print(f"Successfully uploaded attachment name: {p.name}")
                return True

            print("File input value is empty after upload.")
            return False

        except Exception as e:
            print(f"File upload failed: {e}")
            return False
