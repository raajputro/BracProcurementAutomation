import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class TenderList(BasicActions):

    def __init__(self, page):
        super().__init__(page)

        self.tender_process = page.locator('ul#mySidebar a.nav-link:has-text("Tender Process")')
        self.tender_list = page.locator('ul#mySidebar a[href="#tender/list"]')
        self.tender_search = page.locator('#tenderTitleSearch')

    

    def go_to_tender_list(self):
    # Click on "Tender Process"
        self.tender_process.click()
        self.page.wait_for_timeout(1000)
        # Click on "Tender List"
        self.tender_list.click()
        self.page.wait_for_timeout(2000)

        print("Navigated to Tender List.")

    def search_tender(self, tender_no):
        # Enter the tender title in the search box
        self.tender_search.fill(tender_no)
        self.page.wait_for_timeout(1000)
        # Press Enter to initiate the search
        self.tender_search.press("Enter")
        self.page.wait_for_timeout(2000)
        print(f"Searched for tender with title: {tender_no}")

    def navigate_to_tender_details_page(self, tender_number: str):
        tender_no = self.page.locator(f'table#jqGridTender a:has-text("{tender_number}")')
    # Ensure it's visible and clickable
        tender_no.wait_for(state="visible", timeout=5000)
        tender_no.scroll_into_view_if_needed()
        tender_no.click()
        self.page.wait_for_timeout(2000)

        print(f"Clicked on tender number: {tender_number}")
    