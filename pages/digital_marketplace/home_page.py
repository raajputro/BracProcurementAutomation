from utils.basic_actionsdm import BasicActionsDM


class HomePage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # self    = page
        # write down all the elements here with locator format
        self.user_homepage_item_show_framework_agreement_list = page.locator(
            'xpath=//*[contains(text(),"All Framework Agreements")]')
        self.user_homepage_item_show_all_vendors = page.locator('xpath=//*[contains(text(),"All Vendors ")]')
        self.user_homepage_item_show_all_categories = page.locator('xpath=//*[contains(text(),"All Categories")]')

        # Locator: find the span with class "cart-label" and text "Shopping cart"
        self.shopping_cart1 = page.locator('a:has-text("Shopping cart")')
        # self.shopping_cart = page.locator('span.cart-label', has_text='Shopping cart')
        # self.user_homepage_item_show_shopping_cart_list = page.locator('/html/body/div[6]/div[2]/div[1]/div[2]/div[1]/ul/a/span[1]')

        # click username go to order list page
        self.click_username = page.locator('a[class="ico-account"]')

        # self.pendingApprovalOrders1 = page.locator("a[href='/customer/pendingApprovalOrders']", has_text="Pending Approval Orders")

    def click_shopping_cart(self):
        # self.shopping_cart1.click()
        self.click_on_btn(self.shopping_cart1)
        # def goto_shoppingcart(self):
        #     (self.click_on_btn(self.user_homepage_item_show_shopping_cart_list)
        # user_homepage_item_show_shopping_cart_list.click())

    def goto_order_list(self):
        self.click_on_btn(self.click_username)
        # self.click_on_btn(self.pendingApprovalOrders1)
        # self.wait_for_timeout(2000)