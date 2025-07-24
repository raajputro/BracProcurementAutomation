import re

from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class ItemReceive(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.search_order = page.get_by_role("textbox", name="Search DP/FO/PO/CO Order No.")
        self.search_result = page.get_by_text() #need help from bhaiyaaa po value kivabe dibooo
        self.challan_no = page.locator("#challanNo")
        self.challan_date = page.locator("#challanDate")
        self.receive_date = page.locator("#receiveDate")
        self.received_place = page.locator("#receivePlace")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all = page.get_by_role("link", name="Unselect All")
        self.remarks = page.locator("#remarks")
        self.submit = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.get_by_label("Submit Confirmation").get_by_role("button", name="Submit")

    def search_order_for_item_receive(self, oder_no: str):
        self.search_order.fill(oder_no)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace") 
        s_result = self.page.get_by_text(oder_no)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

    def set_challan_number(self, challan_number):
        self.challan_no.fill(challan_number)
        self.wait_for_timeout(2000)

    def challan_date(self, date: str):
        # Fill the challan date input field
        self.challan_date.scroll_into_view_if_needed()
        self.challan_date.fill(date)
    def received_date(self, date: str):
        # Fill the received date input field
        self.receive_date.scroll_into_view_if_needed()
        self.receive_date.fill(date)
        # Validate the date format

    def receive_place(self, place_name: str):
        self.received_place.scroll_into_view_if_needed()
        self.received_place.fill(place_name) 
        self.wait_for_timeout(1000)

    def select_all_items(self):
        self.select_all.scroll_into_view_if_needed()
        self.select_all.click()
        self.wait_for_timeout(1000)

    def unselect_all_items(self): 
        self.unselect_all.click()
        self.wait_for_timeout(1000)


    def submit_item_receive(self):
        self.submit.scroll_into_view_if_needed()
        self.submit.click()
        self.wait_for_timeout(2000)


    def confirm_submission(self):
        self.submit_confirmation.scroll_into_view_if_needed()
        self.submit_confirmation.click()
        self.wait_for_timeout(5000)