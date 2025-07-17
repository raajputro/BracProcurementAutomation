# this is an object of samplePage to automate, which contains all elementsAdd commentMore actions
# and actions could be performed, like input, verify etc.
from utils.basic_actions import BasicActions


class AssignRequisition(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        self.assigned_to = page.locator("#employeeInfoDiv_input")
        self.requisition_search_box = page.locator("//div[@id='assignMultiSelectDiv']//child::input")
        self.assign_button = page.get_by_role("button", name="Assign")
        self.confirmation_message_assign = page.get_by_role("button", name="Yes")


    def assigning_person(self, assigned_person):
        self.input_in_element(self.assigned_to, assigned_person)
        self.page.keyboard.press(' ')
        self.page.wait_for_timeout(3000)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(1000)


    def add_item_to_assign(self, req_num):
        i = 0
        add_item = self.page.locator("//div[@id='tabs-1']//child::li[contains(text(),'" + req_num + "')][1]//following-sibling::a/span[@class='ui-corner-all ui-icon ui-icon-plus']")
        while add_item.is_visible():
            add_item.click()
            self.page.wait_for_timeout(5000)
            self.get_full_page_screenshot('item_added_for_assigning_' + str(i))
            i = i + 1


    def search_requisition_for_assigning(self, requisition_number):
        self.input_in_element(self.requisition_search_box, requisition_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)


    def assigning_items(self):
        self.assign_button.click()
        self.page.wait_for_timeout(2000)
        self.confirmation_message_assign.click()
        self.page.wait_for_timeout(2000)