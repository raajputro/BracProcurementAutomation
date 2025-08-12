import re
from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


# from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class ActiveRequisitionProductList(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # self.product_history = page.locator('a[href*="requisitionProductId={product_id}"]')
        self.history_link = page.locator('a[href="/Requisition/History?requisitionProductId=2960"]')
        # Staging use
        # self.add_to_cart_button = page.locator('button[id="addToCartBtn-7323"]')
        self.add_to_cart_button = page.locator('button[id^="addToCartBtn-"]')

        self.close_button = page.locator('.close')
        self.shopping_cart = page.locator('a[class="ico-cart"]')

    def requisition_item_add_shopping_cart(self):
        self.click_on_btn(self.add_to_cart_button)
        # self.click_on_btn(self.close_button)

    def goto_shopping_cart(self):
        self.click_on_btn(self.shopping_cart)
        self.wait_for_timeout(5000)

    def view_product_switch_history(self):
        self.click_on_btn(self.history_link)
        self.wait_for_timeout(2000)

    # Finds the row with the given requisition ID in the Active Requisition List.
    # If the Total Budget equals the Remaining Budget, click the requisition link.
    def click_requisition_if_budget_matches(self, requisition_id: str):

        # requisition_id = "3449"
        # requisition_id = "1751'
        try:
            row = self.page.locator(
                'tr',
                has=self.page.locator(f'a[href*="requisitionId={requisition_id}"]')
            )

            if row.count() == 0:
                print(f"[ActiveRequisitionList] Row not found for requisitionId={requisition_id}")
                return False
            # strip means remove any leading and trailing whitespace characters (spaces,tabs,newlines)
            total_budget_text = row.locator('td').nth(3).text_content().strip()
            remaining_budget_text = row.locator('td').nth(4).text_content().strip()

            # 1,00,000.00 = 100000
            total_budget = float(total_budget_text.replace(",", ""))
            remaining_budget = float(remaining_budget_text.replace(",", ""))

            if total_budget == remaining_budget:
                print(f"[ActiveRequisitionList] Budgets match ({total_budget}) — clicking requisition link.")
                row.locator(f'a[href*="requisitionId={requisition_id}"]').click()
                self.wait_for_timeout(2000)
                return True

            else:
                print(
                    f"[ActiveRequisitionList] Budgets do NOT match: Total={total_budget}, Remaining={remaining_budget}")
                return False

        except Exception as e:
            print(f"[ActiveRequisitionList] Error occurred: {e}")
            return False

    # def click_history_for_product(self, product_id: str) -> bool:
    #     """
    #     Attempts to click the History link for the given product_id.
    #     Returns True if successful, False if not found.
    #     """
    #     locator = self.page.locator(
    #         f'a[href*="/Requisition/History?requisitionProductId={product_id}"]'
    #     )
    #
    #     try:
    #         # wait up to 3s for it to appear
    #         if locator.is_visible(timeout=3000):
    #             locator.click()
    #
    #             print(f"✅ Clicked History link for product_id={product_id}")
    #
    #             return True
    #         else:
    #             print(f"⚠️ History link for product_id={product_id} is not visible")
    #             return False
    #
    #     except PlaywrightTimeoutError:
    #         print(f"❌ History link for product_id={product_id} not found")
    #         return False

    # def click_history_for_product(self, product_id: str):
    #     """
    #     Finds the row with the given product_id in the product switch table.
    #     Clicks the History link if present.
    #     """
    #     try:
    #         # Find the <tr> that contains the product_id in the Add-to-cart button
    #         row = self.page.locator(
    #             'tr',
    #             has=self.page.locator(f'#addToCartBtn-{product_id}')
    #         )
    #
    #         if row.count() == 0:
    #             print(f"[ProductSwitchHistory] Row not found for product_id={product_id}")
    #             return False
    #
    #         history_link = row.locator(f'a[href*="/Requisition/History?requisitionProductId={product_id}"]')
    #
    #         if history_link.count() == 0:
    #             print(f"[ProductSwitchHistory] History link not found for product_id={product_id}")
    #             return False
    #
    #         print(f"[ProductSwitchHistory] Clicking History link for product_id={product_id}")
    #         history_link.click()
    #         self.wait_for_timeout(2000)
    #         # self.get_full_page_screenshot('switch')
    #         return True
    #     # first.
    #     except Exception as e:
    #         print(f"[ProductSwitchHistory] Error occurred: {e}")
    #         return False
