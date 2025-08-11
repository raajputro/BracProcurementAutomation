import re
from utils.basic_actions import BasicActions

class RequisitionList(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.requisition_search_box = page.get_by_role("input", name=re.compile("requisitionNoForPrint", re.IGNORECASE)) # page.locator("#requisitionNoForPrint")
        self.requisition_search_btn = page.get_by_role("button", name=re.compile("Find", re.IGNORECASE))
        self.requisition_status = page.locator("//table[@id='requisitionGrid']/tbody/tr[2]/child::td[7]")
        self.logout_btn = page.locator("//a[@id='btn_login']")


    def search_requisition(self, requisition_number):
        print("Searching for Requisition Number:", requisition_number)
        #self.input_in_element(self.requisition_search_box, requisition_number)
        self.requisition_search_box.fill(requisition_number)
        self.click_on_btn(self.requisition_search_btn)
        self.wait_for_timeout(5000)


    def find_approver_id(self) -> str:
        status_value = self.requisition_status.text_content()
        approver_id = status_value.split('[')[-1].split(']')[0]
        print("Approver ID: " + approver_id)
        return approver_id

    def find_requisition_status(self) -> str:
        status_value = self.requisition_status.text_content()
        print("Requisition Status: " + status_value)
        return status_value
