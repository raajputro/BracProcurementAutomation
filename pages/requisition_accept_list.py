import re
from utils.basic_actions import BasicActions
from playwright.sync_api import expect
from pages.procurement_home_page import ProcurementHomePage

class RequisitionAcceptList(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.req_no = page.get_by_role("textbox", name="Requisition No.")
        self.find = page.get_by_role("button", name="Find")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.accept = page.get_by_role("button", name=re.compile("Accept", re.IGNORECASE))
        self.confirmation_message_accept = page.locator('span.ui-button-text', has_text="Accept")
        
    def search_requisition(self, requisition_number):
        self.input_in_element(self.req_no, requisition_number + " ") # adding a trailing space to ensure the input is recognized
        self.page.wait_for_timeout(1000)
        self.req_no.click()  # focus the input field
        self.page.keyboard.press("End")  # move cursor to the end
        self.page.keyboard.press("Backspace")  # delete trailing space

        # Dynamic locator for suggestion dropdown
        #suggestion = self.page.locator(f'//ul[contains(@class, "ui-autocomplete")]//a[contains(@class, "ui-corner-all") and contains(text(), "{requisition_number}")]')
        suggestest_requisition_number = self.page.locator('a.ui-corner-all:has-text("' + requisition_number + '")')
        # Wait and click
        suggestest_requisition_number.wait_for(state="visible", timeout=5000)
        suggestest_requisition_number.hover()
        suggestest_requisition_number.click()
        self.page.wait_for_timeout(2000)
        # self.find.click()

    def select_all_requisitions(self):
        self.select_all.click()
        self.page.wait_for_timeout(2000)

    def accept_requisition(self):
        self.accept.click()
        self.page.wait_for_timeout(2000)

    def confirm_acceptance(self):
        self.confirmation_message_accept.hover()
        self.page.wait_for_timeout(1000)
        self.confirmation_message_accept.click()
        self.page.wait_for_timeout(5000)
        