import re
from utils.basic_actions import BasicActions
from datetime import datetime
import time


class FinancialEvaluation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.select_all_button = page.locator('#select-button')
        self.bulk_accept_button = page.locator('#accept')
        self.confirm_yes = page.locator('div.jconfirm-buttons button.btn-green', has_text='Yes')
        self.nominate_button = page.locator('#award')


    def click_select_all_recommendations(self):
        print("Clicking the 'Select All' button...")
        # Wait until the button is visible
        self.select_all_button.wait_for(state='visible', timeout=5000)

        # Scroll into view and click
        self.select_all_button.scroll_into_view_if_needed()
        self.select_all_button.click()
        self.browser_wait_for()
        print("'Select All' button clicked.")


    def click_bulk_accept(self):
        print("Clicking the 'Bulk Accept' button...")
        # Wait until the button is visible and enabled
        self.bulk_accept_button.wait_for(state='visible', timeout=5000)

        # Scroll into view and click
        self.bulk_accept_button.scroll_into_view_if_needed()
        self.bulk_accept_button.click()

        self.browser_wait_for()
        print("'Bulk Accept' button clicked.")
        

    def selecting_confirm_yes(self):
        print("Waiting for confirmation dialog...")
        # Wait for the button to appear
        self.confirm_yes.wait_for(state='visible', timeout=5000)
        # Click the 'Yes' button
        self.confirm_yes.click()
        self.browser_wait_for()
        print("Clicked 'Yes' on confirmation dialog.")


    def click_nominate_for_award(self):
        print("Clicking 'Nominate for Award' button...")
        # Wait for button to be visible and enabled
        self.nominate_button.wait_for(state='visible', timeout=5000)
        # Scroll into view and click
        self.nominate_button.scroll_into_view_if_needed()
        self.nominate_button.click()
        self.browser_wait_for()
        print("'Nominate for Award' button clicked.")