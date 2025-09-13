import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from datetime import datetime
import time


class CreateWorkOrder(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.vendor_input = page.locator("#thirdPartyIdDiv_input")
        self.vendor_dropdown = page.locator("#thirdPartyIdDiv_ctr")
        self.add_to_grid = page.get_by_role("button", name="Add to Grid")
        self.same_schedule = page.get_by_role("checkbox", name="Same schedule")
        self.est_delivery_date_with_text = page.locator('input#defaultDeliveryDate[placeholder="DD-MM-YYYY"]')
        self.delivery_location_dropdown = page.locator("#defaultDeliveryStoreId")
        self.delivery_location_box = page.get_by_placeholder("Note: 1. Address 2. Contact Person Name 3. Cell Number 4. Delivery Time")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')
        self.save_next = page.get_by_role("button", name="Save & Next")
        self.purchase_order_template_dropdown = page.locator('#purchaseLetterBodyTemplateId')
        self.payment_template_dropdown = page.locator('#purchaseLetterPaymentTemplateId')
        self.terms_template_dropdown = page.locator('#purchaseLetterTermTemplateId')
        self.work_order_approver = page.locator('#signatoryMemberDiv_input')
        self.submit_button = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.locator('span.ui-button-text', has_text="Submit")
        self.work_order_no_field = page.locator("#refNo")


    def select_vendor(self, vendor_name: str):
        print("Typing vendor name...")

        self.wait_for_timeout(2000)
        self.vendor_input.type(vendor_name)
        self.page.wait_for_timeout(2000)
        # self.vendor_input.click()  # Focus the input
        # self.page.keyboard.press("End")      # Move cursor to end
        # self.page.keyboard.insert_text(" ")
        # self.page.keyboard.press("Backspace")  # Trigger input event
        self.page.wait_for_timeout(2000)

        # Wait for the suggestion dropdown to appear
        self.vendor_dropdown.wait_for(state="visible", timeout=5000)

        # Select the matching 1st suggestion row (based on vendor_name)
        # suggestion = self.page.locator(f"//div[@class='row ffb-sel']//div[contains(text(), '{vendor_name}')]")
        suggestion =  self.page.locator("//div[@class='row ffb-sel']").first
        suggestion.click()

        print(f"Selected vendor: {vendor_name}")

    def select_payment_mode(self, mode: str):
        print(f"Selecting payment mode: {mode}")

        mode = mode.strip().lower()

        # Dynamic mapping of mode to element ID
        payment_mode_ids = {
            "cash": "isCashPayment",
            "bank": "isBankPayment",
            "online": "isOnlinePayment"
        }

        if mode not in payment_mode_ids:
            raise ValueError(f"Unsupported payment mode: {mode}")

        # Create the locator dynamically
        checkbox_id = payment_mode_ids[mode]
        checkbox = self.page.locator(f'input[type="checkbox"]#{checkbox_id}')

        # Interact with checkbox
        checkbox.wait_for(state="visible", timeout=5000)
        checkbox.scroll_into_view_if_needed()
        checkbox.check()

        print(f"Selected payment mode: {mode.capitalize()}")

    def select_first_checkbox_by_tender(self, tender_no: str):
        print(f"Looking for tender: {tender_no}")

        # XPath to locate the row by Tender No (find the first one)
        row = self.page.locator(f"//table[@id='workOrderDetailGrid']//tr[td//a[contains(text(), '{tender_no}')]]")

        # Locate all checkboxes in the row (using nth-child(2) to target the second column with checkboxes)
        checkboxes = row.locator("td:nth-child(2) input[type='checkbox']")

        # Click the first checkbox
        checkboxes.first.click()

        print(f"First checkbox clicked for Tender: {tender_no}")

    def select_first_checkbox_by_noal_number(self, noal_no: str):
        print(f"Looking for noal number: {noal_no}")

        # XPath to locate the first row by Noal No
        row = self.page.locator(f"//table[@id='workOrderDetailGrid']//tr[td//a[contains(text(), '{noal_no}')]][1]")

        # Ensure the row is found and visible
        row.wait_for(state="visible", timeout=5000)

        # Locate the first checkbox in the row (2nd column)
        checkbox_locator = row.locator("td:nth-child(2) input[type='checkbox']")

        checkbox_locator.scroll_into_view_if_needed()
        checkbox_locator.check()

        print(f"First checkbox clicked for Noal number: {noal_no}")

    def select_first_checkbox_by_noal_and_tender(self, noal_no: str, tender_no: str):
        print(f"Looking for NOAL: {noal_no}, Tender: {tender_no}")

        # XPath: find the first row that has both NOAL and Tender number
        row = self.page.locator(f"//table[@id='workOrderDetailGrid']//tr[td//a[contains(text(), '{noal_no}')] "f"and td//a[contains(text(), '{tender_no}')]][1]")

        # Ensure the row is found and visible
        row.wait_for(state="visible", timeout=5000)

        # Checkbox is in 2nd column
        checkbox_locator = row.locator("td:nth-child(2) input[type='checkbox']")
        checkbox_locator.wait_for(state="visible", timeout=5000)
        checkbox_locator.scroll_into_view_if_needed()
        checkbox_locator.check()
        self.page.wait_for_timeout(1000)

        print(f"First checkbox clicked for NOAL: {noal_no}, Tender: {tender_no}")

    def add_item_to_grid(self):
        self.add_to_grid.click()
        self.wait_for_timeout(5000)

    def same_delivery_schedule(self):
        self.same_schedule.scroll_into_view_if_needed()
        self.same_schedule.check()
        self.wait_for_timeout(1000)

    def estimated_delivery_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.est_delivery_date_with_text.scroll_into_view_if_needed()
        self.est_delivery_date_with_text.fill(date)
        self.wait_for_timeout(1000)
        # Validate the date format


    def delivery_location_dropdown_select(self, delivery_location: str = "Central Store"):
        # Select the delivery location from the dropdown
        # self.delivery_location_dropdown.scroll_into_view_if_needed()
        # self.delivery_location_dropdown.click()
        self.select_from_list_by_value(self.delivery_location_dropdown, delivery_location)

    
    def delivery_location(self, location: str):
        # Fill the delivery location input field
        self.delivery_location_box.scroll_into_view_if_needed()
        self.delivery_location_box.fill(location)
        self.wait_for_timeout(1000)

    def go_to_save_next(self):
        # self.wait_for_timeout(10000)
        try:
            # self.page.wait_for_selector(self.save_next, timeout=5000)
            self.save_next.wait_for(state="visible", timeout=3000)
        # self.save_next.scroll_into_view_if_needed()
            self.save_next.click()
        except:
            print("Save & Next button not found or not clickable.")

        # print("Waiting for Save & Next button to be visible...")
        # print(self.save_next.inner_text())
        self.toast_msg.wait_for(state="visible", timeout=10000)
        toast_msg = self.toast_msg.text_content()
        # print(toast_msg)
        self.print_important_toast(toast_msg)
    
        self.wait_for_timeout(5000)

    def select_purchase_order_template(self, template_name: str):
        self.purchase_order_template_dropdown.scroll_into_view_if_needed()
        self.purchase_order_template_dropdown.wait_for(state='visible', timeout=5000)
        # Select by visible text (label)
        self.purchase_order_template_dropdown.select_option(label=template_name)

        self.wait_for_timeout(1000)  # optional wait

    def select_payment_template(self, template_name: str):
        self.payment_template_dropdown.scroll_into_view_if_needed()
        self.payment_template_dropdown.wait_for(state='visible', timeout=5000)
        # Select option by visible text (label)
        self.payment_template_dropdown.select_option(label=template_name)

        self.page.wait_for_timeout(5000)  # Optional delay to allow any UI updates

    def select_terms_template(self, template_name: str):
        self.terms_template_dropdown.scroll_into_view_if_needed()
        self.terms_template_dropdown.wait_for(state='visible', timeout=5000)
        self.terms_template_dropdown.select_option(label=template_name)
        self.page.wait_for_timeout(5000)

    # def work_order_approver_selecting(self, approver: str):
    #     self.work_order_approver.wait_for(state="visible", timeout=3000)
    #     self.work_order_approver.scroll_into_view_if_needed()
    #     self.work_order_approver.fill(approver)
    #     self.page.keyboard.press("End")
    #     self.page.keyboard.type(" ")
    #     self.page.keyboard.press("Backspace")
    #     work_order_approver_selection = self.page.get_by_text(approver)
    #     work_order_approver_selection.wait_for(state="visible", timeout=5000)
    #     work_order_approver_selection.hover()
    #     work_order_approver_selection.click()
    #     self.wait_for_timeout(3000)
    def work_order_approver_selecting(self, approver: str):
        # Ensure input is ready
        self.work_order_approver.wait_for(state="visible", timeout=3000)
        self.work_order_approver.scroll_into_view_if_needed()
        self.work_order_approver.click()

        # Type the approver name (triggers suggestions)
        self.work_order_approver.type(approver)

        # Wait for and select the first suggestion
        suggestion = self.page.locator("#signatoryMemberDiv_ctr .content > div").first
        suggestion.wait_for(state="visible", timeout=5000)
        suggestion.click()

        # Optional: wait to allow UI to update
        self.page.wait_for_timeout(1000)

    def submit_work_order(self):
        self.submit_button.wait_for(state="visible", timeout=5000)
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()
        self.toast_msg.wait_for(state="visible", timeout=5000)
        toast_msg = self.toast_msg.text_content()
        self.print_important_toast(toast_msg)
        self.wait_for_timeout(5000)

    def get_work_order_number(self) -> str:
        work_order_value = self.work_order_no_field.input_value()
        print("Generated Purchase Order Number:", work_order_value)
        return work_order_value