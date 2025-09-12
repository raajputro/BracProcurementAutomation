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
        self.save_next = page.get_by_role("button", name="Save & Next")
        self.add_to_grid = page.get_by_role("button", name="Add to Grid")
        self.same_schedule = page.get_by_role("checkbox", name="Same schedule")
        self.est_delivery_date_with_text = page.locator('input#defaultDeliveryDate[placeholder="DD-MM-YYYY"]')
        self.delivery_location_dropdown = page.locator("#defaultDeliveryStoreId")
        self.delivery_location_box = page.get_by_placeholder("Note: 1. Address 2. Contact Person Name 3. Cell Number 4. Delivery Time")
        self.tender_template = page.locator("#bodyTemplateId")
        self.terms_condition_template =page.locator("#termTemplateId")
        self.award_notification_template = page.locator("#awardNotificationTemplateId")
        # self.Submission_date_input = page.get_by_label("Submission Date")
        self.Submission_date_input = page.locator('input[name="submissionDate"]')
        self.opening_date_input = page.locator('input[name="openingDate"]')
        self.opening_place_input = page.locator("#openingPlace")
        self.opening_offer_validity_input = page.locator('#offerValidityDay')
        self.tender_approver = page.locator('#signatoryMemberDiv_input')
        self.committee_type = page.locator("#committeeType")
        self.member_type = page.locator("#committeeMemberType")
        self.employee_name = page.locator("#name")
        self.add_to_grid = page.get_by_role("button", name="Add to Grid")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')
        self.tender_no_field = page.locator("#refNo")

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
        print(toast_msg)
    
        self.wait_for_timeout(5000)
        

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


    def default_evaluation_criteria(self, criteria: str = "Manufacturer authorization letter"):
        path = "//input[@type='checkbox' and following-sibling::text()[contains(., '" + criteria + "')]]"
        checkbox = self.page.locator(path)
        checkbox.scroll_into_view_if_needed()
        checkbox.click()
        self.wait_for_timeout(3000)

    def tender_submission_criteria(self, criteria: str = "TIN Certificate"):
        # Click on the tender submission criteria checkbox
        path = "//input[@type='checkbox' and following-sibling::text()[contains(., '" + criteria + "')]]"
        checkbox = self.page.locator(path)
        checkbox.scroll_into_view_if_needed()
        checkbox.click()
        self.wait_for_timeout(3000)

    def tender_template_selection(self, template: str = "QM Template"):
        self.tender_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.tender_template, template)
        self.wait_for_timeout(5000)

    def terms_condition_template_selection(self, template: str = "QM Terms And Conditions"):
        self.terms_condition_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.terms_condition_template, template)
        self.wait_for_timeout(5000)

    def award_notification_template_selection(self, template: str = "QM Award Notifications"):
        self.award_notification_template.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.award_notification_template, template)
        self.wait_for_timeout(5000)

    def submission_date(self, date: str):
        self.Submission_date_input.scroll_into_view_if_needed()
        self.Submission_date_input.fill(date)
        self.wait_for_timeout(5000)

    def opening_date(self, date: str):
        self.opening_date_input.scroll_into_view_if_needed()
        self.opening_date_input.wait_for(state="visible", timeout=3000)
        self.opening_date_input.click()
        self.opening_date_input.press("Control+A")
        self.opening_date_input.press("Backspace")
        self.wait_for_timeout(1000)
        self.opening_date_input.type(date, delay=100)
        self.wait_for_timeout(3000)

    def opening_place(self, place: str = "BRAC Center, 75 Mohakhali, Dhaka-1212"):
        self.opening_place_input.scroll_into_view_if_needed()
        self.opening_place_input.fill(place)
        self.wait_for_timeout(3000)

    def opening_offer_validity(self, days: str = "30"):
        self.opening_offer_validity_input.scroll_into_view_if_needed()
        self.opening_offer_validity_input.fill(days)
        self.wait_for_timeout(3000)

    def tender_approver_selecting(self, approver: str):
        self.tender_approver.wait_for(state="visible", timeout=3000)
        self.tender_approver.scroll_into_view_if_needed()
        self.tender_approver.fill(approver)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace")
        tender_approver_selection = self.page.get_by_text(approver)
        tender_approver_selection.wait_for(state="visible", timeout=5000)
        tender_approver_selection.hover()
        tender_approver_selection.click()
        self.wait_for_timeout(3000)

    def committee_type_selection(self, type: str ):

        self.committee_type.wait_for(state="visible", timeout=3000)
        self.committee_type.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.committee_type, type)
        self.wait_for_timeout(1000)

    def member_type_selection(self, type: str):
        self.member_type.wait_for(state="visible", timeout=3000)
        self.member_type.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.member_type, type)
        self.wait_for_timeout(1000)


    def select_member(self, member: str):
        self.employee_name.wait_for(state="visible", timeout=5000)
        self.employee_name.scroll_into_view_if_needed()

    # Clear and type the member input
        self.employee_name.fill("")
        self.employee_name.fill(member)
        self.page.wait_for_timeout(1000)

    # Ensure suggestions load
        self.employee_name.click()
        self.page.keyboard.press("End")
        self.page.keyboard.insert_text(" ")
        self.page.keyboard.press("Backspace")
        self.page.wait_for_timeout(1000)

    # Define the expected suggestion locator
        suggestion_locator = self.page.locator(f"a.ui-corner-all", has_text=member).first

        try:
            suggestion_locator.wait_for(state="visible", timeout=5000)
            suggestion_locator.scroll_into_view_if_needed()
            suggestion_locator.hover()
            suggestion_locator.click()
            self.page.wait_for_timeout(1000)
        except Exception as e:
            self.page.screenshot(path=f"select_member_error_{member}.png")
            raise RuntimeError(f"Could not select member '{member}'. Error: {e}")
        
    def add_committee_member_to_grid(self):

        self.add_to_grid.click()
        self.wait_for_timeout(5000)

    def submit_tender_initiation(self):
        print("clicking on submit button")
        self.submit_button.click()
        self.wait_for_timeout(5000)


    def confirm_submission(self):
        print("clicked on confirm submission button")
        self.submit_confirmation.click()
        self.wait_for_timeout(5000)
        self.get_full_page_screenshot("tender_initiation_submitted")

        
    def get_tender_number(self) -> str:
        self.tender_value = self.tender_no_field.input_value()
        print("Generated Purchase Order Number:", self.tender_value)
        return self.tender_value
        


    