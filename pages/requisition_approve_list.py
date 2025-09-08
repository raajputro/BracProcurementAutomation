# this is an object of samplePage to automate, which contains all elementsAdd commentMore actions
# and actions could be performed, like input, verify, etc.
import re
from asyncio import wait_for

from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class RequisitionApproveList(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.search_box = page.locator("//input[@name='keyword']")
        # self.search_box = page.get_by_role("input", name="keyword")
        self.search_box = page.get_by_placeholder("Search Requisition No")
        self.approve= page.locator("//input[@type='button' and @value='Approve']")
        self.confirmation_message_approve_locator = page.locator("//button/span[contains(text(),'Approve')]")
        # self.confirmation_message_approve = page.locator(
        #     'button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only', has_text="Approve")


    def search_requisition(self, requisition_number):
        print("Searching for Requisition Number:", requisition_number)
        self.page.wait_for_timeout(10000)
        self.input_in_element(self.search_box, requisition_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)

        
    def select_requisition(self, rq_number):
        # Select the checkbox for the requisition
        print("select requisition")
        try:
            # requisition_select_checkbox = self.page.locator("//td/a[contains(text(),'"+rq_number+"')]//parent::td//parent::tr//child::td/input[@type='checkbox']")
            requisition_select_checkbox = self.page.locator(f"//a[text()='{rq_number}']/parent::td/parent::tr/td[1]/input")
            self.wait_to_load_element(requisition_select_checkbox)
            requisition_select_checkbox.click()
            self.page.wait_for_timeout(3000)
        except Exception as e:
            print(e)


    def approve_requisition(self):
        self.approve.click()
        self.page.wait_for_timeout(5000)


    def confirmation_message_approve(self):
        # Click the confirmation message approve button
        self.wait_to_load_element(self.confirmation_message_approve_locator)
        self.confirmation_message_approve_locator.click()
        self.page.wait_for_timeout(2000)