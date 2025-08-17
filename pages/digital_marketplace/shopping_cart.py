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
        # self.requisition_locator = page.locator('a.item-requisition-link')
        self.requisition_locator = page.locator('a.item-requisition-link')
        # self.requisition_locator = page.locator('a[class="item-requisition-link"]')
        self.cart_form = page.locator('form[id="shopping-cart-form"]')

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

    # def select_cart_vendor(self, vendor):
    #     if


    def select_order_vendor(self, vendor):
        # self.click_on_btn(self.selected_vendor_item, vendor)
        self.page.locator(f"div:has(label:has-text('{vendor}')) input[id^='radio']").click()
        # self.page.locator(f"div:has(label:has-text('{vendor}')) input[type='radio']").click()

    def select_vendor_for_requisition(self, requisition_number: str):
        # Locate all matching requisition links
        requisition_matches = self.page.locator(f"a.item-requisition-link:has-text('{requisition_number}')")

        if requisition_matches.count() == 0:
            print(f"Requisition {requisition_number} not found in cart.")
            return

        print(f"Found {requisition_matches.count()} match(es) for requisition: {requisition_number}")

    # # req_locator = self.page.locator(f"text={requisition_number}")
    #
    # count = req_locator.count()
    # if count == 0:
    #     print(f"Requisition {requisition_number} not found in cart.")
    # else:
    #     print(f"Found {req_locator.count()} match(es) for requisition: {requisition_number}")
    #     first_req = req_locator.first
    #     red_button = first_req.locator("xpath=./ancestor::*[.//input[@type='radio']][1]//input[@type='radio']")
    #     red_button.click()

    # req = self.page.locator(f"text={requisition_number}").first
    # # req = self.page.locator("text=REQ20250014472").first
    # vendor_div=req.locator("xpath=ancestor::div[contains(.,'Vendor')]")
    # vendor_div.locator("xpath=.//input[@type='radio']").first.click()
    # vend_name=vendor_div.locator("xpath=.//b").inner_text()
    # print(f"vend name {vend_name} not found in cart.")
    # self.click_on_btn(self.selected_vendor_item)
    # self.wait_for_timeout(5000)
    # get_vendor_name = self.page.locator("//text()[contains(., 'Vendor')]/following::strong[1]").text_content().first()
    # self.wait_to_load_element(self.order_locator)
    # agreement = fa.split(":")[-1].strip()
    # print(get_vendor_name)
    # return get_vendor_name

    # vendor_block = req.locator("xpath=ancestor::div[contains(.,'Vendor')]")
    # vendor_name = req.locator("xpath=ancestor::div[contains(@class, 'vendor')]//b").inner_text()
    # print(f"Vendor: {vendor_name}")
    # vendor_container = req.locator("xpath=ancestor::div[contains(.,'Vendor')][1]")
    # radio_button = vendor_container.locator("xpath=.//input[@type='radio']")
    # radio_button.click()

    # vendor_radio = self.page.locator(f"text={requisition_number}").nth(0).locator(
    #     "xpath=ancestor::div[contains(.,'Vendor')][1]//input[@type='radio']")
    # vendor_radio.click()
    #
    # # Use the first match to find the vendor container
    # first_match = requisition_matches.first
    # vendor_container = first_match.locator("xpath=ancestor::div[contains(@id, 'vendorContainer')]")
    #
    # # Extract vendor name
    # vendor_name_element = vendor_container.locator("xpath=.//preceding-sibling::div[contains(text(), 'Vendor')]")
    # vendor_name = vendor_name_element.inner_text().replace("Vendor :", "").strip()
    # print(f"Vendor name for requisition {requisition_number}: {vendor_name}")
    #
    # # Select the vendor radio button
    # radio_button = vendor_container.locator("input[type='radio']")
    # if radio_button.count() > 0:
    #     radio_button.first.check()
    #     print(f"Selected vendor radio button for: {vendor_name}")
    # else:
    #     print(f"No radio button found for vendor: {vendor_name}")

    def select_vendor_for_requisition_6(self, requisition_number: str):
        # Locate the requisition link by its text (partial match in case there are prefixes)
        requisition_locator = self.page.locator(f"a.item-requisition-link:has-text('{requisition_number}')")

        if requisition_locator.count() == 0:
            print(f"Requisition {requisition_number} not found in cart.")
            return

        # Print requisition number
        print(f"Found requisition: {requisition_number}")

        # Go up to the vendor container (based on your HTML screenshot, it's a parent div with id like vendorContainerXXX)
        vendor_container = requisition_locator.locator("xpath=ancestor::div[contains(@id, 'vendorContainer')]")

        # Extract vendor name
        vendor_name_element = vendor_container.first.locator(
            "xpath=.//preceding-sibling::div[contains(text(), 'Vendor')]")
        vendor_name = vendor_name_element.inner_text().replace("Vendor :", "").strip()
        print(f"Vendor name for requisition {requisition_number}: {vendor_name}")

        # Click vendor radio button within this container
        radio_button = vendor_container.locator("input[type='radio']")
        radio_button.check()

        print(f"Selected vendor radio button for vendor: {vendor_name}")

    def select_vendor_for_requisition_5(self, requisition_number: str):
        """Find requisition, print its number, vendor name, and select the vendor's radio button."""
        requisition_elements = self.requisition_locator
        count = requisition_elements.count()

        if count == 0:
            print("No requisitions found in the cart.")
            return False

        for i in range(count):
            req_text = requisition_elements.nth(i).text_content().strip()
            if requisition_number in req_text:
                print(f"Requisition found: {req_text}")

                # Get vendor container (parent section for the requisition)
                vendor_container = requisition_elements.nth(i).locator(
                    "xpath=ancestor::div[contains(@id, 'vendorContainer')]"
                )

                # Get vendor name text from the container
                vendor_name_element = vendor_container.locator(
                    "xpath=.//preceding-sibling::div[contains(text(),'Vendor')]")
                if vendor_name_element.count() == 0:
                    vendor_name_element = vendor_container.locator("xpath=.//*[contains(text(),'Vendor')]")

                vendor_name = vendor_name_element.nth(i).text_content().strip()
                print(f"Vendor Name: {vendor_name}")

                # Select vendor's radio button
                vendor_radio = vendor_container.locator("input[type='radio']")
                vendor_radio.check()
                print(f"Vendor radio button selected for {vendor_name}")
                return True

        print(f"Requisition {requisition_number} not found in the cart.")
        return False

    def select_vendor_for_requisition_2(self, requisition_number: str):
        """Find requisition and select its vendor."""
        requisition_elements = self.requisition_locator
        count = requisition_elements.count()

        if count == 0:
            print("No requisitions found in the cart.")
            return False

        for i in range(count):
            req_text = requisition_elements.nth(i).text_content().strip()
            if requisition_number in req_text:
                print(f"Requisition found: {req_text}")

                # Get vendor container
                vendor_container = requisition_elements.nth(i).locator(
                    "xpath=ancestor::div[contains(@id, 'vendorContainer')]"
                )
                # if requisition_number in vendor_container:
                # Get vendor name
                vendor_name = self.vendor_container.locator(
                    "xpath=preceding-sibling::div[contains(@class, 'vendor-name')] | .//*[contains(text(),'Vendor :')]").text_content().strip()
                print(f"Vendor Name: {vendor_name}")

                # Select vendor radio button
                self.selected_vendor_item = self.vendor_container.locator('input[id^="radio"]')
                self.selected_vendor_item.click()
                print(f"Vendor selected for requisition {req_text}")
                return True

        print(f"Requisition {requisition_number} not found in the cart.")
        return False

    # cart_page = ShoppingCart(page)
    # cart_page.select_vendor_for_requisition("REQ20250014472")

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
