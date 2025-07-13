# # this is an object of samplePage to automate, which contains all elements
# # and actions could be performed, like input, verify, etc.
# import re
# from utils.basic_actions import BasicActions
# from pages.procurement_home_page import ProcurementHomePage
# from playwright.sync_api import expect


# class CreateRequisitionPage(ProcurementHomePage, BasicActions):
#     def __init__(self, page):
#         super().__init__(page)
#         # write down all the elements here with locator format
#         self.proc_item_requisition_for_self = page.locator('input[type="radio"][id="self"]')
#         self.proc_item_requisition_for_other = page.locator('input[type="radio"][id="other"]')
#         self.proc_item_requisition_for_other_office = page.locator("#officeInfoDiv_arrow")

#         self.proc_item_project = page.locator('css=#projectInfoDiv_input')
#         self.proc_item_project_dropdown = page.locator('#projectInfoDiv_arrow')
#         self.proc_item_source_of_fund = page.locator('#sourceOfFundDiv_input') #page.locator('css=#sourceOfFundDiv_arrow')
#         self.proc_item_remarks = page.get_by_role("textbox", name="Max size of requisition remarks 300 characters")

#         self.proc_item_information = page.locator('css=#itemInfo')
#         self.proc_item_unit_measure = page.locator('css=#mUnitDiv_arrow')

#         self.proc_item_tor = page.locator('css=#itemSpecification')
#         self.proc_item_quantity = page.locator('css=#quantity')
#         self.proc_item_unit_price = page.locator('css=#unitPrice')

#         self.requisition_for_single_project = page.locator('input[type="radio"][id="singleProjectRadio"]')
#         self.requisition_for_multiple_project = page.locator('input[type="radio"][id="multiProjectRadio"]')
#         self.requisition_cost_quantity = page.locator('input[type="radio"][id="itemCostQuantity"]')
#         self.requisition_cost_amount = page.locator('input[type="radio"][id="itemCostAmount"]')

#         self.requisition_item_gl_code = page.locator('css=#glInfo_0Div_arrow')
#         self.requisition_item_qty_amount = page.get_by_role("textbox", name="amountQty_0")
#         self.requisition_item_remarks = page.get_by_placeholder("Max size of item remarks 500 characters")
#         # page.get_by_role("textbox", name="reqDetailsRemarks")

#         self.requisition_add_button = page.get_by_role("button", name=re.compile("Add to Grid", re.IGNORECASE))
#         # schedule elements
#         self.requisition_delivery_schedule = page.get_by_role("checkbox", name=re.compile("Same schedule", re.IGNORECASE))
#         self.requisition_delivery_date = page.locator('css=#defaultDeliveryDate')
#         self.requisition_delivery_location = page.locator('//select[@id="defaultDeliveryStoreId"]')

#         # save and submit elements
#         self.save_button = page.get_by_role("button", name=re.compile("save", re.IGNORECASE))
#         self.submit_button = page.get_by_role("button", name=re.compile("submit", re.IGNORECASE))
#         self.confirm_submit_button = page.locator('css=button[role="button"] span[class="ui-button-text"]')
#         # requisition number elements
#         self.requisition_message = page.get_by_text("Procurement Requisition", exact=True) #page.locator('//div[@class="message"]')



#     # methods to perform actions within the page
#     def set_requisition_for_HO_and_project(self, ho, project_name):
#         if ho:
#             self.proc_item_requisition_for_self.click()
#         else:
#             self.proc_item_requisition_for_other.click()
#             self.proc_item_requisition_for_other_office.click()
#             # Click on Chattagram(D00014) branch
#             self.page.get_by_text("171798692561Chattagram(DO0014)").click()
#         self.select_from_dropdown(self.proc_item_project_dropdown, project_name)


#     def set_requisition_information(self, source_of_fund, remarks):
#         self.select_option_from_dropdown(self.proc_item_source_of_fund, source_of_fund)
#         self.input_in_element(self.proc_item_remarks, remarks)


#     def set_requisition_details(self, item_information, item_measure_unit, quantity, unit_price):
#         self.input_in_element(self.proc_item_information, item_information)
#         self.press_button("Enter")
#         #expect(self.proc_item_unit_measure).to_be_visible()
#         self.select_from_dropdown(self.proc_item_unit_measure, item_measure_unit)
#         self.press_button("Enter")
#         self.input_in_element(self.proc_item_tor, 'More Glue')
#         # expect(self.proc_item_tor).to_have_text('Glue (any type of glue)')
#         self.input_in_element(self.proc_item_quantity, quantity)
#         # if self.requisition_cost_quantity.is_checked():
#         #     expect(self.requisition_item_qty_amount).to_have_text(quantity)
#         self.input_in_element(self.proc_item_unit_price, unit_price)
#         # if self.requisition_cost_amount.is_checked():
#         #     qty = self.proc_item_quantity.get_attribute("value")
#         #     expect(self.requisition_item_qty_amount).to_have_value(qty*unit_price)

#     def set_requisition_project_delivery_schedule(self, gl_code, delivery_date, delivery_location):
#         self.requisition_for_single_project.click()
#         self.select_from_dropdown(self.requisition_item_gl_code, gl_code)
#         self.input_in_element(self.requisition_item_remarks, "Deliver all Glues")
#         self.click_on_btn(self.requisition_delivery_schedule)
#         self.input_in_element(self.requisition_delivery_date, delivery_date)
#         self.select_from_list_by_value(self.requisition_delivery_location, delivery_location)


#     def add_item_to_grid(self):
#         self.click_on_btn(self.requisition_add_button)
#         self.page.wait_for_timeout(5000)


#     def save_requisition(self):
#         self.click_on_btn(self.save_button)


