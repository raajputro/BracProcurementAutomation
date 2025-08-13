import re
from utils.basic_actions import BasicActions

class BillList(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.bill_payable_search_box = page.get_by_role('textbox', name='Search Vendor Bill Payable' )
        # self.bill_search_btn = page.get_by_role("button", name=re.compile("Find", re.IGNORECASE))
        self.bill_status = page.locator("//table[@id='jqgrid-grid-thirdPartyBillPayableList']/tbody/tr[1]/td[14]")


    def search_bill(self, bill_number):
        print("Searching for Bill Number:", bill_number)
        self.bill_payable_search_box.fill(bill_number)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(3000)


    def find_approver_id(self) -> str:
        status_value = self.bill_status.text_content()
        approver_id = status_value.split('[')[-1].split(']')[0]
        print("Approver ID: " + approver_id)
        return approver_id

    def find_requisition_status(self) -> str:
        status_value = self.bill_status.text_content()
        print("Requisition Status: " + status_value)
        return status_value

    def click_on_bill_num(self, bill_number):
        self.page.locator("//a[contains(text(),'"+bill_number+"')]").click()
        self.page.wait_for_timeout(2000)
