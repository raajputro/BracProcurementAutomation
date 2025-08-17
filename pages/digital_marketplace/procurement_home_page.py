from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class ProcurementHomePage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.proc_item_requisition = page.locator('//div[text()="Requisition"]')
        self.proc_item_requisition_create_requisition = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Create Requisition"]')
        self.requisition_list = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition List"]')
        self.requisition_approve_list = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition Approve List"]')

    # write down all the necessary actions performed on this page as def
    def navigate_to_create_requisition(self):
        self.proc_item_requisition.click()
        # self.get_screen_shot("Selecting Requisition")
        self.proc_item_requisition_create_requisition.click()
        # self.get_screen_shot("Selecting Create Requisition")
        # self.page.wait_for_timeout(5000)
        # self.get_screen_shot("Create Requisition Page")
        # expect(self.page.get_by_role("heading", name="Create Requisition")).to_be_visible()

    def navigate_to_requisition_list(self):
        self.proc_item_requisition.click()
        self.requisition_list.click()
        self.wait_for_timeout(5000)

    def navigate_to_requisition_approve_list(self):
        self.proc_item_requisition.click()
        self.requisition_approve_list.click()
        self.wait_for_timeout(5000)
