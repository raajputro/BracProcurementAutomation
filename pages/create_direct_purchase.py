
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateDirectPurchase(ProcurementHomePage, BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.po_value = ''
        self.vendor_info = page.get_by_role("textbox", name="Min 3 characters")
        
        self.select_all_checkbox = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all_checkbox = page.get_by_role("link", name="Unselect All", exact=True)
        self.search_requisition = page.get_by_role("textbox", name="Please enter item name or REQ")
        self.save_next_page = page.get_by_role("button", name="Save & Next ->>")
        self.same_schedule = page.get_by_role("checkbox", name="Same schedule")
        self.estimated_delivery_date_using_calendar_box = page.locator("#sameDeliveryScheduleId").get_by_role("img",
                                                                                                              name="Select date")
        self.est_delivery_date_with_text = page.locator('input#defaultDeliveryDate[placeholder="DD-MM-YYYY"]')
        self.delivery_location_dropdown = page.locator("#defaultDeliveryStoreId")
        self.delivery_location_box = page.get_by_placeholder("Note: 1. Address 2. Contact Person Name 3. Cell Number 4. Delivery Time")

        self.template_selection_dropdown = page.locator("#purchaseLetterBodyTemplateId")
        self.direct_purchase_approver = page.locator("#signatoryMemberDiv_input")

        self.purchase_submit = page.get_by_role("button", name="Submit")
        self.purchase_submit_confirmation = page.get_by_label("Submit Confirmation").get_by_role("button",
                                                                                                 name="Submit")
        self.purchase_order_no_field = page.locator("#refNo")

    def search_vendor(self, vendor_name: str):
        self.vendor_info.fill(vendor_name)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace")

        search_result = self.page.get_by_text(vendor_name)
        search_result.wait_for(state="visible", timeout=5000)
        search_result.hover()
        search_result.click()

    def same_delivery_schedule(self):
        self.same_schedule.scroll_into_view_if_needed()
        self.same_schedule.click()
        self.wait_for_timeout(1000)

    def estimated_delivery_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.est_delivery_date_with_text.scroll_into_view_if_needed()
        self.est_delivery_date_with_text.fill(date)
        # Validate the date format

    def estimated_delivery_date_using_calendar(self):
        # Click on the estimated delivery date calendar icon
        self.estimated_delivery_date_using_calendar_box.scroll_into_view_if_needed()
        self.estimated_delivery_date_using_calendar_box.click()

    def delivery_location_dropdown_select(self, delivery_location: str = "Central Store"):

        self.select_from_list_by_value(self.delivery_location_dropdown, delivery_location)

    def delivery_location(self, location: str):
        # Fill the delivery location input field
        self.delivery_location_box.scroll_into_view_if_needed()
        self.delivery_location_box.fill(location)

    def search_item_by_name(self, item_name: str):
        self.search_requisition.scroll_into_view_if_needed()
        self.search_requisition.fill(item_name)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")  # Adding a space to trigger the search
        self.wait_for_timeout(5000)

    def select_all_items(self):
        self.select_all_checkbox.scroll_into_view_if_needed()
        self.select_all_checkbox.click()
        self.wait_for_timeout(1000)

    def unselect_all_items(self):
        self.unselect_all_checkbox.click()
        self.wait_for_timeout(1000)

    def save_and_next(self):
        self.save_next_page.scroll_into_view_if_needed()
        self.save_next_page.click()
        self.wait_for_timeout(5000)

    def get_purchase_order_number(self) -> str:
        self.po_value = self.purchase_order_no_field.input_value()
        print("Generated Purchase Order Number:", self.po_value)
        return self.po_value
        # po_value = po_number

    def template_selection(self, template: str = "Direct Purchase Order Template"):
        self.template_selection_dropdown.scroll_into_view_if_needed()
        self.select_from_list_by_value(self.template_selection_dropdown, template)

    def direct_purchase_approver_selecting(self, approver: str):
        self.direct_purchase_approver.scroll_into_view_if_needed()
        self.direct_purchase_approver.fill(approver)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace")
        direct_purchase_approver_selection = self.page.get_by_text(approver)
        direct_purchase_approver_selection.wait_for(state="visible", timeout=5000)
        direct_purchase_approver_selection.hover()
        direct_purchase_approver_selection.click()

    def submit_direct_purchase(self):
        self.purchase_submit.scroll_into_view_if_needed()
        self.purchase_submit.click()
        self.wait_for_timeout(2000)

    def confirm_submission(self):
        self.purchase_submit_confirmation.scroll_into_view_if_needed()
        self.purchase_submit_confirmation.click()
        self.wait_for_timeout(5000)