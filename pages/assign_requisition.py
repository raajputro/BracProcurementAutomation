# this is an object of samplePage to automate, which contains all elementsAdd commentMore actions
# and actions could be performed, like input, verify etc.
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect
from resources.resource_file import TestResources


class AssignRequisition(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # self.assigned_to = page.get_by_label("Assigned To")
        self.assigned_to = page.locator("#employeeInfoDiv_input")
        self.selecting_person = page.locator('#employeeInfoDiv_hidden')
        self.requisition_search_box = page.locator("//div[@id='assignMultiSelectDiv']//child::input")
        self.add_all=page.get_by_role("link", name="Add all")
        self.remove_all=page.get_by_role("link", name="Remove all")
        self.assign_button = page.get_by_role("button", name="Assign")
        self.confirmation_message_assign = page.get_by_role("button", name="Yes")
        self.locator_text_add_item = "//div[@id='tabs-1']//child::li[contains(text(),'"+TestResources.test_requisition_number+"')][1]//following-sibling::a/span[@class='ui-corner-all ui-icon ui-icon-plus']"
        self.add_item= page.locator(self.locator_text_add_item)
       


    def assigning_person(self, assigned_person):
        self.input_in_element(self.assigned_to, assigned_person)
        self.page.wait_for_timeout(5000)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000)
        # self.page.keyboard.press("Enter")
        # self.page.wait_for_timeout(1000)
    
    def add_item_to_assign(self):
        print("Elem Xpath = " + self.locator_text_add_item)
        i = 0
        while self.add_item.is_visible():
            print("Elem Visible")
            self.add_item.click()
            self.page.wait_for_timeout(5000)
            self.get_full_page_screenshot('item_added_for_assigning_' + str(i))
            i = i + 1

    def search_requisition_for_assigning(self, requisition_number):
        self.input_in_element(self.requisition_search_box, requisition_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)
        # self.assign_button.click()
        # self.page.wait_for_timeout(2000)
        # self.comfirmation_message_assign.click()
        # self.page.wait_for_timeout(2000)
        # #expect(self.page.locator("//div[@class='requisition_proposal_list']")).to_contain_text(requisition_number)

    def assigning_items(self):
        self.assign_button.click()
        self.page.wait_for_timeout(2000)
        self.confirmation_message_assign.click()
        self.page.wait_for_timeout(2000)