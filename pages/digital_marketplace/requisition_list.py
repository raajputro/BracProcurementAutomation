import re

from utils.basic_actionsdm import BasicActionsDM


class RequisitionList(BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)
        self.requisition_list = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition List"]')

        self.requisition_search_box = page.locator("#requisitionNoForPrint")
        self.requisition_search_btn = page.get_by_role("button", name=re.compile("Find", re.IGNORECASE))
        self.requisition_status = page.locator("//table[@id='requisitionGrid']/tbody/tr[2]/child::td[7]")
        self.logout_btn = page.locator("//a[@id='btn_login']")
        # self.click_requisition_no = page.locator('a[style="text-decoration: underline;"][onclick^="showDetails("]')
        self.requisition_no = page.locator("table tr a")

    def search_requisition(self, requisition_number):
        self.input_in_element(self.requisition_search_box, requisition_number)
        self.click_on_btn(self.requisition_search_btn)
        self.wait_for_timeout(5000)
        # status_value = self.requisition_status.text_content()
        # approver_id = status_value.split('[')[-1].split(']')[0]
        # print("Approver ID: " + approver_id)
        # # self.logout_btn.click()
        # # self.page.get_by_text(" Logout", exact=True).click()
        # return approver_id

    def find_approver_id(self) -> str:
        status_value = self.requisition_status.text_content()
        approver_id = status_value.split('[')[-1].split(']')[0]
        print("Approver ID: " + approver_id)
        return approver_id

    def find_requisition_status(self) -> str:
        status_value = self.requisition_status.text_content()
        print("Requisition Status: " + status_value)
        return status_value

    def goto_requisition_details_information(self):
        self.requisition_no.nth(0).click()
