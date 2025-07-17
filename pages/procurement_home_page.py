# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
from utils.basic_actions import BasicActions
from playwright.sync_api import expect


class ProcurementHomePage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.proc_item_requisition = page.locator('//div[text()="Requisition"]')
        self.proc_item_requisition_create_requisition = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Create Requisition"]')


    # write down all the necessary actions performed on this page as def
    def navigate_to_create_requisition(self):
        self.proc_item_requisition.click()
        #self.get_screen_shot("Selecting Requisition")
        self.proc_item_requisition_create_requisition.click()
        # self.get_screen_shot("Selecting Create Requisition")
        # self.page.wait_for_timeout(5000)
        # self.get_screen_shot("Create Requisition Page")
        #expect(self.page.get_by_role("heading", name="Create Requisition")).to_be_visible()


