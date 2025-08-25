import re

from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage

from playwright.sync_api import expect


class OrderListPublicSide(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        #   Write down all the elements here with locator format
        # Goto order list page
        self.pending_approval_orders = page.locator("a[href='/customer/pendingApprovalOrders']",
                                                    has_text="Pending Approval Orders")

        # Search order reference number
        self.search_order_number = page.get_by_placeholder('Order Reference Number')
        self.search_button = page.locator('button[class="button"][type="submit"]')

        # Go to pending approval order details
        # self.click_details_button = page.locator(
        #     "button.order-details-button[onclick*='/pendingApprovalOrderDetails/2472']"
        # )
        self.details_button = page.get_by_role("button", name="Details")
        self.approve_order_button = page.get_by_role("link", name="Approve Order")
        self.yes_button = page.get_by_role("button", name="YES")
        self.close_button = page.locator("button.modal-close.modal-toggle")

        self.goto_order_list = page.locator("a.ico-account")

        # Order review
        self.review_button = page.locator("a.review-order-button")
        self.review_confirm_button = page.get_by_role("button", name="Review")
        self.enter_review_reasons = page.locator('textarea[id="reviewRemarks"]')
        self.enter_minimum_characters = page.locator('textarea[id="reviewRemarks"]')

        # Preview locator
        self.preview_button = page.get_by_role("link", name="Preview")
        self.cancel_print_button = page.get_by_role("button", name="Cancel")

        # Order rejection locator
        self.reject_button = page.get_by_role("link", name="Reject Order")
        self.cancellation_remarks = page.locator("textarea[name='cancelRemarks']")

        # Pending Approval Order Checkbox for single order
        self.pending_approval_checkbox = page.locator("input#pendingApprovalOrder")

        self.order_1 = page.locator('input[type="checkbox"][value="2469"]')
        self.order_2 = page.locator('input[type="checkbox"][value="2470"]')
        self.order_3 = page.locator('input[type="checkbox"][value="2467"]')
        # Select approve button for multiselect approval
        self.click_multiselect_approve = page.locator('button[id="pendingApprovalOrder-selected"]')

    def goto_pending_approval_orders_list(self):
        self.click_on_btn(self.pending_approval_orders)
        self.wait_for_timeout(2000)

    def search_order_input(self, order_reference_number):
        self.input_in_element(self.search_order_number, order_reference_number)
        # self.wait_for_timeout(2000)
        self.click_on_btn(self.search_button)
        self.wait_for_timeout(2000)
        # self.print('Search_pending_approval_order_number')

    def goto_pending_approval_order_details(self):
        # self.click_on_btn(self.click_details_button)
        self.click_on_btn(self.details_button)
        self.wait_for_timeout(2000)
        # self.print('View_pending_approval_order_details')

    def approve_order(self):
        self.click_on_btn(self.approve_order_button)
        # self.print('Show_approve_order_popup')
        self.click_on_btn(self.close_button)
        self.click_on_btn(self.approve_order_button)
        self.click_on_btn(self.yes_button)
        # self.print('Successfully_approve_order_details')

    def check_pending_approval(self):
        self.pending_approval_checkbox.check()
        self.wait_for_timeout(2000)

    def uncheck_pending_approval(self):
        self.pending_approval_checkbox.uncheck()
        self.wait_for_timeout(2000)

    def multiselect_approve(self):
        self.click_on_btn(self.click_multiselect_approve)
        self.wait_for_timeout(2000)

    def open_review_popup(self):
        self.click_on_btn(self.review_button)
        self.wait_for_timeout(2000)

    # Click on Review confirm without filling mandatory field
    def check_review_mandatory_validation(self):
        self.click_on_btn(self.review_confirm_button)
        self.wait_for_timeout(2000)
        # try:
        #     # Expect validation error to appear
        #     validation_error = self.page.locator("span.review-error-message")
        #     expect(validation_error).to_be_visible()
        #     self.get_full_page_screenshot('check_review_mandatory_validation')
        #     expect(validation_error).to_have_text(re.compile(r"Please fill out this field.", re.I))
        # except Exception as e:
        #     raise AssertionError(f"Mandatory validation check failed: {e}")

    def check_minimum_characters_validation(self):
        self.input_in_element(self.enter_minimum_characters, '!')
        self.click_on_btn(self.enter_minimum_characters)
        self.wait_for_timeout(2000)
        self.input_in_element(self.enter_minimum_characters, 'ab')
        self.click_on_btn(self.enter_minimum_characters)
        self.wait_for_timeout(2000)
        self.click_on_btn(self.review_confirm_button)

    def check_max_min_characters_validation(self):
        self.click_on_btn(self.review_confirm_button)
        characters = "w"
        # characters = "44Send back reasons~!@#$%^&*()_+}{|”:?><~`,./’;[]=-\Docx word“confirm” is a verb in its present tense, meaning that it happens right now currently. the word “confirmed” is this same word in the past tense, meaning that confirmation occurred in the past. 2556"

        self.input_in_element(self.enter_review_reasons, characters)
        if (len(characters) >= 3) and (len(characters) <= 255):
            print(len(characters))
        elif len(characters) == 2:
            print(len(characters))
        elif len(characters) == 1:
            print(len(characters))
        elif len(characters) == 0:
            print(len(characters))
        else:
            print("Sorry!")
        self.wait_for_timeout(5000)

    def remove_review_popup(self):
        self.click_on_btn(self.close_button)
        self.wait_for_timeout(2000)

    def order_review(self):
        self.click_on_btn(self.review_button)
        self.wait_for_timeout(2000)
        self.input_in_element(self.enter_review_reasons,
                              'Send back reasons~!@#$%^&*()_+}{|”:?><~`,./’;[]=-\Docx word“confirm” is a verb in its present tense, meaning that it happens right now currently. the word “confirmed” is this same word in the past tense, meaning that confirmation occurred in the past. 2556')
        self.click_on_btn(self.review_confirm_button)

    def open_preview(self):
        self.click_on_btn(self.preview_button)
        self.wait_for_timeout(2000)
        # self.click_on_btn(self.cancel_print_button)
        # self.wait_for_timeout(2000)

    def open_order_rejection_popup(self):
        self.click_on_btn(self.reject_button)
        self.wait_for_timeout(2000)

    def remove_order_rejection_popup(self):
        self.click_on_btn(self.close_button)
        self.wait_for_timeout(2000)

    def check_minimum_characters_validation_for_order_rejection(self):
        # self.click_on_btn(self.yes_button)
        self.input_in_element(self.cancellation_remarks, '')
        self.click_on_btn(self.yes_button)
        self.wait_for_timeout(2000)
        self.input_in_element(self.cancellation_remarks, '1')
        self.click_on_btn(self.yes_button)
        self.wait_for_timeout(2000)
        self.input_in_element(self.cancellation_remarks, 'a@')
        self.click_on_btn(self.yes_button)
        self.wait_for_timeout(2000)

    def rejection_max_characters_input(self):
        # characters = "w"
        characters = "Order rejection remarks or reasons~!@#$%^&*()_+}{|”:?><~`,./’;[]=-\Docx word“confirm” is a verb in its present tense, meaning that it happens right now currently. the word “confirmed” is this same word in the past tense, meaning that confirmation occurred in the past. 2556test"
        self.input_in_element(self.cancellation_remarks, characters)
        if (len(characters) >= 3) and (len(characters) <= 256):
            print(len(characters))
        else:
            print("Sorry!")
        self.wait_for_timeout(5000)

    def confirm_rejection(self):
        self.click_on_btn(self.yes_button)
        self.wait_for_timeout(2000)

    def check_uncheck_order(self):
        self.pending_approval_checkbox.check()
        self.wait_for_timeout(2000)
        self.pending_approval_checkbox.uncheck()
        self.wait_for_timeout(2000)
        self.pending_approval_checkbox.check()
        self.wait_for_timeout(2000)

    def confirm_multi_select_approve(self):
        self.click_on_btn(self.click_multiselect_approve)
        self.wait_for_timeout(2000)

    def multi_select_approve1(self):
        self.order_1.check()
        self.wait_for_timeout(2000)
        # self.order_2.check()
        # self.wait_for_timeout(2000)
        order_3 = "2025/TRN-2467"
        if order_3 == "2025/TRN-2467":
            self.order_3.check()
        else:
            print("Order not available for approval at this time.")
        self.wait_for_timeout(5000)
        self.order_3.uncheck()
        self.wait_for_timeout(2000)
