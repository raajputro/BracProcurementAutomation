import re

from pages.digital_marketplace.shopping_cart import ShoppingCart
from utils.basic_actionsdm import BasicActionsDM
# from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect
from datetime import datetime, timedelta


class CheckoutPage(ShoppingCart, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        # prepare the delivery schedule
        self.schedule_quantity = page.locator('input[type="number"]')
        self.schedule_expected_date = page.locator('input[type="date"][class="todayDate"]')
        self.schedule_expected_location = page.locator('input[id^="location"]')
        self.schedule_receiving_person_pin = page.locator('input[id^="deliveryInfo"]')

        # self.click_add_schedule_button = page.locator('button[id^="addScheduleButton"]')
        self.click_add_schedule_button = page.locator('button[id^="addScheduleButton"][class="button1"]')
        self.continue_button = page.locator('#chkContinue')

        # Confirm order window
        self.order_remarks = page.locator('#confirmOrderRemarks')
        self.checkbox = page.locator('#termsofservice')
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.view_order_details = page.locator("//a[contains(text(),'Click here for order details.')]")
        # self.view_order_details_another = page.locator("a", has_text="Click here for order details."||"div.details-link", has_text="Click here for order details.")

        # Review order locator
        self.schedule_delete_icon = page.locator('button[class="removeScheduleButton"]')
        self.schedule_edit_button = page.locator('button[class="editScheduleButton"][type="button"]')
        self.update_schedule_button = page.locator('button[id^="updateScheduleButton"][class="button1"]')

    def update_quantity(self, quantity):
        self.schedule_quantity.clear()
        self.wait_for_timeout(3000)
        self.input_in_element(self.schedule_quantity, quantity)
        self.wait_for_timeout(3000)

    def update_expected_date(self):
        self.schedule_expected_date.click()
        expected_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.schedule_expected_date.fill(expected_date)
        self.wait_for_timeout(5000)
        print(f"Filled expected date with: {expected_date}")

    def delivery_schedule_preparation(self, location, pin):
        self.input_in_element(self.schedule_expected_location, location)
        self.page.wait_for_timeout(3000)
        self.input_in_element(self.schedule_receiving_person_pin, pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)

    # concatenated
    def fillup_receiving_pin(self):
        pin_digits = ['0', '0', '0', '0', '6', '0', '0', '8']

        self.click_on_btn(self.schedule_receiving_person_pin)

        for digit in pin_digits:
            self.schedule_receiving_person_pin.type(digit)
            self.wait_for_timeout(200)
        # self.wait_for_timeout(5000)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(10000)

    def click_add_schedule_btn(self):
        self.click_on_btn(self.click_add_schedule_button.nth(0))
        # self.wait_for_timeout(5000)

    def click_continue(self):
        self.click_on_btn(self.continue_button)

    def fillup_order_remarks(self, input_remarks):
        self.click_on_btn(self.order_remarks)
        self.order_remarks.clear()
        self.input_in_element(self.order_remarks, input_remarks)
        self.wait_for_timeout(2000)

    def select_terms_of_service(self):
        self.click_on_btn(self.checkbox)
        # self.wait_for_timeout(2000)

    def confirm_order(self):
        self.click_on_btn(self.confirm_button)
        self.wait_for_timeout(5000)
        order_locator = self.page.locator("text=ORDER REFERENCE NO:").text_content()
        # self.wait_to_load_element(self.order_locator)
        order_reference_number = order_locator.split(":")[-1].strip()
        print("Order reference number: " + order_reference_number)
        return order_reference_number

    def goto_public_side_order_details_view(self):
        self.click_on_btn(self.view_order_details)
        self.wait_for_timeout(2000)
        order_status_pending = self.page.locator("text=Order Status:").text_content()
        order_status = order_status_pending.split(":")[-1].strip()
        print("Order status: " + order_status)
        return order_status

    def delivery_schedule_preparation_item_1(self, location, pin):
        self.click_on_btn(self.schedule_quantity.nth(0))
        self.click_on_btn(self.schedule_expected_date.nth(0))
        self.input_in_element(self.schedule_expected_location.nth(0), location)
        self.page.wait_for_timeout(5000)
        self.input_in_element(self.schedule_receiving_person_pin.nth(0), pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)
        self.click_on_btn(self.click_add_schedule_button.nth(0))

    def delivery_schedule_preparation_item_2(self, location, pin):
        self.click_on_btn(self.schedule_quantity.nth(1))
        self.click_on_btn(self.schedule_expected_date.nth(1))
        self.input_in_element(self.schedule_expected_location.nth(1), location)
        self.page.wait_for_timeout(5000)
        self.input_in_element(self.schedule_receiving_person_pin.nth(1), pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)
        self.click_on_btn(self.click_add_schedule_button.nth(1))

    # Use for delete review item
    def update_delivery_location_for_review_order_item_1(self):
        self.schedule_expected_location.nth(0).click()
        self.input_in_element(self.schedule_expected_location.nth(0), "Savar, Dhaka")
        self.schedule_receiving_person_pin.nth(0).click()

    def update_receiving_person_info_for_review_order(self, pin):
        self.input_in_element(self.schedule_receiving_person_pin.nth(0), pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)
        self.click_on_btn(self.click_add_schedule_button.nth(0))

    def update_delivery_schedule_for_review_order(self):
        self.click_on_btn(self.schedule_quantity.nth(1))
        self.schedule_quantity.nth(1).clear()
        self.input_in_element(self.schedule_quantity.nth(1), "7")
        self.schedule_expected_date.nth(1).click()
        self.wait_for_timeout(5000)
        next_date = (datetime.strptime("2025-08-14", "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        self.schedule_expected_date.nth(1).fill(next_date)

    def update_delivery_location_for_review_order_item_2(self):
        self.schedule_expected_location.nth(1).click()
        self.schedule_expected_location.nth(1).clear()
        self.input_in_element(self.schedule_expected_location.nth(1), "Cumilla")

    def add_remaining_schedule_item_for_review_order(self, pin):
        self.input_in_element(self.schedule_expected_location.nth(1), "Rampura, Dhaka")
        self.page.wait_for_timeout(5000)
        self.input_in_element(self.schedule_receiving_person_pin.nth(1), pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)

    def fillup_order_remarks_for_review_order(self):
        self.click_on_btn(self.order_remarks)
        self.order_remarks.clear()
        self.input_in_element(self.order_remarks, 'The initiator places the order for review again.')
        self.wait_for_timeout(2000)
