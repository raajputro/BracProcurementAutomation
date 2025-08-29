import re
from utils.basic_actions import BasicActions

class TenderDetails(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        self.tender_details_page_approve = page.locator("#approve")
        


    def navigate_to_tender_detail_page(self, tender_number):
        # Click on the tender number link

        tender_details = self.page.locator("//a[contains(text(),'"+tender_number+"')]")
        tender_details.click()
        self.page.wait_for_timeout(5000)

    def approve_tender_from_details_page(self):
        # Click the approve button on the direct purchase details page
        self.tender_details_page_approve.click()
        self.page.wait_for_timeout(5000)
 