import re
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect


class CheckoutPage(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        # write down all the elements here with locator format
        # prepare the delivery schedule
        # location73033552 , scheduleTable73003549
        self.select_schedule_table = page.locator('table#scheduleTable73033552')
        self.enter_quantity = page.locator('td#list73033552')
        self.select_expected_date = page.locator('input[id="date73033552"][class="todayDate"]')
        self.enter_expected_location = page.locator('input#location73033552')
        # location73003549
        self.enter_receiving_person_pin = page.locator('input#deliveryInfo73033552')

        # # Tooltip elements
        # self.valid_pin_heading = page.locator("div.np-tooltip h3", has_text="Valid PIN")
        # self.valid_pin_message = page.locator("div.np-tooltip p",
        #                                       has_text="Receiving Person PIN should be 8-digit numeric and valid")
        #
        # # Hidden fields
        # self.hidden_pin = page.locator("#pin70233439")
        # self.hidden_name = page.locator("#receivingPersonName70233439")
        # self.hidden_phone = page.locator("#receivingPersonPhone70233439")
        # self.hidden_designation = page.locator("#receivingPersonDesignation70233439")
        # self.hidden_program = page.locator("#receivingPersonProgram70233439")
        # self.hidden_department = page.locator("#receivingPersonDepartment70233439")
        # self.hidden_email = page.locator("#receivingPersonEmail70233439")
        #
        # # Error message
        # self.delivery_info_error = page.locator("#errordeliveryInfo70233439")

        self.click_add_schedule_button = page.locator('button[id="addScheduleButton73033552"]')
        self.continue_button = page.locator('#chkContinue')

        # Confirm order window
        self.order_remarks = page.locator('#confirmOrderRemarks')
        self.checkbox = page.locator('#termsofservice')
        self.confirm = page.get_by_role("button", name="Confirm")


    # self.click_add_schedule_button_1 = page.locator('button[type="submit"]')

    def delivery_schedule_preparation(self, location):
        self.click_on_btn(self.select_schedule_table)
        self.click_on_btn(self.enter_quantity)
        self.click_on_btn(self.select_expected_date)
        self.input_in_element(self.enter_expected_location, location)
        # self.input_in_element(self.enter_receiving_person_pin, user_pin)
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)

    def fill_concatenated_pin(self):
        pin_digits = ['0', '0', '0', '0', '6', '0', '0', '8']

        self.click_on_btn(self.enter_receiving_person_pin)

        for digit in pin_digits:
            self.enter_receiving_person_pin.type(digit)
            self.wait_for_timeout(200)

        self.page.keyboard.press("Enter")
        self.wait_for_timeout(10000)

    def click_add_schedule_btn(self):
        self.click_on_btn(self.click_add_schedule_button)

    def filling_order_remarks(self):
        self.click_on_btn(self.order_remarks)
        self.input_in_element(self.order_remarks,'The initiator places an order')
        # self.page.keyboard.press('Enter')
        self.wait_for_timeout(2000)

    def select_checkbox(self):
        self.click_on_btn(self.checkbox)
        self.wait_for_timeout(2000)

    def confirm_order(self):
        self.click_on_btn(self.confirm)
        self.wait_for_timeout(2000)

