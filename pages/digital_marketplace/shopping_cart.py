# import urllib2 from BeautifulSoup import BeautifulSoup soup = BeautifulSoup(urllib2.urlopen("https://www.google.com")) print soup.title.string;
import re

import pages.login_page
# from tests.testsdm.test_requisition_creation_flow import vendor_name
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect


class ShoppingCart(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.vendor_container = page.locator('div[id^="vendorContainer"]')
        self.selected_vendor_item = page.locator('input[id^="radio"]')
        self.requisition_locator = page.locator('a.item-requisition-link')
        # self.requisition_locator = page.locator('a[class="item-requisition-link"]')
        self.checked_requisition_locator = page.locator('input[checked="checked"][type="checkbox"]')
        self.cart_form = page.locator('form[id="shopping-cart-form"]')

        self.selected_radio = page.locator(
            "//div[input[@type='radio' and @checked='checked']]/label"
        )

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

    def select_vendor_by_name(self, vendor_name: str, requisition_number):
        # Build a locator that directly finds the radio button whose label contains the vendor_name
        radio_button = self.page.locator(
            f"//div[starts-with(@id,'vendorContainer')]//label[contains(., '{vendor_name}')]/preceding-sibling::input[@type='radio']"
        )

        if radio_button.count() == 0:
            print(f"Vendor '{vendor_name}' not found.")
            return False

        print(f"Found vendor: {vendor_name}")
        radio_button.check()
        self.wait_for_timeout(5000)
        print(f"Selected radio button for vendor: {vendor_name}")
        # self.page.wait_for_load_state("networkidle", timeout=15000)

        # Now safely get checked requisitions after reload
        # checked_reqs = self.page.locator(
        #     "//div[input[@type='checkbox' and @checked='checked']]/label/strong"
        # )
        checked_reqs = self.page.locator("//input[@type='checkbox' and @checked]/following-sibling::label/strong")

        count = checked_reqs.count()
        print(f"Found {count} checked requisition(s).")

        for i in range(count):
            print(f"value of i: {i}")
            req_number = checked_reqs.nth(i+1).inner_text().strip()
            print(f"requisition #{i + 1}: {req_number}")
            # All okay
            if req_number != requisition_number:
                checked_reqs.nth(i+1).click()
                print(f"Unchecked requisition #{i + 1}: {req_number}")

            else:
                print(f"Checked requisition #{i + 1}: {req_number}")
        return True

    def select_vendor_for_requisition(self, requisition_number: str):
        # Step 1: Find the requisition link by number
        requisition_locator = self.page.locator(
            f"//a[@class='item-requisition-link' and contains(., '{requisition_number}')]"
        )

        if requisition_locator.count() == 0:
            print(f"Requisition '{requisition_number}' not found.")
            return False

        print(f"Found requisition: {requisition_number}")

        # Step 2: From requisition, go up to vendor container
        vendor_block = requisition_locator.locator("xpath=ancestor::div[contains(@id,'vendorContainer')]")

        # Step 3: Get vendor name text
        vendor_name = vendor_block.locator("label").inner_text()
        print(f"Vendor found for requisition {requisition_number}: {vendor_name.strip()}")

        # Step 4: Click its radio button
        radio_button = vendor_block.locator("input[@type='radio']")
        radio_button.check()
        print(f"Selected vendor radio button for '{vendor_name.strip()}' linked to requisition {requisition_number}")

        return True

    def select_vendor_for_requisition_found(self, requisition_number: str):
        # Locate all matching requisition links
        requisition_matches = self.page.locator(f"a.item-requisition-link:has-text('{requisition_number}')")

        if requisition_matches.count() == 0:
            print(f"Requisition {requisition_number} not found in cart.")
            return

        print(f"Found {requisition_matches.count()} match(es) for requisition: {requisition_number}")

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
