import re
from typing import Self
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from pages.create_tender_initiation import CreateTenderInitiation


class TenderInitiationList(CreateTenderInitiation):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        cti = CreateTenderInitiation(page)
        # self.tender_value_2 = cti.tender_value
        self.search_box = page.get_by_placeholder("Search Reference No")
        #self.check_box = page.locator("input[type='checkbox'].isUnderMyAuthority")
        self.approve= page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
        # self.navigate_detail_direct_purchase = page.locator('a[style="text-decoration: underline;"]')
        self.confirmation_message_approve = page.locator('button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only', has_text="Approve")
        
    def search_tender(self, tender_number):
        self.search_box.scroll_into_view_if_needed()
        print("Searching for teder:", tender_number)
        self.search_box.fill(tender_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)
    
    def navigate_to_tender_detail_page(self, tender_number):
        # Click on the tender number link
        tender_details = self.page.locator("//a[contains(text(),'"+tender_number+"')]")
        tender_details.click()
        self.page.wait_for_timeout(5000)  
        
