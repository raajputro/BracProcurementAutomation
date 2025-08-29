
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class VendoParticipation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        

    def apply_in_tender(self, tender_num: str):
        apply_tender=self.page.locator("div.card", has_text=tender_num).get_by_role("button", name="Apply")
        self.page.wait_for_timeout(5000)
        apply_tender.scroll_into_view_if_needed()   
        apply_tender.click()
        self.page.wait_for_timeout(5000)