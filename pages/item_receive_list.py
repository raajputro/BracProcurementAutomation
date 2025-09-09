from utils.basic_actions import BasicActions
from playwright.sync_api import expect


class ItemReceiveListPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format

        self.search_order = page.get_by_role("textbox", name="Search DP/FO/PO/CO Order No.")
        self.challan_no = page.locator("#challanNo")