import re
from utils.basic_actions import BasicActions

class TenderDetails(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.tender_details_page_approve = page.locator("#approve")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')
        
    def approve_tender_from_details_page(self):
        # Click the approve button on the direct purchase details page
        self.page.mouse.wheel(0, 5000)  # Scrolls down by 5000px
        self.page.wait_for_timeout(1000)

        self.tender_details_page_approve.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        self.tender_details_page_approve.click()
        toast_msg_text = self.toast_msg.text_content()
        self.print_important_toast(toast_msg_text)
        self.page.wait_for_timeout(5000)