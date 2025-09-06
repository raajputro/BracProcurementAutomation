import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class PrepareShortList(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.shortlist_button = page.locator("button:has-text('Short List')")
        self.recommendation_box = page.locator('#recommendation')
        self.forward_button = page.locator('button#saveComments')

    def click_details_of_item(self, requisition_no: str, item_title: str):
    # Construct a combined row locator using both texts
        row = self.page.locator(f'table#jqGridShortListTable tr:has(td:has-text("{requisition_no}")):has(td:has-text("{item_title}"))').first

    # Get the status text from the located row
        status_locator = row.locator('td[aria-describedby="jqGridShortListTable_status"]')
        status = status_locator.inner_text().strip()

        print(f"Status found: '{status}' for Requisition No: {requisition_no} and Item: {item_title}")
        click_details = row.locator('button:has-text("Details")')
        click_details.click()
        self.page.wait_for_timeout(5000)

        # if status.lower() == "pending":
        #     print("Clicking Details button since status is Pending.")
        #     row.locator('button:has-text("Details")').click()
        #     self.page.wait_for_timeout(5000)
        # else:
        #     print("Status is not Pending. Skipping click.")
        #     self.page.wait_for_timeout(2000)


    def fill_supplier_details(self, supplier_name, is_responsive,comment_text="", upload_file_path=None, proposed_qty=None, advance_amount=None):
        """
        Fill details for a given supplier based on responsiveness.

        :param supplier_name: Name of the supplier (e.g. "Mentors")
        :param is_responsive: Boolean, True for Responsive, False for Non-Responsive
        :param proposed_qty: Quantity to fill if Responsive
        :param advance_amount: Advance amount to fill if Responsive
        :param comment_text: Comment to write in textarea
        :param upload_file_path: Path to document file to upload
        """

        # Find supplier ID by matching hidden input value
        supplier_name_locator = self.page.locator('input[id^="supName_"]')
        count = supplier_name_locator.count()
        supplier_id = None
        for i in range(count):
            val = supplier_name_locator.nth(i).input_value()
            if val.strip() == supplier_name:
                supplier_id = supplier_name_locator.nth(i).get_attribute('id').split('_')[1]
                break
        if not supplier_id:
            raise Exception(f"Supplier name '{supplier_name}' not found!")

        # 1. Select Responsive / Non-Responsive radio button
        select_responsiveness = self.page.locator(f'#res_{supplier_id}' if is_responsive else f'#non_res_{supplier_id}')
        select_responsiveness.check()
        self.page.wait_for_timeout(5000)

        if is_responsive:
            # 2. Propose Vendor Selection checkbox and Proposed Quantity
            propose_vendor_selection_checkbox = self.page.locator(f'#checkSuggest_{supplier_id}')
            propose_vendor_selection_checkbox.check(force=True)
            self.page.wait_for_timeout(3000)
            if proposed_qty is not None:
                proposed_quantity = self.page.locator(f'#awardQty_{supplier_id}')
                proposed_quantity.fill(str(proposed_qty))

            # 3. Advance Amount (BDT)
            # advance_amount_checkbox = self.page.locator(f'#chkAdv_{supplier_id}')
            # advance_amount_checkbox.check(force=True)
            # self.page.wait_for_timeout(3000)
            # if advance_amount is not None:
            #     give_advance_amount = self.page.locator(f'#advAmount_{supplier_id}')
            #     give_advance_amount.fill(str(advance_amount))

        # 4. Upload document if path provided
        if upload_file_path:
            upload_document_file = self.page.locator(f'#document_{supplier_id} input[type="file"]')
            upload_document_file.set_input_files(upload_file_path)
            self.page.wait_for_timeout(1000)  # Allow time for upload

        # 5. Write comment
        comment_box = self.page.locator(f'#input_comment_{supplier_id}')
        comment_box.fill(comment_text)
        self.page.wait_for_timeout(5000)

    def click_shortlist_button(self):
        self.page.wait_for_timeout(2000)
        print("Clicking Shortlist button...")
        self.shortlist_button.click()
        print("Shortlist button clicked.")
        self.page.wait_for_timeout(2000)  # Optional: wait after click

    def fill_recommendation_field(self, note_text: str):
        """
        Fills the recommendation textarea only if it is enabled.
        Prints a message if the field is disabled.

        :param note_text: The text to fill in the recommendation field
        """
        # Check if the element is disabled
        is_disabled = self.recommendation_box.get_attribute('disabled') is not None

        if is_disabled:
            print("Recommendation field is disabled")
        else:
            self.recommendation_box.fill(note_text)
            print("Recommendation field filled successfully")
            self.page.wait_for_timeout(500)  # Optional wait

    def click_forward_to_committee(self):
        """
        Clicks the 'Forward to Committee' button.
        """
        self.forward_button.scroll_into_view_if_needed()
        print("Clicking 'Forward to Committee' button...")
        self.forward_button.click()
        self.page.wait_for_timeout(1000)  # Optional: wait for post-click UI changes