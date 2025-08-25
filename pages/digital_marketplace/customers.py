from symtable import Class

# from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM

from playwright.sync_api import expect


class Customers(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.customers_menu = page.locator('i[class="nav-icon far fa-user"]')
        self.customers_submenu = page.locator('a[href="/Admin/Customer/List"]')

        # Customer search parameter
        self.first_name = page.locator('input[id="SearchFirstName"]')
        self.last_name = page.locator('input[id="SearchLastName"]')
        self.email = page.locator('input[id="SearchEmail"]')
        self.username = page.locator('input[id="SearchUsername"]')
        self.ip_address = page.locator('input[id="SearchIpAddress"]')
        self.dob_month = page.locator('input[id="SearchMonthOfBirth"]')
        self.dob_day = page.locator('input[id="SearchDayOfBirth"]')
        self.user_group = page.locator('.k-multiselect-wrap')

        self.customer_search_button = page.locator('button[id="search-customers"]')

    def view_customers_list(self):
        self.customers_menu.click()
        # self.wait_for_timeout(5000)
        self.customers_submenu.click()
        # self.wait_for_timeout(5000)

    def search_vendor(self, customer_name):
        self.first_name.click()
        self.input_in_element(self.first_name, customer_name)
        # self.wait_for_timeout(5000)

    def search_customers(self):
        self.customer_search_button.click()
        self.wait_for_timeout(5000)
        username = self.page.locator("td").nth(1).inner_text()

        print(username)
        return username
