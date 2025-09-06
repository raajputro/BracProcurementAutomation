import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class FinancialEvaluation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.select_all_button = page.locator('#select-button')
        self.bulk_accept_button = page.locator('#accept')
        self.confirm_yes = page.locator('div.jconfirm-buttons button.btn-green', has_text='Yes')

    def click_select_all_recommendations(self):
        """
        Clicks the 'Select All' button to select all tender.
        """
        print("Clicking the 'Select All' button...")
        # Wait until the button is visible
        self.select_all_button.wait_for(state='visible', timeout=5000)

        # Scroll into view and click
        self.select_all_button.scroll_into_view_if_needed()
        self.select_all_button.click()

        self.page.wait_for_timeout(1000)
        print("'Select All' button clicked.")

    def click_bulk_accept(self):
        """
        Clicks the 'Bulk Accept' button on the page.
        """
        print("Clicking the 'Bulk Accept' button...")
        # Wait until the button is visible and enabled
        self.bulk_accept_button.wait_for(state='visible', timeout=5000)

        # Scroll into view and click
        self.bulk_accept_button.scroll_into_view_if_needed()
        self.bulk_accept_button.click()

        self.page.wait_for_timeout(1000)
        print("'Bulk Accept' button clicked.")

    def selecting_confirm_yes(self):
        """
        Clicks the 'Yes' button in a confirmation dialog.
        """
        print("Waiting for confirmation dialog...")
        # Wait for the button to appear
        self.confirm_yes.wait_for(state='visible', timeout=5000)

        # Click the 'Yes' button
        self.confirm_yes.click()

        self.page.wait_for_timeout(5000)
        print("Clicked 'Yes' on confirmation dialog.")