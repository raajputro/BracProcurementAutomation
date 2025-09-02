
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class VendoParticipation(BasicActions):

    def __init__(self, page):
        super().__init__(page)

        self.save_and_next_button = page.locator('#savePrimary')
        
        

    def apply_in_tender(self, tender_num: str):

        apply_tender=self.page.locator("div.card", has_text=tender_num).get_by_role("button", name="Apply")
        self.page.wait_for_timeout(5000)
        apply_tender.scroll_into_view_if_needed()   
        apply_tender.click()
        self.page.wait_for_timeout(5000)


    def fill_criteria_row(self, page, criteria_text: str, option: str, comment: str, file_path: str):
        row = page.locator(f'table#jqGridCompliance tr:has-text("{criteria_text}")')

        # Select radio
        # option = option.capitalize()
        radio = row.locator(f'input[type="radio"][value="{option}"]')
        radio.check()
        self.page.wait_for_timeout(2000)

        # Fill comment
        remarks = row.locator('textarea[placeholder*="Enter Comments"]')
        remarks.fill(comment)
        self.page.wait_for_timeout(2000)

        # Upload file
        complianc_document = row.locator('input[type="file"]')
        complianc_document.set_input_files(file_path)
        # complianc_document=row.locator('input[type="file"]')
        # uploaded_file_name = self.upload_file(complianc_document,file_path)
        # print(f"Uploaded file name: {uploaded_file_name}")
        self.page.wait_for_timeout(2000)

    def fill_required_document_fields(self, page, document_name: str, comment: str, file_path: str):
        row = page.locator(f'table#tenderItemReqDocComGrid tr:has-text("{document_name}")')
        self.page.wait_for_timeout(2000)
        remarks_field = row.locator('textarea')
        remarks_field.fill(comment)
        self.page.wait_for_timeout(2000)

        document_upload = row.locator('input[type="file"]')
        document_upload.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

    def click_on_save_and_next(self):
        self.save_and_next_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(2000)
        self.save_and_next_button.click()
        self.page.wait_for_timeout(5000)

    def fill_tender_item_fields(self, page, item_name: str, radio_value: str, comment: str, file_path: str, currency: str, unit_cost: str):
        row = page.locator(f'table#jqGridTenderItem tr:has-text("{item_name}")')
        self.page.wait_for_timeout(2000)

        # Checkbox
        checkbox = row.locator('input[type="checkbox"]')
        checkbox.scroll_into_view_if_needed()
        checkbox.check()
        self.page.wait_for_timeout(1000)

        # Technical Proposal Button
        technical_button = row.locator('button[title="Add Technical Proposal/Offer"]')
        technical_button.scroll_into_view_if_needed()
        technical_button.click()
        self.page.wait_for_timeout(1000)

        ti_row = page.locator(f'tr.itemCriteriaRow:has-text("{item_name}")')
        self.page.wait_for_timeout(2000)
           # Select the radio button dynamically
        radio_button = ti_row.locator(f'input[type="radio"][value="{radio_value}"]')
        radio_button.scroll_into_view_if_needed()
        radio_button.check()
        self.page.wait_for_timeout(1000)

    # Fill the comment field
        comment_field = ti_row.locator('textarea[id^="comment_"]')
        comment_field.fill(comment)
        self.page.wait_for_timeout(1000)

    # Upload the document
        file_input = ti_row.locator('input[type="file"]')
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        technical_info_save_button = page.locator('button#saveTechInfo:has-text("Save")')
        technical_info_save_button.scroll_into_view_if_needed()
        technical_info_save_button.click()
        self.page.wait_for_timeout(3000)

    # Financial Proposal Button
        financial_button = row.locator('button[title="Add Financial Proposal/Offer"]')
        financial_button.scroll_into_view_if_needed()
        financial_button.click()
        self.page.wait_for_timeout(1000)

        # Select currency from dropdown by label
        currency_dropdown = page.locator('select#foreignCurrency')
        currency_dropdown.select_option(label=currency)
        page.wait_for_timeout(1000)  # opt

        unit_cost_input = page.locator('input#unitCost')
        unit_cost_input.fill(unit_cost)
        page.wait_for_timeout(1000)  # allow subtotal to calculate

    #Get the calculated subtotal
        sub_total = page.locator('input#subTotalCost').input_value()
        print(f"Subtotal calculated: {sub_total}")

        financial_info_save_button = page.locator("button#saveFinInfo")
        financial_info_save_button.scroll_into_view_if_needed()
        financial_info_save_button.click()
        self.page.wait_for_timeout(3000)

        submit_button = page.locator("button#submit")
        submit_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(2000)
        submit_button.click()
        self.page.wait_for_timeout(5000)

