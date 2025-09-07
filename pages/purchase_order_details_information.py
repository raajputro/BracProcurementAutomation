import re
from utils.basic_actions import BasicActions

class PurchaseOrderDetailsInformation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.approve_button = page.locator('#approve')

    def approve_work_order(self):
        """
        Approve the bill.
        """
        self.approve_button.wait_for(state='visible', timeout=10000)
        self.approve_button.scroll_into_view_if_needed()
        self.approve_button.click()
        self.page.wait_for_timeout(2000)        