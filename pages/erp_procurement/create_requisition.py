from playwright.sync_api import expect
from utils.basic_actions import BasicActions

class CreateRequisitionPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)

        # validating page has been redirected correctly
        self.validation_point = page.get_by_role("heading", name="Create Requisition")

        # elements for Requisition For?
        self.head_office_selector = page.locator("#self")
        self.other_office_selector = page.locator("#other")
        self.project_name_selector = page.locator("#projectInfoDiv_input")
        self.office_name_selector = page.locator("#officeInfoDiv_input")
        self.office_input = page.locator('input#officeName')
        self.office_type_input = page.locator('input#officeTypeName')
        self.office_info_input = page.locator('input#officeName')
        self.program_input = page.locator('input#countryProgramInfoName')
        self.project_end_date_input = page.locator('input#projectEndDate')
        self.department_input = page.locator('input#departmentInfoName')

        # elements for Requisition Information
        self.fund_source_selector = page.locator("#sourceOfFundDiv_input")
        self.fund_source_remarks_selector = page.locator("//*[@id='remarks']")


        # elements for requisition for
        self.item_info_selector = page.locator("//*[@id='itemInfo']")
        self.item_measure_selector = page.locator("#mUnitDiv_arrow")
        self.item_tor_selector = page.locator("//*[@id='itemSpecification']")
        self.item_qty_selector = page.locator("#quantity")
        self.item_unit_price_selector = page.locator("#unitPrice")
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


    def validate_create_requisition_heading(self):
        """
        Validates if the 'Create Requisition' heading is visible on the page.
        """
        self.validate_heading(self.validation_point, "Create Requisition")


    def setting_requisition_for_HO(self, project_name):
        """
        Sets Requisition For as Head Office, selects a project, and prints auto-filled values:
        Office Info, Office Type, Program, Project End Date and Department.
        """  
        self.select_radio_button(self.head_office_selector, "Requisition For - Head Office")
        self.read_auto_filled_input(self.office_type_input, "Office Type")
        self.select_option_from_dropdown(self.project_name_selector, project_name, "Project Name")
        self.read_auto_filled_input(self.office_input, "Office Info")
        self.read_auto_filled_input(self.program_input, "Program")
        self.read_auto_filled_input(self.project_end_date_input, "Project End Date")
        self.read_auto_filled_input(self.department_input, "Department")

    def setting_requisition_for_OO(self, office_name, project_name):
        """
        Sets Requisition For as Other Office, selects a project and office, and prints auto-filled values:
        Office Info, Office Type, Program, Project End Date, and Department.
        """
        self.select_radio_button(self.other_office_selector, "Requisition For - Other Office")
        self.select_option_from_dropdown(self.office_name_selector, office_name, "Office Name")
        self.read_auto_filled_input(self.office_info_input, "Office Info")
        self.read_auto_filled_input(self.office_type_input, "Office Type")
        self.select_option_from_dropdown(self.project_name_selector, project_name, "Project Name")
        self.read_auto_filled_input(self.program_input, "Program")
        self.read_auto_filled_input(self.project_end_date_input, "Project End Date")
        self.read_auto_filled_input(self.department_input, "Department")
        
        



    def set_requisition_for(self, requisition_type, project_name, office_name=None):
        """
        Handles both Head Office (HO) and Other Office (OO) requisition setup.

        Sequence:
            ➡ Head Office:
                1️⃣ Select HO radio button
                2️⃣ Read auto-filled Office Info, Office Type
                3️⃣ Select Project
                4️⃣ Read auto-filled Program, Project End Date, Department

            ➡ Other Office:
                1️⃣ Select OO radio button
                2️⃣ Select Office
                3️⃣ Read auto-filled Office Info, Office Type
                4️⃣ Select Project
                5️⃣ Read auto-filled Program, Project End Date, Department
        """

        # --- Select requisition type ---    
        if requisition_type == "HO":
            self.select_radio_button(self.head_office_selector, "Requisition For - Head Office")
        elif requisition_type == "OO":
            self.select_radio_button(self.other_office_selector, "Requisition For - Other Office")
        else:
            print(f"❌ Invalid requisition type: '{requisition_type}'. Must be 'HO' or 'OO'.")
            return

        # --- Handle office selection for OO only ---
        if requisition_type == "OO":
            self.select_option_from_dropdown(self.office_name_selector, office_name, "Office Name")

        # --- Common auto-filled fields before project selection ---
        self.read_auto_filled_input(self.office_info_input, "Office Info")
        self.read_auto_filled_input(self.office_type_input, "Office Type")

        # --- Select project ---
        self.select_option_from_dropdown(self.project_name_selector, project_name, "Project Name")

        # --- Auto-filled fields after project selection ---
        self.read_auto_filled_input(self.program_input, "Program")
        self.read_auto_filled_input(self.project_end_date_input, "Project End Date")
        self.read_auto_filled_input(self.department_input, "Department")

        print(f"✅ Requisition setup completed successfully for {requisition_type}.\n")

    def set_requisition_information(self, source_of_fund, remarks):
        """
        1️⃣ Select Source of Fund from dropdown
        2️⃣ Enter Remarks text
        
        """
        self.select_option_from_dropdown(self.fund_source_selector, source_of_fund, "Source of Fund")
        self.input_in_element(self.fund_source_remarks_selector, remarks, "Remarks")



            
