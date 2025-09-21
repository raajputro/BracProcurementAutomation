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
        self.history_link = page.locator('a[href^="/Requisition/History?requisitionProductId="]')
        # Staging use
        # self.add_to_cart_button = page.locator('button[id="addToCartBtn-7323"]')
        # self.add_to_cart_button = page.locator('button[id^="addToCartBtn-"]')
        self.add_to_cart_button = page.locator('button[type="button"][class="button-1 save-customer-info-button"]')

        self.close_button = page.locator('.close')
        self.shopping_cart = page.locator('a[class="ico-cart"]')

    def requisition_item_add_shopping_cart(self):
        self.click_on_btn(self.add_to_cart_button)

    def goto_shopping_cart(self):
        self.click_on_btn(self.shopping_cart)
        self.wait_for_timeout(5000)

    def view_product_switch_history(self):
        self.click_on_btn(self.history_link)
        self.wait_for_timeout(2000)

    # Finds the row with the given requisition ID in the Active Requisition List.
    # If the Total Budget equals the Remaining Budget, click the requisition link.
    def click_requisition_if_budget_matches(self, requisition_id: str):
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
