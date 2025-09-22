from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateVendorBillPayable(ProcurementHomePage, BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)
        self.purchase_order_type = page.locator("#dpmNo")
        self.vendor_info = page.get_by_role("textbox", name="Search by vendor name(Example")
        self.order_no = page.locator("#woIdDiv_input")
        self.challan_no = page.locator("#challanIdDiv_input")
        self.bill_no = page.locator("#billNo")
        self.remarks = page.get_by_role("textbox", name="Max size of remarks 500")
        self.bill_date = page.locator("#billDate")
        self.bill_receive_date = page.locator("#billReceiveDate")
        self.select_all = page.get_by_role("link", name="Select All", exact=True)
        self.unselect_all = page.get_by_role("link", name="Unselect All")
        self.bill_recommender1 = page.locator("#poRecommenderIdDiv_input")
        self.bill_recommender2 = page.locator("#recommender2IdDiv_input")
        self.bill_approver = page.locator("#approverIdDiv_input")
        self.submit = page.get_by_role("button", name="Submit")
        self.submit_confirmation = page.get_by_label("Submit Confirmation").get_by_role("button", name="Submit")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')
        self.framework_order_no = page.locator('input[id="fwoNo"]')



    def vendor_bill_payable_information_for_framework_order(self):
        self.wait_for_timeout(7000)
        self.click_on_btn(self.framework_order_no)
        self.wait_for_timeout(3000)

    # def search_vendor(self, vendor_name: str):
    #     self.vendor_info.fill(vendor_name)
    #     self.page.keyboard.press("End")
    #     self.page.keyboard.type(" ")
    #     self.page.keyboard.press("Backspace")
    #     search_result = self.page.get_by_text(vendor_name)
    #     search_result.wait_for(state="visible", timeout=5000)
    #     search_result.hover()
    #     search_result.click()

    # def bill_number(self, bill_no_1: str):
    #     self.wait_for_timeout(5000)
    #     self.bill_no.fill(bill_no_1)
    #     self.page.keyboard.type(" ")
    #     self.page.keyboard.press("Backspace")
    #     self.wait_for_timeout(1000)

    # def bill_date_with_text(self, date: str):
    #     # Fill the estimated delivery date input field
    #     self.bill_date.scroll_into_view_if_needed()
    #     self.bill_date.fill(date)
    #     self.wait_for_timeout(1000)

    # def bill_receive_date_with_text(self, date: str):
    #     # Fill the estimated delivery date input field
    #     self.bill_receive_date.scroll_into_view_if_needed()
    #     self.bill_receive_date.fill(date)
    #     self.wait_for_timeout(1000)

    # def select_all_items(self):
    #     self.select_all.scroll_into_view_if_needed()
    #     self.select_all.click()
    #     self.wait_for_timeout(1000)

    # def unselect_all_items(self):
    #     self.unselect_all.click()
    #     self.wait_for_timeout(1000)

    # def Bill_recommender_selecting(self, recommender: str):
    #     self.bill_recommender.scroll_into_view_if_needed()
    #     self.bill_recommender.fill(recommender)
    #     self.page.keyboard.press("End")
    #     self.page.keyboard.type(" ")
    #     self.page.keyboard.press("Backspace")
    #     bill_recommender_selection = self.page.get_by_text(recommender)
    #     bill_recommender_selection.wait_for(state="visible", timeout=5000)
    #     bill_recommender_selection.hover()
    #     bill_recommender_selection.click()

    # def submit_bill(self):
    #     self.submit.scroll_into_view_if_needed()
    #     self.submit.click()
    #     self.wait_for_timeout(2000)

    # def confirm_submission(self):
    #     self.submit_confirmation.scroll_into_view_if_needed()
    #     self.submit_confirmation.click()
    #     self.wait_for_timeout(5000)

    # def search_challan_number(self, challan_num):
    #     self.challan_no.fill(challan_num)
    #     self.page.keyboard.press('End')
    #     self.page.keyboard.press(' ')
    #     self.wait_for_timeout(1000)
    #     self.page.keyboard.press('Enter')

    def search_vendor(self, vendor_name: str):
        self.vendor_info.fill(vendor_name)
        self.page.keyboard.press("End")
        self.page.keyboard.type(" ")
        self.page.keyboard.press("Backspace")
        search_result = self.page.get_by_text(vendor_name)
        search_result.wait_for(state="visible", timeout=5000)
        search_result.hover()
        search_result.click()
        self.wait_for_timeout(5000)

    def select_order_no(self, order_num: str):
        self.order_no.type(order_num)
        self.wait_for_timeout(5000)
        s_result = self.page.get_by_text(order_num).nth(0)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

        self.wait_for_timeout(1000)

    def select_order_no_1(self, order_num: str):
        self.order_no.click()
        self.order_no.fill(order_num)
        self.page.keyboard.press(' ')

        # self.page.keyboard.press("End")
        # self.page.keyboard.type(" ")
        # # self.page.keyboard.press("Backspace")
        # s_result = self.page.get_by_role('link', name=order_num)
        # s_result.wait_for(state="visible", timeout=5000)
        # s_result.hover()
        # s_result.click()

        self.wait_for_timeout(3000)

    def select_challan_no(self, challan_no: str):
        self.challan_no.type(challan_no)
        # self.page.keyboard.press("End")
        # self.page.keyboard.type(" ")
        # self.page.keyboard.press("Backspace")
        s_result = self.page.get_by_text(challan_no).nth(0)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

        self.wait_for_timeout(1000)

    def bill_number(self, bill_no_1: str):
        self.wait_for_timeout(5000)
        self.bill_no.fill(bill_no_1)
        # self.page.keyboard.type(" ")
        # self.page.keyboard.press("Backspace")
        # self.wait_for_timeout(1000)

    def bill_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.bill_date.scroll_into_view_if_needed()
        self.bill_date.fill(date)
        self.wait_for_timeout(1000)

    def bill_receive_date_with_text(self, date: str):
        # Fill the estimated delivery date input field
        self.bill_receive_date.scroll_into_view_if_needed()
        self.bill_receive_date.fill(date)
        self.wait_for_timeout(1000)

    def select_all_items(self):
        self.select_all.scroll_into_view_if_needed()
        self.select_all.click()
        self.wait_for_timeout(1000)

    def unselect_all_items(self):
        self.unselect_all.click()
        self.wait_for_timeout(1000)

    def Bill_recommender1_selecting(self, recommender: str):
        self.bill_recommender1.scroll_into_view_if_needed()
        self.bill_recommender1.type(recommender)
        s_result = self.page.get_by_text(recommender).nth(0)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

    def Bill_recommender2_selecting(self, recommender: str):
        self.bill_recommender2.scroll_into_view_if_needed()
        self.bill_recommender2.type(recommender)
        s_result = self.page.get_by_text(recommender).nth(0)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

    def Bill_approver_selecting(self, approver: str):
        self.bill_approver.scroll_into_view_if_needed()
        self.bill_approver.type(approver)
        s_result = self.page.get_by_text(approver).nth(0)
        s_result.wait_for(state="visible", timeout=5000)
        s_result.hover()
        s_result.click()

    def submit_bill(self):
        self.submit.scroll_into_view_if_needed()
        self.submit.click()
        self.wait_for_timeout(2000)

    def confirm_submission(self):
        self.submit_confirmation.scroll_into_view_if_needed()
        self.submit_confirmation.click()
        self.toast_msg.wait_for(state="visible", timeout=10000)
        toast_msg_text = self.toast_msg.text_content()
        print(toast_msg_text)
        self.wait_for_timeout(5000)

    def search_challan_number(self, challan_num):
        self.challan_no.fill(challan_num)
        self.page.keyboard.press('End')
        self.page.keyboard.press(' ')
        self.wait_for_timeout(1000)
        self.page.keyboard.press('Enter')


