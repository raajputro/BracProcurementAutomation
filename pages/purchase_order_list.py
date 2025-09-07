import re
from utils.basic_actions import BasicActions

class PurchaseOrderList(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.purchase_order_search_box = page.get_by_role('textbox', name='Search Purchase Order No' )
        # self.work_order_status = page.locator("//table[@id='workOrderGrid']/tbody/tr[2]/td[13]")
        # self.work_order_status = page.locator("//table[@id='workOrderGrid']//td[@aria-describedby='workOrderGrid_status']")
        self.work_order_status = page.locator("//table[@id='workOrderGrid']//td[@aria-describedby='workOrderGrid_status']")

    

    def search_work_order(self, work_order_num):
        print("Searching for PO Number:", work_order_num)
        self.purchase_order_search_box.fill(work_order_num)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(5000)
    

    def find_work_order_status(self) -> str:
        status_value = self.work_order_status.text_content()
        print("Work Order Status: " + status_value)
        return status_value

    def click_on_work_order_num(self, po_number):
        self.page.locator("//a[contains(text(),'"+po_number+"')]").click()
        self.page.wait_for_timeout(2000)
