import re
from utils.basic_actions import BasicActions

class TenderDetails(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.tender_details_page_approve = page.locator("#approve")
        
    def approve_tender_from_details_page(self):
        # Click the approve button on the direct purchase details page
        self.page.mouse.wheel(0, 5000)  # Scrolls down by 5000px
        self.page.wait_for_timeout(1000)

        self.tender_details_page_approve.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        self.tender_details_page_approve.click()
        self.page.wait_for_timeout(5000)
 