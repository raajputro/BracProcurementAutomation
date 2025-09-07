import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class CreateNoal(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.tender_finalize = page.locator('a:has-text("Tender Finalize")')
        self.create_noal = self.page.get_by_role("link", name="Create NOAL", exact=True)
        self.tender_search = page.locator('#tenderTitle')
        self.submit_button = page.locator('#approve')
        self.yes_button = page.locator('.ui-dialog-buttonset >> text=Yes')

    def click_create_noal(self):
        # Step 1: Click on "Tender Finalize"
        self.tender_finalize.click()
        self.page.wait_for_timeout(2000)  # wait for the submenu to appear or load

        # Step 2: Click on "Create NOAL"
        self.create_noal.scroll_into_view_if_needed()
        self.create_noal.click()
        self.page.wait_for_timeout(2000)  # wait for the NOAL section/page to load

    def search_tender(self, tender_title: str):
        """
        Enters the tender title in the Tender Search input to trigger the search.
        """
        print(f"Searching for tender: {tender_title}")
        # Wait for the search field to be visible
        self.tender_search.wait_for(state='visible', timeout=5000)

        # Fill in the tender title
        self.tender_search.fill(tender_title)
        self.tender_search.press("Enter")

        # Optionally wait for the grid to load results
        self.page.wait_for_timeout(2000)  # wait for search results to load

    def select_items_by_tender_supplier_payment_type(self, tender_no: str, supplier_name: str, payment_type: str):
        """
        Selects rows from the jqGrid table that match the given Tender No and Supplier Name,
        then checks the main checkbox and the specified payment type checkbox (e.g. Cash, Bank, Online).
        """
        print(f"Selecting items for Tender No: {tender_no}, Supplier: {supplier_name}, Payment Type: {payment_type}")

        # Normalize payment type to lowercase (e.g. 'cash', 'bank', 'online')
        payment_type = payment_type.strip().lower()
        if payment_type not in ['cash', 'bank', 'online']:
            print(f"Invalid payment type: {payment_type}. Must be one of: Cash, Bank, Online.")
            return

        rows = self.page.locator('table#jqGrid tr.jqgrow')
        row_count = rows.count()
        matched_rows = []

        for i in range(row_count):
            row = rows.nth(i)

            tender_cell = row.locator('td[aria-describedby="jqGrid_id_no"]')
            supplier_cell = row.locator('td[aria-describedby="jqGrid_supplier_name"]')

            if tender_cell.count() == 0 or supplier_cell.count() == 0:
                continue

            current_tender = tender_cell.get_attribute('title')
            current_supplier = supplier_cell.get_attribute('title')

            if current_tender == tender_no and current_supplier == supplier_name:
                print(f"Match found in row {i+1}")

                # Main checkbox
                checkbox = row.locator('input[type="checkbox"].check')
                checkbox_value = checkbox.get_attribute("value")
                if checkbox.is_visible():
                    checkbox.check()

                # Specific payment checkbox
                payment_checkbox = row.locator(f'input.paymentType_{checkbox_value}#' + f'{payment_type}_{checkbox_value}')
                if payment_checkbox.is_visible():
                    payment_checkbox.check()
                    print(f"Checked {payment_type.capitalize()} checkbox in row {i+1}")
                else:
                    print(f"Payment type checkbox '{payment_type}' not found or not visible in row {i+1}")

                matched_rows.append(i + 1)

        if not matched_rows:
            print(f"No rows matched for Tender: {tender_no}, Supplier: {supplier_name}")
        else:
            print(f"Process completed. Rows selected: {matched_rows}")


    def click_submit_button(self):

        print("Clicking the Submit (Approve) button...")

        # Wait for it to be visible and enabled
        self.submit_button.wait_for(state='visible', timeout=3000)
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()
        self.page.wait_for_timeout(2000)  # Optional: wait for any post-click actions to complete
        print("Submit button clicked.")

    def confirm_submission(self):
        print("Looking for confirmation dialog...")

        # Wait until it's visible and click it
        self.yes_button.wait_for(state='visible', timeout=10000)
        self.yes_button.scroll_into_view_if_needed()
        self.yes_button.click()

        self.page.wait_for_timeout(2000)  # Optional wait to allow the action to complete
        print("Clicked 'Yes' on confirmation dialog.")
