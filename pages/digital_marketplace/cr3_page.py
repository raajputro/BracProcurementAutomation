import re
from operator import index

from playwright.sync_api import expect
from utils.basic_actionsdm import BasicActionsDM
from pages.digital_marketplace.procurement_home_page import ProcurementHomePage
import datetime


class CreateReqPage(ProcurementHomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)

        # validating page has been redirected correctly
        self.validation_point = page.get_by_role("heading", name="Create Requisition")

        # elements for Requisition For?
        self.head_office_selector = page.locator("#self")
        self.project_name_dropdown_selector = page.locator("#projectInfoDiv_arrow")

        # project for construction
        self.selected_project_name = page.locator('//*[@id="projectInfoDiv_hidden"]')

        # elements for Requisition Information
        self.fund_source_selector = page.locator("#sourceOfFundDiv_input")
        self.fund_source_remarks_selector = page.locator("//*[@id='remarks']")
        self.fund_source_dropdown_selector = page.locator('#sourceOfFundDiv_arrow')
        self.fund_container = page.locator('#sourceOfFundDiv_ctr')

        # elements for requisition details
        self.item_info_selector = page.locator("//*[@id='itemInfo']")
        self.item_info = page.locator("//a[@id='ui-active-menuitem' and contains(text(), 'Pen Box')]")
        self.item_info_for_active = page.locator(
            "/html/body/div[2]/div[2]/div/div[1]/div[1]/form[1]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/ul/li/a")
        self.item_measure_selector = page.locator("#mUnitDiv_arrow")
        self.item_tor_selector = page.locator("//*[@id='itemSpecification']")
        self.item_qty_selector = page.locator("#quantity")
        self.item_unit_price_selector = page.locator("#unitPrice")

        # all active framework agreement locator
        self.active_agreement_button = page.locator('#check-agreement-button')
        self.fa_agreement_input = page.locator('input#faAgreementNo')
        self.finalize_dropdown_agreement = page.locator("ul.ui-autocomplete li.ui-menu-item a",
                                                        has_text="BPD/2024/FA-93")
        self.find_button = page.locator('//*[@id="find-button-requisitionList"]')

        # Item selection
        self.item_1 = page.locator('tr[id="206158470471"]')
        self.item_2 = page.locator('tr[id="206158470472"]')
        self.item_3 = page.locator('tr[id="206158470473"]')
        self.item_4 = page.locator('tr[id="206158470474"]')
        self.item_5 = page.locator('tr[id="206158470475"]')
        self.item_6 = page.locator('tr[id="206158470476"]')

        # elements for requisition for
        self.gl_code_dropdown = page.locator("#glInfo_0Div_arrow")
        self.selected_gl_code = page.locator('//*[@id="glInfo_0Div"]')
        self.gl_info_hidden_input = page.locator("input[id='glInfo_0Div_hidden'][value='1202010501-01]']")
        self.gl_input = page.locator("#glInfo_0Div_input")
        self.dropdown_option = page.locator("div#glInfo_0Div_ctr div.row.ffb-sel", has_text="1202010501-01")
        self.gl_code = page.locator("div.row", has_text="[1202010501-01] Furniture and Fixture")
        self.ref_code_dropdown = page.locator("#refCodeId_0Div_arrow")
        self.ref_code_input = page.locator("#refCodeId_0Div_input")
        self.req_for_remarks_selector = page.locator("#reqDetailsRemarks")
        self.add_to_grid_button = page.locator("input#addToGrid")

        # Same schedule selector
        self.select_same_schedule = page.locator('//*[@id="useDefault"]')
        self.date_picker_icon = page.locator("img.ui-datepicker-trigger")
        self.today = page.locator(".ui-datepicker-calendar .ui-state-highlight")
        self.delivery_store_select = page.locator("#defaultDeliveryStoreId")
        self.location_input = page.locator("#defaultDeliveryPlace")

        # element to save the requisition
        self.save_button = page.locator("#create-button-requisition")
        self.submit_button = page.locator("#submit2-button-requisition")
        self.submit_confirmation_button = page.locator("button:has-text('Submit')")

        self.submit_confirmation_btn_selector = page.locator("//div[@role='dialog']//following::button")
        self.requisition_number = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')
        # self.message_text = page.locator('//div[@class="jGrowl-notification"]//div[@class="message"]')

        self.date_picker_icon = page.locator('xpath=//*[@alt="Select date"]')

    def validate(self):
        expect(self.validation_point).to_be_visible()

    def setting_requisition_for(self, project_name):
        self.head_office_selector.click()  # selecting Head Office
        self.project_name_dropdown_selector.click()  # clicking on project name dropdown
        self.page.get_by_text(project_name).click()  # selecting given project name

    def setting_requisition_information(self, fund_source, fund_remarks):
        self.fund_source_selector.fill(fund_source)
        self.page.keyboard.press(" ")
        self.page.get_by_text(fund_source, exact=True).click()
        self.fund_source_remarks_selector.fill(fund_remarks)

    def fill_item_information_1(self):
        item_text = "[22245]-Pen Box-(Supplies and Stationeries->Supplies and Stationeries->Stationery)"
        self.click_on_btn(self.item_info_selector)
        # Type 'Pen Box' with delay
        for char in "Pen Box":
            self.item_info_selector.type(char)
            self.wait_for_timeout(200)
        # Wait for the dropdown and select the correct item
        dropdown_locator = self.page.locator(
            "//ul[contains(@class,'ui-autocomplete')]//a[normalize-space(text())='" + item_text + "']")
        expect(dropdown_locator).to_be_visible(timeout=5000)
        # Click the matching item
        dropdown_locator.click()
        self.wait_for_timeout(1000)

    def fill_agreement_information(self):
        # whitelisted_agreement = "BPD/2024/FA-93"
        self.click_on_btn(self.active_agreement_button)
        # Type 'agreement no.' with delay
        for char in "BPD/2024/FA-93":
            self.fa_agreement_input.type(char)
            self.wait_for_timeout(200)
        self.finalize_dropdown_agreement.click()
        self.find_button.click()
        self.wait_for_timeout(2000)

    # Globally call white listed agreement
    # def setting_white_listed_agreement_item(self, white_listed_agreement):
    #     self.active_agreement_button.click()
    #     white_listed_agreement1 = white_listed_agreement + " "
    #     self.input_in_element(self.fa_agreement_input, white_listed_agreement1)
    #     white_listed_agreement2 = white_listed_agreement1[:-2] + "3"
    #     self.input_in_element(self.fa_agreement_input, white_listed_agreement2)
    #     self.wait_for_timeout(5000)

    def finalize_agreement_item_and_quantity(self):
        self.item_1.click()
        self.item_qty_selector.fill("100")

    def setting_requisition_for_details(self):
        self.gl_code_dropdown.click()
        self.gl_input.click()
        # Type "202010501-01] Furniture and Fixture": with delay
        for char in "202010501-01]":
            self.gl_input.type(char)
            self.wait_for_timeout(200)
        self.gl_code.click()
        self.wait_for_timeout(2000)
        self.ref_code_dropdown.click()
        self.ref_code_input.fill("Ref code input")
        self.req_for_remarks_selector.fill("Item remarks 1")
        self.wait_for_timeout(5000)
        self.add_to_grid_button.click()
        self.wait_for_timeout(5000)

    def setting_same_schedule_for_date(self):
        # self.select_same_schedule().click()
        self.click_on_btn(self.select_same_schedule)
        self.click_on_btn(self.date_picker_icon)
        self.click_on_btn(self.today)
        self.wait_for_timeout(5000)

    def setting_same_schedule_for_location(self):
        self.delivery_store_select.click()
        self.wait_for_timeout(5000)
        self.page.select_option("#defaultDeliveryStoreId", value="1")
        # For central store and other delivery schedule
        # self.page.select_option("#defaultDeliveryStoreId", value="2")
        # self.page.select_option("#defaultDeliveryStoreId", value="-1")
        self.wait_for_timeout(2000)
        self.location_input.click()
        self.input_in_element(self.location_input, "Gulshan 1, Head Office, Dhaka - 1200")
        self.wait_for_timeout(2000)

    def setting_save_requisition(self) -> str:
        self.save_button.click()
        self.wait_to_load_element(self.requisition_number)
        value = self.requisition_number.text_content()
        print("Draft Requisition Number:" + value)
        return value.split(' ')[-1]
        # print("Last Value: " + val[-1])

    def submit_requisition(self) -> str:
        self.submit_button.click()
        self.wait_to_load_element(self.submit_confirmation_button)
        self.submit_confirmation_button.click()
        self.wait_to_load_element(self.requisition_number)
        value = self.requisition_number.text_content()
        return value.split(' ')[-1]

    # this is for non-agreement item
    def setting_requisition_details_for_master_item(self, item_info_1, item_info_2, item_tor, qty, unit_price):
        self.item_info_selector.click()
        self.item_info_selector.fill(item_info_1)
        self.page.keyboard.press(' ')
        self.wait_for_timeout(2500)
        self.page.get_by_text(item_info_2).click()
        self.item_measure_selector.click()
        self.page.locator('//*[@id="17"]').click()
        self.item_tor_selector.fill(item_tor)
        self.item_qty_selector.fill(qty)
        self.item_unit_price_selector.fill(unit_price)
