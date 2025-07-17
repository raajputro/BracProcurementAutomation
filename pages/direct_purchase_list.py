import re
from typing import Self
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from resources.resource_file import TestResources
from playwright.sync_api import expect
from pages.create_direct_purchase import CreateDirectPurchase


class DirectPurchaseList(CreateDirectPurchase):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        cdp = CreateDirectPurchase(page)
        self.po_value_2 = cdp.po_value
        self.search_box = page.get_by_placeholder("Search Direct Purchase Order No")
        #self.check_box = page.locator("input[type='checkbox'].isUnderMyAuthority")
        self.approve= page.get_by_role("button", name=re.compile("Approve", re.IGNORECASE))
        # self.navigate_detail_direct_purchase = page.locator('a[style="text-decoration: underline;"]')
        self.confirmation_message_approve = page.locator('button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only', has_text="Approve")
        self.direct_purchase_details_page_approve=page.get_by_role("button", name=re.compile("approve-button", re.IGNORECASE))

    def search_purchase_order(self, purchase_order_number):
        self.search_box.scroll_into_view_if_needed()
        print("Searching for Purchase Order Number:", purchase_order_number)
        self.search_box.fill(purchase_order_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)
    
    def navigate_to_direct_purchase_detail_page(self, purchase_order_number):
        # Click on the direct purchase number link
        self.page.locator("//a[contains(text(),'"+purchase_order_number+"')]").click()
        self.page.wait_for_timeout(2000)

    def approve_direct_purchase_from_details_page(self):
        # Click the approve button on the direct purchase details page
        self.direct_purchase_details_page_approve.click()
        self.page.wait_for_timeout(2000)
 
        
    def select_direct_purchase_order(self, purchase_order_number):
        # Select the checkbox for the direct purchase order
        check_box = self.page.locator("//a[contains(text(),'"+purchase_order_number+"')]//parent::td//parent::tr//child::td/input[@type='checkbox']")
        check_box.click()
        #self.page.wait_for_timeout(1000)

    def approve_direct_purchase(self):
        # Click the approve button
        self.approve.click()
        self.page.wait_for_timeout(5000)

    def confirmation_message_approve(self):
        # Click the confirmation message approve button
        self.confirmation_message_approve.click()
        self.page.wait_for_timeout(2000)
       