#     def track_requisition_number(self):
#         #self.wait_to_load_element(self.requisition_message)
#         self.requisition_message.wait_for(state="visible", timeout=10000)
#         val_text = self.requisition_message.text_content()
#         self.requisition_message.wait_for(state="hiddengit che", timeout=10000)
#         print("Requisition Info: " + val_text)

# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify, etc.
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class CreateRequisitionPage(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        self.proc_item_requisition_for_self = page.locator('input[type="radio"][id="self"]')
        self.proc_item_requisition_for_other = page.locator('input[type="radio"][id="other"]')
        self.proc_item_project = page.locator('css=#projectInfoDiv_input')
        self.proc_item_project_dropdown = page.locator('#projectInfoDiv_arrow')
        self.proc_item_source_of_fund = page.locator('css=#sourceOfFundDiv_arrow')
        self.proc_item_information = page.locator('css=#itemInfo')
        self.proc_item_unit_measure = page.locator('css=#mUnitDiv_arrow')

        self.proc_item_tor = page.locator('css=#itemSpecification')
        self.proc_item_quantity = page.locator('css=#quantity')
        self.proc_item_unit_price = page.locator('css=#unitPrice')

        self.requisition_for_single_project = page.locator('input[type="radio"][id="singleProjectRadio"]')
        self.requisition_for_multiple_project = page.locator('input[type="radio"][id="multiProjectRadio"]')
        self.requisition_cost_quantity = page.locator('input[type="radio"][id="itemCostQuantity"]')
        self.requisition_cost_amount = page.locator('input[type="radio"][id="itemCostAmount"]')

        self.requisition_item_gl_code = page.locator('css=#glInfo_0Div_arrow')
        self.requisition_item_qty_amount = page.get_by_role("textbox", name="amountQty_0")

        self.requisition_add_button = page.get_by_role("button", name=re.compile("Add to Grid", re.IGNORECASE))
        # schedule elements
        self.requisition_delivery_schedule = page.get_by_role("checkbox", name=re.compile("Same schedule", re.IGNORECASE))
        self.requisition_delivery_date = page.locator('css=#defaultDeliveryDate')
        self.requisition_delivery_location = page.locator('//select[@id="defaultDeliveryStoreId"]')

        # save and submit elements
        self.save_button = page.get_by_role("button", name=re.compile("save", re.IGNORECASE))
        self.submit_button = page.get_by_role("button", name=re.compile("submit", re.IGNORECASE))
        self.confirm_submit_button = page.locator('css=button[role="button"] span[class="ui-button-text"]')
        # requisition number elements
        self.requisition_message = page.locator('//div[@class="message"]')
        self.requisition_message_2 = page.locator('//div[@class="message"]')

        # jGrowl > div.jGrowl-notification.ui-state-highlight.ui-corner-all.success
        # jGrowl > div.jGrowl-notification.ui-state-highlight.ui-corner-all.success > div.message
        # < div
        #
        # class ="jGrowl-notification ui-state-highlight ui-corner-all success" style="display: block;" > < div class ="close" > × < / div > < div class ="header" > Procurement Requisition < / div > < div class ="message" > Requisition Saved As Draft Successfully Requisition Number: REQ20250004371 <
        #
        # / div > < / div >


    # methods to perform actions within the page
    def select_requisition_for_self(self):
        self.proc_item_requisition_for_self.click()

    def select_requisition_for_other(self):
        self.proc_item_requisition_for_other.click()

    def input_project_name(self, project_name):
        self.select_from_dropdown(self.proc_item_project_dropdown, project_name)

    def input_source_of_fund(self, source_of_fund):
        self.select_from_dropdown(self.proc_item_source_of_fund, source_of_fund)

    def input_item_information(self, item_information, item_measure_unit):
        self.input_in_element(self.proc_item_information, item_information)
        self.press_button("Enter")
        #expect(self.proc_item_unit_measure).to_be_visible()
        self.select_from_dropdown(self.proc_item_unit_measure, item_measure_unit)
        #self.press_button("Enter")
        self.input_in_element(self.proc_item_tor, 'More Glue')
        # expect(self.proc_item_tor).to_have_text('Glue (any type of glue)')

    def input_item_quantity(self, quantity):
        self.input_in_element(self.proc_item_quantity, quantity)
        # if self.requisition_cost_quantity.is_checked():
        #     expect(self.requisition_item_qty_amount).to_have_text(quantity)

    def input_item_unit_price(self, unit_price):
        self.input_in_element(self.proc_item_unit_price, unit_price)
        # if self.requisition_cost_amount.is_checked():
        #     qty = self.proc_item_quantity.get_attribute("value")
        #     expect(self.requisition_item_qty_amount).to_have_value(qty*unit_price)

    def set_delivery_schedule(self):
        self.click_on_btn(self.requisition_delivery_schedule)
        self.input_in_element(self.requisition_delivery_date, "05-06-2025")
        self.select_from_list_by_value(self.requisition_delivery_location, "Central Store")

    def set_requisition_details(self):
        self.requisition_for_single_project.click()
        self.select_from_dropdown(self.requisition_item_gl_code, "[5102010107-05] Remuneration")

    def add_item_to_grid(self):
        self.click_on_btn(self.requisition_add_button)
        self.page.wait_for_timeout(5000)

    def save_requisition(self):
        self.click_on_btn(self.save_button)

    def submit_requisition(self):
        self.click_on_btn(self.submit_button)
        self.page.wait_for_timeout(10000)

    def confirm_submit_requisition(self):
        self.wait_to_load_element(self.confirm_submit_button)
        self.click_on_btn(self.confirm_submit_button)

    def track_requisition_number(self):
        #self.wait_to_load_element(self.requisition_message)
        val_text = self.requisition_message_2.text_content()
        print("Requisition Info: " + val_text)
