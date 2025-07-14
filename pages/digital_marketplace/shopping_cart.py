# import urllib2 from BeautifulSoup import BeautifulSoup soup = BeautifulSoup(urllib2.urlopen("https://www.google.com")) print soup.title.string;
import re
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.home_page import HomePage
from playwright.sync_api import expect



class ShoppingCart(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # self.page = page
        self.vendorSelection = page.locator('#vendorContainer33')
        self.selectedVendorItem =page.locator('#radio33')
        # self.userHomePageItem_showAllCategories = page.locator('xpath=//*[contains(text(),"All Categories")]')
        self.selectCartPageTermsAndCondition = page.locator('input[id="termsofservice"]')
        self.selectCartPageCheckoutButton= page.locator('button[id="checkout"][type="submit"]')
    #     self.second_common_login_btn = page.locator("//button[@type='submit']")

    def select_vendor(self):
        self.click_on_btn(self.vendorSelection)
        self.click_on_btn(self.selectedVendorItem)
        self.click_on_btn(self.selectCartPageTermsAndCondition)
        self.click_on_btn(self.selectCartPageCheckoutButton)