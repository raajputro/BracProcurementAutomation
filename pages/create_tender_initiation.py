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
        self.select_method_dropdown_options_qm = page.get_by_text("Quotation Method-(QM)")
        self.remarks= page.locator("textarea#remarks.height65[placeholder='Max size of remarks 250 characters']")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.locator('span.ui-button-text', has_text="Submit")
        self.save_button = page.get_by_role("button", name="Save")
        self.save_next = page.get_by_role("button", name="Save & Next ->>")
        self.add_to_grid = page.get_by_role("button", name="Add to Grid")
        self.same_schedule = page.get_by_role("checkbox", name="Same schedule")
        self.est_delivery_date_with_text = page.locator('input#defaultDeliveryDate[placeholder="DD-MM-YYYY"]')
        self.delivery_location_dropdown = page.locator("#defaultDeliveryStoreId")
        self.delivery_location_box = page.get_by_placeholder("Note: 1. Address 2. Contact Person Name 3. Cell Number 4. Delivery Time")
        self.tender_template = page.locator("#bodyTemplateId")
        self.terms_condition_template =page.locator("#termTemplateId")
        self.award_notification_template = page.locator("#awardNotificationTemplateId")

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

    def select_Quotation_method(self):
    # Step 1: Type into the input field
        self.select_method_dropdown.fill("Quotation Method-(QM)")
        self.page.wait_for_timeout(1000)
        self.select_method_dropdown.click()  # Focus the input
        self.page.keyboard.press("End")      # Move cursor to end
        self.page.keyboard.insert_text(" ")
    # Step 2: Wait for the suggestion to appear
        suggested_method = self.page.get_by_text("Quotation Method-(QM)")
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

    def go_to_save_next(self):
        self.save_next.click()
        self.wait_for_timeout(5000)

    def add_item_to_grid(self):
        self.add_to_grid.click()
        self.wait_for_timeout(5000)

    def same_delivery_schedule(self):
        self.same_schedule.scroll_into_view_if_needed()
        self.same_schedule.click()
        self.wait_for_timeout(1000)

    def estimated_delivery_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.est_delivery_date_with_text.scroll_into_view_if_needed()
        self.est_delivery_date_with_text.fill(date)
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


    def default_evaluation_criteria(self, criteria: str = "Manufacturer authorization letter"):
        # Click on the default evaluation criteria checkbox
        checkbox = self.get_by_level(criteria)
        checkbox.check()
        checkbox.scroll_into_view_if_needed()
        checkbox.click()
        self.wait_for_timeout(1000)

    def tender_submission_criteria(self, criteria: str = "TIN Certificate"):
        # Click on the tender submission criteria checkbox
        checkbox = self.get_by_level(criteria)
        checkbox.check()
        checkbox.scroll_into_view_if_needed()
        checkbox.click()

    def tender_template_selection(self, template: str = "QM Template"):
        self.tender_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.tender_template, template)

    def terms_condition_template_selection(self, template: str = "QM Terms And Conditions"):
        self.terms_condition_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.terms_condition_template, template)

    def award_notification_template_selection(self, template: str = "QM Award Notifications"):
        self.award_notification_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.award_notification_template, template)

    def submit_tender_initiation(self):
        self.submit_button.click()
        self.wait_for_timeout(5000)

    def confirm_submission(self):
        self.submit_confirmation.click()
        self.wait_for_timeout(5000)
        self.get_full_page_screenshot("tender_initiation_submitted")
        


    