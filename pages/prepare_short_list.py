import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class PrepareShortList(BasicActions):

    def __init__(self, page):
        super().__init__(page)

    def click_details_of_item(self, requisition_no: str, item_title: str):
    # Construct a combined row locator using both texts
        row = self.page.locator(f'table#jqGridShortListTable tr:has(td:has-text("{requisition_no}")):has(td:has-text("{item_title}"))').first

    # Get the status text from the located row
        status_locator = row.locator('td[aria-describedby="jqGridShortListTable_status"]')
        status = status_locator.inner_text().strip()

        print(f"Status found: '{status}' for Requisition No: {requisition_no} and Item: {item_title}")

        if status.lower() == "pending":
            print("Clicking Details button since status is Pending.")
            row.locator('button:has-text("Details")').click()
            self.page.wait_for_timeout(5000)
        else:
            print("Status is not Pending. Skipping click.")
            self.page.wait_for_timeout(2000)