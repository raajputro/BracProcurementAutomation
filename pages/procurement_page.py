# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
from utils.basic_actions import BasicActions
from playwright.sync_api import expect


class ProcurementPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.proc_item_requisition = page.locator('//div[text()="Requisition"]')
        self.proc_item_requisition_create_requisition = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Create Requisition"]')
        self.proc_item_requisition_Requisition_Initiator_List = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition Initiator List"]')
        self.proc_item_requisition_Requisition_List = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition List"]')
        self.proc_item_requisition_Requisition_Approve_List = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition Approve List"]')
        self.proc_item_requisition_Requisition_Assign = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition Assign"]')
        self.proc_item_requisition_Requisition_BPD_List = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Requisition BPD List"]')
        self.proc_item_requisition_Undo_Requisition_Review = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Undo Requisition Review"]')
        self.proc_item_requisition_Framework_Active_List = page.locator(
            '//div[text()="Requisition"]//following-sibling::ul//child::span[text()="Framework Active List"]')
        
    # write down all the necessary actions performed on this page as def
    def navigate_to_create_requisition(self):
        self.proc_item_requisition.click()
        #self.get_screen_shot("Selecting Requisition")
        self.proc_item_requisition_create_requisition.click()
        # self.get_screen_shot("Selecting Create Requisition")
        # self.page.wait_for_timeout(5000)
        # self.get_screen_shot("Create Requisition Page")
        expect(self.page.get_by_role("heading", name="Create Requisition")).to_be_visible()

