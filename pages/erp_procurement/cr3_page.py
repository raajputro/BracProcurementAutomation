from playwright.sync_api import expect
from utils.basic_actions import BasicActions
from pages.erp_procurement.procurement_home_page import ProcurementHomePage

class CreateReqPage(ProcurementHomePage, BasicActions):
    def __init__(self, page):
        super().__init__(page)

        # validating page has been redirected correctly
        self.validation_point = page.get_by_role("heading", name="Create Requisition")
        # elements for Requisition For?
        self.head_office_selector = page.locator("#self")
        self.project_name_dropdown_selector = page.locator("#projectInfoDiv_arrow")
        # elements for Requisition Information
        self.fund_source_selector = page.locator("#sourceOfFundDiv_input")
        self.fund_source_remarks_selector = page.locator("//*[@id='remarks']")
            #page.get_by_role("textbox", name="remarks").filter(has=page.get_by_placeholder("Max size of requisition remarks 300 characters"))
        # elements for requisition details
        self.item_info_selector = page.locator("//*[@id='itemInfo']")
        self.item_measure_box_selector = page.locator("#mUnitDiv_input")
        self.item_measure_selector = page.locator("#mUnitDiv_arrow")
        self.item_tor_selector = page.locator("//*[@id='itemSpecification']")
        self.item_qty_selector = page.locator("#quantity")
        self.item_unit_price_selector = page.locator("#unitPrice")
        # elements for requisition for
        self.single_project_selector = page.get_by_role('radio').get_by_text("Single Project")
        self.multi_project_selector = page.locator(f'#multiProjectRadio')

        self.gl_code_selector = page.locator("#glInfo_0Div_arrow")
        self.req_for_remarks_selector = page.locator("#reqDetailsRemarks")
        self.schedule_selector = page.get_by_role("checkbox", name="Same schedule")
        self.date_selector = page.locator("#defaultDeliveryDate")
        self.delivery_location_selector = page.locator("#defaultDeliveryStoreId")
        self.delivery_location_details_selector = page.locator("#defaultDeliveryPlace")
        self.add_to_grid_selector = page.get_by_role("button", name="Add to Grid")
        # element to save the requisition
        self.save_btn_selector = page.get_by_role("button", name="Save")
        self.submit_btn_selector = page.get_by_role("button", name="Submit")
        self.submit_confirmation_btn_selector = page.locator("//div[@role='dialog']//following::button")
        self.requisition_number = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')


    def validate(self):
        expect(self.validation_point).to_be_visible()


    def setting_requisition_for(self, project_name):
        self.head_office_selector.click()        # selecting Head Office
        self.project_name_dropdown_selector.click()     # clicking on project name drop down
        self.page.get_by_text(project_name).click()     # selecting given project name


    def setting_requisition_information(self, fund_source, fund_remarks):
        self.fund_source_selector.fill(fund_source)
        self.page.keyboard.press(" ")
        self.page.get_by_text(fund_source, exact=True).click()
        self.fund_source_remarks_selector.fill(fund_remarks)


    def setting_requisition_details(self, item_info_1, item_info_2, item_tor, measure_unit, qty, unit_price):
        self.item_info_selector.click()
        self.item_info_selector.fill(item_info_1)       # This info will search for item list
        self.page.keyboard.press(' ')
        self.wait_for_timeout(2500)
        self.page.get_by_text(item_info_2).click()      # This is to select EXACT item from the list
        
        if self.item_measure_box_selector.text_content() is None:
            self.item_measure_selector.click()
            self.page.locator(f'//*[@val="{measure_unit}"]').click()        
        
        if self.item_tor_selector.text_content() is None:
            self.item_tor_selector.fill(item_tor)
        
        self.item_qty_selector.fill(qty)
        self.item_unit_price_selector.fill(unit_price)


    def setting_requisition_for_details_for_single_project(self, gl_code, gl_remarks):
        self.gl_code_selector.click()
        self.page.get_by_text(gl_code).click()
        # self.req_for_remarks_selector.fill(gl_code)        

    
    def select_multi_project(self):
        self.multi_project_selector.click()
        self.wait_for_timeout(500)

    
    def set_multi_project_data(self, project_name, qty, gl_code, row_index=0,ref_code=None, area_code=None):
        print(f'Row Index: {row_index}')
        if row_index != 0:
            self.page.locator('//input[@type="button" and @value="Add"]').click()
            self.wait_for_timeout(500)

        # # Selecting Project Name
        self.select_from_input_dropdown(self.page.locator(f'#projectInfo_{row_index}Div_input'), project_name)
        # # Selecting GL Code
        self.select_from_input_dropdown(self.page.locator(f'#glInfo_{row_index}Div_input'), gl_code)
        # Selecting Ref Code
        if ref_code != None:
            self.select_from_input_dropdown(self.page.locator(f'#refCodeId_{row_index}Div_input'), ref_code)
        # Selecting Area Code
        if area_code != None:
            self.select_from_input_dropdown(self.page.locator(f'#deptInfo_{row_index}Div_input'), area_code)
            
        # Setting Quantity
        self.page.locator(f'#amountQty_{row_index}').fill(qty)
        self.wait_for_timeout(500)


    def schedule_selection(self, del_date, del_loc, del_loc_details):
        self.schedule_selector.click()
        self.date_selector.fill(del_date)
        self.delivery_location_selector.select_option(label=del_loc)
        self.delivery_location_details_selector.fill(del_loc_details)
        self.wait_for_timeout(5000)
        
    
    def add_requisition_to_grid(self):
        self.add_to_grid_selector.click()
        self.wait_for_timeout(5000)


    def save_requisition(self) -> str:        
        self.save_btn_selector.click()
        self.wait_to_load_element(self.requisition_number)
        value = self.requisition_number.text_content()
        #print(value)
        return value.split(' ')[-1]
        #print("Last Value: " + val[-1])


    def submit_requisition(self) -> str:        
        self.submit_btn_selector.click()
        self.wait_to_load_element(self.submit_confirmation_btn_selector)
        self.submit_confirmation_btn_selector.click()
        self.wait_to_load_element(self.requisition_number)
        value = self.requisition_number.text_content()
        self.print_important_toast(value)
        return value.split(' ')[-1]


    def select_from_input_dropdown(self, locator, value):
        locator.fill(value)
        self.page.keyboard.press(" ")
        self.page.get_by_text(value, exact=True).click()