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

        self.purchase_order = page.locator('//div[text()="Purchase Order"]')
        self.framework_order = page.locator(
            '//div[text()="Purchase Order"]//following-sibling::ul//child::span[text()="Framework Order"]')
        self.framework_order_list = page.get_by_role("link", name="Framework Order List")

        self.item_receive = page.locator('//div[text()="Item Receive"]')
        self.item_receive_list = page.locator(
            '//div[text()="Item Receive"]//following-sibling::ul//child::span[text()="Item Receive List"]')

        self.bill_payable = page.locator('//div[text()="Bill Payable"]')
        self.create_vendor_bill_payable = page.locator(
            '//div[text()="Bill Payable"]//following-sibling::ul//child::span[text()="Create Vendor Bill Payable"]')
        self.vendor_billing_list = page.locator(
            '//div[text()="Bill Payable"]//following-sibling::ul//child::span[text()="Vendor Billing List"]')

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

    def navigate_to_framework_order_list(self):
        self.purchase_order.click()
        self.framework_order.click()
        self.framework_order_list.click()
        self.wait_for_timeout(5000)

    def goto_item_receive_list(self):
        self.item_receive.click()
        self.item_receive_list.click()
        self.wait_for_timeout(3000)

    def goto_bill_payable(self):
        self.bill_payable.click()
        self.create_vendor_bill_payable.click()

    def goto_vendor_billing_list(self):
        self.vendor_billing_list.click()
