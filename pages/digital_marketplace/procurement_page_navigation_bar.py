# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.

import re

from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class ProcurementPageNavigationBar(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format

        self.requisition = page.locator('//div[text()="Requisition"]')
        #under requisition
        self.create_requisition = page.get_by_role("link", name="Create Requisition")
        self.requisition_list = page.get_by_role("link", name="Requisition List")
        self.requisition_approval_list = page.get_by_role("link", name="Requisition Approve List")
        self.requisition_assign= page.locator("#wrapper").get_by_text("Requisition Assign", exact=True) #will show assign unassign and others options
        #under requisition assign
        self.requisition_accept_list= page.get_by_role("link", name="Requisition Accept List")
        self.assign_requisition = page.get_by_role("link", name="Assign Requisition", exact=True)
        self.unassign_requisition = page.get_by_role("link", name="Unassign Requisition")

        self.procurement_process = page.locator("#wrapper").get_by_text("Procurement Process", exact=True)
        #under procurement process
        self.create_tender_initiation = page.get_by_role("link", name="Create Tender Initiation")
        self.tender_initiation_list = page.get_by_role("link", name="Tender Initiation List")

        self.purchase_order =  page.locator('//div[text()="Purchase Order"]')
        #under purchase order
        self.direct_purchase = page.locator("div").filter(has_text=re.compile(r"^Direct Purchase$")).locator("span")

        #under direct purchase
        self.create_direct_purchase = page.get_by_role("link", name="Create Direct Purchase")
        self.direct_purchase_list = page.get_by_role("link", name="Direct Purchase List")

        self.item_receive = page.locator("#wrapper").get_by_role("listitem").filter(has_text="Item Receive Item Receive").locator("div")
        #under item receive
        self.create_item_receive = page.locator("#wrapper").get_by_role("link", name="Item Receive", exact=True)
        self.item_receive_list = page.get_by_role("link", name="Item Receive List")

        self.bill_payable = page.locator("#wrapper").get_by_role("listitem").filter(has_text="Bill Payable Create Vendor").locator("div")
        #under bill payable
        self.create_vendor_bill_payable = page.get_by_role("link", name="Create Vendor Bill Payable")
        self.vendor_billing_list = page.get_by_role("link", name="Vendor Billing List")



    def click_requisition(self):
        self.requisition.wait_for(state="visible")
        self.requisition.click()
        self.requisition.wait_for(state="visible")

    def click_create_requisition(self):
        self.create_requisition.wait_for(state="visible")
        self.create_requisition.click()
        self.wait_for_timeout(1000)  
    
    def click_requisition_list(self):
        self.requisition_list.wait_for(state="visible")
        self.requisition_list.click()
        self.wait_for_timeout(1000)
    
    def click_requisition_approval_list(self):
        self.requisition_approval_list.wait_for(state="visible")
        self.requisition_approval_list.click()
        self.requisition_approval_list.wait_for(state="visible")
    
    def click_requisition_assign(self):
        self.requisition_assign.wait_for(state="visible")
        self.requisition_assign.click()
        self.requisition_assign.wait_for(state="visible")

    def click_assign_requisition(self):
        self.assign_requisition.wait_for(state="visible")
        self.assign_requisition.click()
        self.assign_requisition.wait_for(state="visible")

    def click_unassign_requisition(self):  
        self.unassign_requisition.wait_for(state="visible")
        self.unassign_requisition.click()
        
    def click_requisition_accept_list(self):
        self.requisition_accept_list.wait_for(state="visible")
        self.requisition_accept_list.click()
        self.wait_for_timeout(1000)
    
    def click_procurement_process(self):
        self.procurement_process.wait_for(state="visible")
        self.procurement_process.click()
        self.wait_for_timeout(1000)
    
    def click_create_tender_initiation(self):
        self.create_tender_initiation.wait_for(state="visible")
        self.create_tender_initiation.click()
        self.wait_for_timeout(1000)

    def click_tender_initiation_list(self):
        self.tender_initiation_list.wait_for(state="visible")
        self.tender_initiation_list.click()
        self.wait_for_timeout(1000)
    
    def click_purchase_order(self):
        self.purchase_order.wait_for(state="visible")
        self.purchase_order.click()
        self.wait_for_timeout(1000)
    
    def click_direct_purchase(self):
        self.direct_purchase.wait_for(state="visible")
        self.direct_purchase.click()
        self.wait_for_timeout(1000)

    def click_create_direct_purchase(self):
        self.create_direct_purchase.wait_for(state="visible")
        self.create_direct_purchase.click()
        self.wait_for_timeout(5000)

    def click_direct_purchase_list(self):
        self.direct_purchase_list.wait_for(state="visible")
        self.direct_purchase_list.click()
        self.wait_for_timeout(1000)

    def click_item_receive(self):
        self.item_receive.wait_for(state="visible")
        self.item_receive.click()
        self.wait_for_timeout(1000)
    
    def click_create_item_receive(self):
        self.create_item_receive.wait_for(state="visible")
        self.create_item_receive.click()
        self.wait_for_timeout(1000)

    def click_item_receive_list(self):
        self.item_receive_list.wait_for(state="visible")
        self.item_receive_list.click()
        self.wait_for_timeout(1000)

    def click_bill_payable(self):
        self.bill_payable.wait_for(state="visible")
        self.bill_payable.click()
        self.wait_for_timeout(1000)
    
    def click_create_vendor_bill_payable(self):
        self.create_vendor_bill_payable.wait_for(state="visible")
        self.create_vendor_bill_payable.click()
        self.wait_for_timeout(1000)

    def click_vendor_billing_list(self):
        self.vendor_billing_list.wait_for(state="visible")
        self.vendor_billing_list.click()
        self.wait_for_timeout(1000)
    



        
        
