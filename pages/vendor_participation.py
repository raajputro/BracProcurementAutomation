
import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class VendoParticipation(BasicActions):

    def __init__(self, page):
        super().__init__(page)
        
        

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