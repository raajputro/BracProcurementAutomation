import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class ETenderDetails(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.open_tender_button = page.locator('button#Open')
        self.yes_button = page.locator('button.btn-green:has-text("Yes")')

    def click_open_button(self):
        self.open_tender_button.wait_for(state="visible", timeout=20000)
        self.open_tender_button.scroll_into_view_if_needed()
        self.open_tender_button.click()
        self.page.wait_for_timeout(2000)
        print("Clicked the 'Open' button.")

    def wait_until(self, target_time_str: str):
        """Wait until the given time before proceeding."""
        target_time = datetime.strptime(target_time_str, "%d-%m-%Y %I:%M %p")
        now = datetime.now()
        seconds_to_wait = (target_time - now).total_seconds()

        if seconds_to_wait > 0:
            print(f" Waiting {int(seconds_to_wait)} seconds until: {target_time_str}")
            time.sleep(seconds_to_wait)
        else:
            print(f" Opening time {target_time_str} already passed or is now.")

    def confirm_open_tender(self):
        self.yes_button.wait_for(state="visible", timeout=40000)
        self.yes_button.scroll_into_view_if_needed()
        self.yes_button.click()
        self.page.wait_for_timeout(2000)
        print("Clicked 'Yes' on open tender confirmation dialog.")