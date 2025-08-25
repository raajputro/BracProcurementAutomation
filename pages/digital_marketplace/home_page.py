from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class HomePage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # self    = page
        self.user_homepage_item_show_framework_agreement_list = page.locator(
            'xpath=//*[contains(text(),"All Framework Agreements")]')
        self.user_homepage_item_show_all_vendors = page.locator('xpath=//*[contains(text(),"All Vendors ")]')
        self.user_homepage_item_show_all_categories = page.locator('xpath=//*[contains(text(),"All Categories")]')

        # Locator: find the span with class "cart-label" and text "Shopping cart"
        self.shopping_cart = page.locator('a:has-text("Shopping cart")')

        # click username go to order list page
        self.click_username = page.locator('a[class="ico-account"]')
        self.admin_username = page.locator('a[href="/order/allhistory"]')

        self.administration_link = page.locator('a[href="/Admin"]')
        self.cart_quantity = page.locator('//*[@id="topcartlink"]/a/span[2]')

        self.view_details_for_active_requisition = page.locator('a[class="btn btn-success"]')

        self.pending_approval_orders = page.locator("a[href='/customer/pendingApprovalOrders']",
                                                    has_text="Pending Approval Orders")
        self.welcome_locator = page.locator("div.topic-block-title >> h2")

    def verify_welcome_message(self):
        # expect(self.welcome_locator).to_have_text("Welcome to BRAC Digital Marketplace")
        actual_text = self.welcome_locator.text_content().strip()
        print("Print digital marketplace welcoming message: " + actual_text)
        return actual_text

    def goto_pending_approval_orders_list(self):
        self.click_on_btn(self.pending_approval_orders)

    def goto_shopping_cart(self):
        self.click_on_btn(self.shopping_cart)

    def goto_all_orders_for_admin(self):
        self.click_on_btn(self.admin_username)
        self.wait_for_timeout(2000)

    def goto_order_list(self):
        self.click_on_btn(self.click_username)
        # self.wait_for_timeout(2000)

    def goto_administration(self):
        self.click_on_btn(self.administration_link)

    def go_to_active_requisition_list(self):
        self.click_on_btn(self.view_details_for_active_requisition)
        self.wait_for_timeout(5000)

    # Using for test purpose
    def get_cart_value(self):
        self.cart_quantity = page.locator('//*[@id="topcartlink"]/a/span[2]')
        value = self.cart_quantity.text_content()
        cart_value = value.strip('()')
        print("CartValue:", cart_value)
        self.wait_for_timeout(2500)
        print("hvcacdbdcnfgmhmgjmjmgm543645")
        self.wait_for_timeout(2500)
        print("hvcacdbdcnfgmhmgjmjmgm543645")
        self.wait_for_timeout(2500)
        return cart_value
