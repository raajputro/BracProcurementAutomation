import re

from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage

from playwright.sync_api import expect


class ActiveRequisitionListPage(HomePage, BasicActionsDM):
    # def __init__(self, driver):
    #     super(ActiveRequisitionListPage, self).__init__(driver)
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.order_requisition_number = page.locator('input[id="searchOrderInput"]')
        self.search_button = page.locator('button[class="button"]')

        self.requisition_hyperlink = page.locator(
            'a[href^="/Requisition/ActiveRequisitionProductList?requisitionId"]')
        # Need to change child id when using from table child = row
        # self.requisition_hyperlink = page.locator('.data-table > tbody:nth-child(2) > tr:nth-child(1)')
        self.add_to_cart_button = page.locator('button[id="addToCartBtn-7323"]')
        self.close_button = page.locator('.close')

    def search_order_requisition_number(self, requisition_number):
        self.input_in_element(self.order_requisition_number, requisition_number)
        self.search_button.click()

    def goto_active_requisition_product_list(self):
        self.click_on_btn(self.requisition_hyperlink)
        self.wait_for_timeout(2000)

    # Need change requisition id when requisition number will be changed
    def goto_active_requisition_product_list_stg(self):
        self.navigate_to_url(
            "https://stgmarketplace.brac.net/Requisition/ActiveRequisitionProductList?requisitionId=3568")


    def requisition_item_add_shopping_cart(self):
        self.click_on_btn(self.add_to_cart_button)
        self.wait_for_timeout(5000)
