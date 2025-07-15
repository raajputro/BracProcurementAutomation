import re
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect


class CheckoutPage(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # prepare the delivery schedule
        self.select_schedule_table = page.locator('table#scheduleTable70233439')
        self.enter_quantity = page.locator('td#list70233439')
        self.select_expected_date = page.locator('input[id="date70233439"][class="todayDate"]')
        self.enter_expected_location = page.locator('input#location70233439')
        self.enter_receiving_person_pin = page.locator('input[id="deliveryInfo70233439"]')
        self.click_add_schedule_button = page.locator('button[id="addScheduleButton70233439"]')
        # self.click_add_schedule_button_1 = page.locator('button[type="submit"]')

    def delivery_schedule_preparation(self, location, user_pin):
        self.click_on_btn(self.select_schedule_table)
        self.click_on_btn(self.enter_quantity)
        self.click_on_btn(self.select_expected_date)
        self.input_in_element(self.enter_expected_location, location)
        self.input_in_element(self.enter_receiving_person_pin, user_pin)
        self.page.wait_for_timeout(5000)

    def click_add_schedule_btn(self):
        self.click_on_btn(self.click_add_schedule_button)
