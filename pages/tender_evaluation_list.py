import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class TenderEvaluationList(BasicActions):

    def __init__(self, page):
        super().__init__(page)

        self.tender_evaluation = page.locator("a.nav-link.evaluate-link:has-text('Tender Evaluation')")
        self.tender_evaluation_list = page.locator("a.autoload:has-text('Tender Evaluation List')")
        self.tender_search = page.locator('#tenderTitleSearch')


    def go_to_tender_evaluation_list(self):
        print("Navigating to Tender Evaluation List...")

        # Step 1: Click on the 'Tender Evaluation' main menu
        self.tender_evaluation.wait_for(state="visible", timeout=1000)
        self.tender_evaluation.click()
        self.page.wait_for_timeout(1000)  # Let the sub-menu open

        # Step 2: Click on the sub-menu item 'Tender Evaluation List'
        self.tender_evaluation_list.wait_for(state="visible", timeout=1000)
        self.tender_evaluation_list.click()
        self.page.wait_for_timeout(3000)  # Wait for the page to load

        print("Navigated to Tender Evaluation List.")

    def search_tender(self, tender_no):
        
        # Enter the tender title in the search box
        self.tender_search.fill(tender_no)
        self.page.wait_for_timeout(1000)

        # Press Enter to initiate the search
        self.tender_search.press("Enter")
        self.page.wait_for_timeout(2000)
        print(f"Searched for tender with title: {tender_no}")

    def click_tender_number(self, tender_number: str):
        """
        Clicks on the tender number link in the tender evaluation list.
        """
        print(f"Clicking tender number: {tender_number}")

        # Locate the anchor element with the given tender number
        tender_no = self.page.locator(f'table#jqGridTender a:has-text("{tender_number}")')

        # Wait until it's visible
        tender_no.wait_for(state="visible", timeout=10000)

        # Scroll into view and click
        tender_no.scroll_into_view_if_needed()
        tender_no.click()

        # Optional wait to allow page transition or content load
        self.page.wait_for_timeout(2000)

        print(f"Clicked tender number: {tender_number}")