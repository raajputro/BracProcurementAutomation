import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateTenderInitiation(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.search_box_for_list = page.get_by_placeholder("Please enter item name or REQ. No. to filter")
        self.select_all_checkbox = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all_checkbox = page.get_by_role("link", name="Unselect All", exact=True)
        self.select_method_dropdown = page.locator("#purchaseMethodIdDiv_input")
        self.select_method_dropdown_options_dpm = page.get_by_text("Direct Purchase-(DPM)")
        self.remarks= page.locator("textarea#remarks.height65[placeholder='Max size of remarks 250 characters']")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.locator('span.ui-button-text', has_text="Submit")
        self.save_button = page.get_by_role("button", name="Save")

    

    def search_requisition(self, requisition_number: str):
        self.search_box_for_list.fill(requisition_number)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.wait_for_timeout(5000)
          # Wait for the search results to load
        # self.search_box_for_list.press("Enter")
        self.get_full_page_screenshot(f"search_requisition_{requisition_number}")
        # expect(self.search_box_for_list).to_have_value(requisition_number)

    def select_all_items(self):
        self.select_all_checkbox.click()
        self.get_full_page_screenshot("select_all_items")
        self.wait_for_timeout(1000)  # Wait for the selection to be processed

    def unselect_all_items(self):
        self.unselect_all_checkbox.click()
        self.get_full_page_screenshot("unselect_all_items")
        self.wait_for_timeout(1000)  # Wait for the unselection to be processed
    
    def select_direct_purchase_method(self):
    # Step 1: Type into the input field
        self.select_method_dropdown.fill("Direct Purchase-(DPM)")
        self.page.wait_for_timeout(1000)
        self.select_method_dropdown.click()  # Focus the input
        self.page.keyboard.press("End")      # Move cursor to end
        self.page.keyboard.insert_text(" ")
    # Step 2: Wait for the suggestion to appear
        suggested_method = self.page.get_by_text("4Direct Purchase-(DPM)")
        # Wait and click
        suggested_method.wait_for(state="visible", timeout=5000)
        suggested_method.hover()
        suggested_method.click()
        self.wait_for_timeout(8000)

    def fill_remarks(self, remarks: str):
        self.remarks.fill(remarks)
        self.wait_for_timeout(5000)
        
    def save_tender_initiation(self):
        self.save_button.click()
        self.wait_for_timeout(5000)

    def submit_tender_initiation(self):
        self.submit_button.click()
        self.wait_for_timeout(5000)

    def confirm_submission(self):
        self.submit_confirmation.click()
        self.wait_for_timeout(5000)
        self.get_full_page_screenshot("tender_initiation_submitted")
        


    