# import urllib2 from BeautifulSoup import BeautifulSoup soup = BeautifulSoup(urllib2.urlopen("https://www.google.com")) print soup.title.string;
import re

# from tests.testsdm.test_requisition_creation_flow import vendor_name
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect


class ShoppingCart(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.vendor_selection = page.locator('#vendorContainer112')
        # Staging server
        # self.selected_vendor_item = page.locator('input[id="radio112"]')
        # Software shop up vendor
        # self.selected_vendor_item = page.locator('input[id="radio140"]')
        self.selected_vendor_item = page.locator('input[id^="radio"]')
        self.select_cart_terms_and_condition = page.locator('input[id="termsofservice"]')
        self.select_cart_checkout_button = page.locator('button[id="checkout"][type="submit"]')

        # self.vendor_name = "Plan for demand"
        self.remove_button = page.locator('button[name="updatecart"][class="remove-btn"]')
        # self.cart_quantity = page.locator('//*[@id="topcartlink"]/a/span[2]')
        self.logo = page.locator("a[href='/']")

        self.click_username = page.locator('.ico-account')

        self.item_remarks_textarea_locator = page.locator(
            'xpath=//strong[normalize-space(text())="Specification"]/following-sibling::textarea')
        # or using partial match
        self.item_remarks_locator = page.locator('textarea[id^="itemRemarks"]')
        self.cart_quantity_input = page.locator('input[id^="itemquantity"]')
        self.update_shopping_cart = page.locator('button[id="updatecart"]')

    def remove_vendor_item(self):
        count = self.remove_button.count()
        print("Found " + str(count) + " vendor items")
        for i in range(count):
            self.remove_button.first.click()
            self.wait_for_timeout(2000)
        self.wait_for_timeout(5000)

    def select_vendor_and_checkout_cart_page(self):
        self.click_on_btn(self.vendor_selection)
        self.click_on_btn(self.selected_vendor_item)
        self.click_on_btn(self.select_cart_terms_and_condition)
        self.click_on_btn(self.select_cart_checkout_button)

    def select_vendor(self):
        self.click_on_btn(self.selected_vendor_item)
        # self.wait_for_timeout(5000)
        get_vendor_name = self.page.locator("//text()[contains(., 'Vendor')]/following::strong[1]").text_content()
        # self.wait_to_load_element(self.order_locator)
        # agreement = fa.split(":")[-1].strip()
        print(get_vendor_name)
        return get_vendor_name

    def update_shopping_cart_remarks(self):
        self.item_remarks_locator.nth(0).click()
        self.item_remarks_locator.nth(0).clear()
        self.input_in_element(self.item_remarks_locator.nth(0), "Marketplace item remarks 123 @#$ test")

    def update_shopping_cart_value(self):
        self.cart_quantity_input.nth(0).click()
        self.cart_quantity_input.nth(0).clear()
        self.input_in_element(self.cart_quantity_input.nth(0), "5")
        self.update_shopping_cart.click()
        self.wait_for_timeout(5000)

    def cart_page_checkout(self):
        self.click_on_btn(self.select_cart_terms_and_condition)
        self.click_on_btn(self.select_cart_checkout_button)
        self.wait_for_timeout(2000)

    def goto_home_page(self):
        self.click_on_btn(self.logo)
        self.wait_for_timeout(2000)

    def goto_order_list(self):
        self.click_on_btn(self.click_username)

    # Use for review requisition item order
    def item_remarks_update_for_multiple_items(self):
        self.item_remarks_locator.nth(0).click()
        self.item_remarks_locator.nth(0).clear()
        self.input_in_element(self.item_remarks_locator.nth(0), "test remarks 1")
        self.item_remarks_locator.nth(1).click()
        self.item_remarks_locator.nth(1).clear()
        self.input_in_element(self.item_remarks_locator.nth(1), "test remarks 2")

    def update_shopping_cart_info(self):
        self.click_on_btn(self.update_shopping_cart)

    def update_cart_value_for_multiple_items(self):
        self.cart_quantity_input.nth(0).click()
        self.cart_quantity_input.nth(0).clear()
        self.input_in_element(self.cart_quantity_input.nth(0), "5")
        self.cart_quantity_input.nth(1).click()
        self.cart_quantity_input.nth(1).clear()
        self.input_in_element(self.cart_quantity_input.nth(1), "10")

    def item_remarks_update_for_review_order(self):
        self.item_remarks_locator.nth(0).click()
        self.item_remarks_locator.nth(0).clear()
        self.input_in_element(self.item_remarks_locator.nth(0), "Review Order item test remarks 1")

    def update_cart_value_for_review_order(self):
        self.cart_quantity_input.nth(0).click()
        self.cart_quantity_input.nth(0).clear()
        self.input_in_element(self.cart_quantity_input.nth(0), "9")
        self.cart_quantity_input.nth(1).click()
        self.cart_quantity_input.nth(1).clear()
        self.input_in_element(self.cart_quantity_input.nth(1), "6")
