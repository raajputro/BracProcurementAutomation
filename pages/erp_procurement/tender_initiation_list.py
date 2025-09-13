import re
from typing import Self
from utils.basic_actions import BasicActions
from pages.erp_procurement.create_tender_initiation import CreateTenderInitiation


class TenderInitiationList(CreateTenderInitiation):
    def __init__(self, page):
        super().__init__(page)
        self.search_box = page.get_by_placeholder("Search Reference No")
        self.approve= page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
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