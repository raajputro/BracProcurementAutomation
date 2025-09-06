import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class TenderEvaluationList(BasicActions):

    def __init__(self, page):
        super().__init__(page)

    def go_to_tender_evaluation_list(self):
        print("Navigating to Tender Evaluation List...")

        # Step 1: Click on the 'Tender Evaluation' main menu
        tender_eval_main = self.page.locator("a.nav-link.evaluate-link:has-text('Tender Evaluation')")
        tender_eval_main.wait_for(state="visible", timeout=10000)
        tender_eval_main.click()
        self.page.wait_for_timeout(1000)  # Let the sub-menu open

        # Step 2: Click on the sub-menu item 'Tender Evaluation List'
        eval_list_link = self.page.locator("a.autoload:has-text('Tender Evaluation List')")
        eval_list_link.wait_for(state="visible", timeout=10000)
        eval_list_link.click()
        self.page.wait_for_timeout(3000)  # Wait for the page to load

        print("Navigated to Tender Evaluation List.")