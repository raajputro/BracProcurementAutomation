import re
from utils.basic_actionsdm import BasicActionsDM


class BillList(BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)
        self.bill_payable_search_box = page.get_by_role('textbox', name='Search Vendor Bill Payable')
        self.bill_search_btn = page.get_by_role("button", name=re.compile("Find", re.IGNORECASE))
        self.bill_payable = page.locator('//div[text()="Bill Payable"]')
        self.create_vendor_bill_payable = page.locator(
            '//div[text()="Bill Payable"]//following-sibling::ul//child::span[text()="Create Vendor Bill Payable"]')
        self.vendor_billing_list = page.locator(
            '//div[text()="Bill Payable"]//following-sibling::ul//child::span[text()="Vendor Billing List"]')
        # self.bill_status = page.locator("//table[@id='jqgrid-grid-thirdPartyBillPayableList']/tbody/tr[2]/td[14]")
        # self.bill_status2 = page.locator("//table[@id='jqgrid-grid-thirdPartyBillPayableList']").get_by_role("link", name=bill_num, exact=True)

    def go_to_billing_list(self):
        self.bill_payable.click()
        self.vendor_billing_list.click()
        self.wait_for_timeout(3000)

    def search_bill(self, bill_number):
        print("Searching for Bill Number:", bill_number)
        self.bill_payable_search_box.fill(bill_number)
        self.page.keyboard.press("Enter")
        # self.wait_for_timeout(3000)
        # self.click_on_btn(self.bill_search_btn)
        self.wait_for_timeout(5000)

    def find_approver_id(self, bill_num) -> str:
        bill_status = self.page.locator(
            f"//table[@id='jqgrid-grid-thirdPartyBillPayableList']/tbody/tr/td[2]/a[text()='{bill_num}']//parent::td//parent::tr/td[14]")
        self.wait_to_load_element(bill_status)
        status_value = bill_status.text_content()
        print("Status Value: " + status_value)
        approver_id = status_value.split('[')[-1].split(']')[0]
        print("Approver ID: " + approver_id)
        return approver_id

    def find_bill_status(self, bill_num) -> str:
        bill_status = self.page.locator(
            f"//table[@id='jqgrid-grid-thirdPartyBillPayableList']/tbody/tr/td[2]/a[text()='{bill_num}']//parent::td//parent::tr/td[14]")
        self.wait_to_load_element(bill_status)
        status_value = bill_status.text_content()
        print("Bill Status: " + status_value)
        return status_value

    def click_on_bill_num(self, bill_number):
        # self.page.locator("//a[contains(text(),'"+bill_number+"')]").click()
        self.page.locator(
            f"//table[@id='jqgrid-grid-thirdPartyBillPayableList']/tbody/tr/td[2]/a[text()='{bill_number}']").click()
        self.page.wait_for_timeout(2000)
