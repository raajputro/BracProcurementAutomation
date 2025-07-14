import re
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect



class CheckoutPage(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # prepare the delivery schedule
        self.selectScheduleTable = page.locator('table#scheduleTable70233439')
        self.enterQuantity = page.locator('td#list70233439')
        self.selectExpectedDate = page.locator('input[id="date70233439"][class="todayDate"]')
        self.enterExpectedLocation = page.locator('input#location70233439')
        self.enterReceivingPersonPIN = page.locator('input[id="deliveryInfo70233439"]')
        # self.clickAddScheduleButton = page.locator('button[type="submit"]')
        # button[id="addScheduleButton70233439"]


    def confirm_Order(self, location, user_PIN):
        self.click_on_btn(self.selectScheduleTable)
        self.click_on_btn(self.enterQuantity)
        self.click_on_btn(self.selectExpectedDate)
        self.input_in_element(self.enterExpectedLocation, location)
        self.input_in_element(self.enterReceivingPersonPIN, user_PIN).click()
        # self.wait_for_timeout(5000)
