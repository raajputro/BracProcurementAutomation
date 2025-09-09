import re
from utils.basic_actions import BasicActions

class PurchaseOrderDetailsInformation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.approve_button = page.locator('#approve')
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')

    def approve_work_order(self):
        """
        Approve the bill.
        """
        self.approve_button.wait_for(state='visible', timeout=10000)
        self.approve_button.scroll_into_view_if_needed()
        self.approve_button.click()
        toast_msg = self.toast_msg.text_content()
        self.print_important_toast(toast_msg)
        self.page.wait_for_timeout(2000)        