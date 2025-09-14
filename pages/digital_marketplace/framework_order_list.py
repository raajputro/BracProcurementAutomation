from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect
from pages.digital_marketplace.procurement_home_page import ProcurementHomePage


class FrameworkOrderListPage(ProcurementHomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)

        self.page = page
        self.search_box = page.locator("input[placeholder='Search Framework Order No']")
        self.search_button = page.locator("span[onclick='getFrameWorkOrderList(true)']")
        self.table_rows = page.locator("#pending-acknowledgement-report-grid tbody tr")

    def search_framework_order(self, fa_order_no: str):
        self.search_box.fill(fa_order_no)
        self.search_button.click()
        self.page.wait_for_timeout(1000)
        print(f"Searched for Framework Order No. : {fa_order_no}")

    def click_framework_order_1(self):
        self.link.click()

    def click_framework_order(self, framework_order_no: str):
        link = self.page.locator(f"//a[contains(text(),'{framework_order_no}')]")
        link.wait_for(state="visible", timeout=5000)
        link.click()
        print(f"Opened Marketplace framework order details: {framework_order_no}")
