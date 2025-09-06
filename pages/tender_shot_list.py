import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class TenderShortList(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.tender_evaluation_menu = page.locator("a.nav-link.evaluate-link:has-text('Tender Evaluation')")
        self.tender_short_list_link = page.locator("a.autoload:has-text('Tender Short List')")
        self.tender_search = page.locator('#tenderTitleSearch')

    def go_to_tender_short_list(self):
        print("Navigating to Tender Short List...")
    
        self.tender_evaluation_menu.wait_for(state="visible", timeout=2000)
        self.tender_evaluation_menu.click()
        self.page.wait_for_timeout(1000)  # Allow sub-menu to expand

        # Step 2: Click on 'Tender Short List' sub-menu item
        self.tender_short_list_link.wait_for(state="visible", timeout=2000)
        self.tender_short_list_link.click()
        self.page.wait_for_timeout(3000)  # Allow page to load

        print("Navigated to Tender Short List.")

    def search_tender(self, tender_no):
        
        # Enter the tender title in the search box
        self.tender_search.fill(tender_no)
        self.page.wait_for_timeout(1000)

        # Press Enter to initiate the search
        self.tender_search.press("Enter")
        self.page.wait_for_timeout(2000)
        print(f"Searched for tender with title: {tender_no}")

    def click_tender_number(self, tender_number: str):
        print(f"Clicking tender number: {tender_number}")
    
        # Locate the anchor tag that contains the tender number
        tender_no = self.page.locator(f'table#jqGridTender a:has-text("{tender_number}")')
    
        # Ensure it is visible before interacting
        tender_no.wait_for(state="visible", timeout=10000)
    
        # Scroll and click
        tender_no.scroll_into_view_if_needed()
        tender_no.click()
    
        self.page.wait_for_timeout(2000)  # Optional delay to allow next page to load
        print(f"Clicked tender number: {tender_number}")