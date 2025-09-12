import re
from utils.basic_actions import BasicActions
from pages.procurement_home_page import ProcurementHomePage
from playwright.sync_api import expect


class PerticipateTenderList(BasicActions):

    def __init__(self, page):
        super().__init__(page)

        self.tender_EoI_search = page.locator("#tenderTitleSearch")
        self.tender_participation_menu = page.get_by_role("link", name="Tender Participation")
        self.participate_in_tender_link = page.get_by_role("link", name="Participate In Tender")
        self.save_and_next_button = page.locator('#savePrimary')

    
    def go_to_participate_in_tender(self):
        # Click on Tender Participation menu
        self.tender_participation_menu.click()
        self.page.wait_for_timeout(1000)  # Wait for submenu to expand

        # Click on Participate In Tender
        self.participate_in_tender_link.click()
        self.page.wait_for_timeout(2000)  # Wait for page/navigation if needed

    def search_tender_EoI(self, tender_num: str):
        self.tender_EoI_search.fill(tender_num)
        self.page.wait_for_timeout(2000)
        self.tender_EoI_search.press("Enter")
        self.page.wait_for_timeout(5000)

    def click_apply_button_for_tender(self, tender_number: str):
    # Locate the row that contains the tender number in one of the <td>s
        row = self.page.locator(f'tr:has(td:has-text("{tender_number}"))')
    # Ensure the row exists
        if row.count() == 0:
            raise Exception(f"Tender number '{tender_number}' not found on the page.")
        # Find the button in that row (text could be 'Apply' or 'Re-Apply')
        apply_button = row.locator('button:has-text("Apply")')
    # Ensure button exists
        if apply_button.count() == 0:
            raise Exception(f"'Apply' button not found for tender '{tender_number}'.")
    # Click the button
        apply_button.click()
        self.page.wait_for_timeout(5000)
        print(f"Clicked 'Apply' button for tender '{tender_number}'.")

    def fill_criteria_row(self,criteria_text: str, option: str, comment: str, file_path: str):
        row = self.page.locator(f'table#jqGridCompliance tr:has-text("{criteria_text}")')
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
        self.page.wait_for_timeout(2000)

    def fill_required_document_fields(self,document_name: str, comment: str, file_path: str):
        row = self.page.locator(f'table#tenderItemReqDocComGrid tr:has-text("{document_name}")')
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


    def selecting_item(self,item_name: str):
        row = self.page.locator(f'table#jqGridTenderItem tr:has-text("{item_name}")')
        self.page.wait_for_timeout(2000)
        # Checkbox
        checkbox = row.locator('input[type="checkbox"]')
        checkbox.scroll_into_view_if_needed()
        checkbox.check()
        self.page.wait_for_timeout(1000)


    def selecting_technical_button(self,item_name: str, radio_value: str, comment: str, file_path: str):
        row = self.page.locator(f'table#jqGridTenderItem tr:has-text("{item_name}")')
        # Technical Proposal Button
        technical_button = row.locator('button[title*="Technical Proposal/Offer"]')
        technical_button.scroll_into_view_if_needed()
        technical_button.click()
        self.page.wait_for_timeout(1000)

        ti_row = self.page.locator(f'tr.itemCriteriaRow:has-text("{item_name}")')
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

        technical_info_save_button = self.page.locator('#saveTechInfo')
        technical_info_save_button.scroll_into_view_if_needed()
        technical_info_save_button.click()
        self.page.wait_for_timeout(3000)

    def selecting_financial_button(self,item_name: str, currency: str, unit_cost: str):
        row = self.page.locator(f'table#jqGridTenderItem tr:has-text("{item_name}")')
        # Financial Proposal Button
        financial_button = row.locator('button[title*="Financial Proposal/Offer"]')
        financial_button.scroll_into_view_if_needed()
        financial_button.click()
        self.page.wait_for_timeout(1000)

        # Select currency from dropdown by label
        currency_dropdown = self.page.locator('select#foreignCurrency')
        currency_dropdown.select_option(label=currency)
        self.page.wait_for_timeout(1000)  # opt

        unit_cost_input = self.page.locator('input#unitCost')
        unit_cost_input.wait_for(state="visible", timeout=60000)
        # clear existing text if any
        unit_cost_input.click()
        # optional: unit_cost_input.fill("") or select all then backspace
        unit_cost_input.press("Control+A")  
        unit_cost_input.press("Backspace")
        # unit_cost_input.type(unit_cost)
        unit_cost_input.type(unit_cost, delay=100)

        self.page.wait_for_timeout(5000)  # allow subtotal to calculate

    #Get the calculated subtotal
        sub_total = self.page.locator('input#subTotalCost').input_value()
        print(f"Subtotal calculated: {sub_total}")
        self.page.wait_for_timeout(2000)

         # Click on Save button
        financial_info_save_button = self.page.locator('button#saveFinInfo')
        financial_info_save_button.scroll_into_view_if_needed()
        financial_info_save_button.click(timeout=60000)
        self.page.wait_for_timeout(3000)


    def click_on_submit(self):
        
        submit_button = self.page.locator("button#submit:has-text('Submit')")
    
        submit_button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(2000)
        submit_button.click()
        self.page.wait_for_timeout(5000)


