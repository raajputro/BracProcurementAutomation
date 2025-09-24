import re
from utils.basic_actions import BasicActions
from pages.erp_procurement.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class RequisitionAcceptList(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.req_no = page.get_by_role("textbox", name="Requisition No.")
        self.find = page.get_by_role("button", name="Find")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.accept = page.get_by_role("button", name=re.compile("Accept", re.IGNORECASE))
        self.status_dropdown = page.locator("select#acceptStatus")
        self.confirmation_message_accept = page.locator('span.ui-button-text', has_text="Accept")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')


    def select_status(self, status_text: str):
        self.status_dropdown.select_option(label=status_text)
        self.page.wait_for_timeout(1000)
        
    def search_requisition(self, requisition_number):
        self.req_no.type(requisition_number)
        self.page.wait_for_timeout(2000)
        s_result = self.page.locator('a.ui-corner-all:has-text("' + requisition_number + '")')
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()
        self.page.wait_for_timeout(2000)


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
        toast_msg_text = self.toast_msg.text_content()
        self.print_important_toast(toast_msg_text)
        self.page.wait_for_timeout(5000)
        
