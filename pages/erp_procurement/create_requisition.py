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
        self.project_name_dropdown_selector = page.locator("#projectInfoDiv_arrow")
        self.office_name_dropdown_selector = page.locator("#officeInfoDiv_arrow")
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
        try:
            # Select Requisition For as Head Office
            expect(self.head_office_selector).to_be_visible(timeout=5000)
            self.head_office_selector.click()
            
            # Get Office Info
            office_value = self.office_input.input_value()
            print(f"Office Info is auto-filled with: '{office_value}'")

            # Get Office Type
            office_type_value = self.office_type_input.input_value()
            print(f"Office Type is auto-filled with: '{office_type_value}'")

            # Select project from dropdown
            expect(self.project_name_dropdown_selector).to_be_visible(timeout=5000)
            self.project_name_dropdown_selector.click()
            # Wait for project text to be visible and click
            project_option = self.page.get_by_text(project_name)
            expect(project_option).to_be_visible(timeout=5000)
            project_option.click()

            # Get Program
            program_value = self.program_input.input_value()
            print(f"Program is auto-filled with: '{program_value}'")

            # Get Project End Date
            project_end_date_value = self.project_end_date_input.input_value()
            print(f"Project End Date is auto-filled with: '{project_end_date_value}'")

            # Get Department
            Department_value = self.department_input.input_value()
            print(f"Department is auto-filled with: '{Department_value}'")

        except TimeoutError as te:
            print(f"❌ Timeout Error: Element not found or not visible. Details: {te}")
        except Exception as e:
            print(f"❌ Error while setting requisition for HO. Details: {e}")

        


    # def setting_requisition_for_OO(self, project_name, office_name):
    #     """
    #     Sets Requisition For as Other Office, selects a project and office, and prints auto-filled values:
    #     Office Info, Office Type, Program, Project End Date, and Department.
    #     """
    #     try:
    #         # Select Requisition For as Other Office
    #         expect(self.other_office_selector).to_be_visible(timeout=5000)
    #         self.other_office_selector.click()

    #         # Select office from dropdown
    #         # expect(self.officeInfoDiv_arrow).to_be_visible(timeout=5000)
    #         # self.officeInfoDiv_arrow.click()
    #         office_option = self.page.get_by_text(office_name)
    #         expect(office_option).to_be_visible(timeout=5000)
    #         office_option.click()

    #         # Get Office Info
    #         office_info_value = self.office_info_input.input_value()
    #         print(f"Office Info is auto-filled with: '{office_info_value}'")        

    #         # Get Office Type
    #         office_type_value = self.office_type_input.input_value()
    #         print(f"Office Type is auto-filled with: '{office_type_value}'")

    #         # Select project from dropdown
    #         expect(self.project_name_dropdown_selector).to_be_visible(timeout=5000)
    #         self.project_name_dropdown_selector.click()
    #         project_option = self.page.get_by_text(project_name)
    #         expect(project_option).to_be_visible(timeout=5000)
    #         project_option.click()

    #         # Get Program
    #         program_value = self.program_input.input_value()
    #         print(f"Program is auto-filled with: '{program_value}'")

    #         # Get Project End Date
    #         project_end_date_value = self.project_end_date_input.input_value()
    #         print(f"Project End Date is auto-filled with: '{project_end_date_value}'")

    #         # Get Department
    #         Department_value = self.department_input.input_value()
    #         print(f"Department is auto-filled with: '{Department_value}'")

    #     except TimeoutError as te:
    #         print(f"❌ Timeout Error: Element not found or not visible. Details: {te}")
    #     except Exception as e:
    #         print(f"❌ Error while setting requisition for Other Office. Details: {e}")

    def setting_requisition_for_OO(self, project_name, office_name):
        """
        Sets Requisition For as Other Office, selects a project and office, and prints auto-filled values:
        Office Info, Office Type, Program, Project End Date, and Department.
        """
        try:
            print("➡ Step 1: Selecting 'Other Office' option")
            expect(self.other_office_selector).to_be_visible(timeout=8000)
            self.other_office_selector.click()

            print(f"➡ Step 2: Selecting office '{office_name}' from dropdown")
            expect(self.office_name_dropdown_selector).to_be_visible(timeout=5000)
            self.office_name_dropdown_selector.click()
            office_option = self.page.get_by_text(office_name, exact=True)
            expect(office_option).to_be_visible(timeout=5000)
            office_option.click()

            # Fetch auto-filled Office Info and Office Type
            office_info_value = self.office_info_input.input_value()
            print(f"✅ Office Info is auto-filled with: '{office_info_value}'")

            office_type_value = self.office_type_input.input_value()
            print(f"✅ Office Type is auto-filled with: '{office_type_value}'")

            # Select Project
            print(f"➡ Step 3: Selecting project '{project_name}'")
            expect(self.project_name_dropdown_selector).to_be_visible(timeout=5000)
            self.project_name_dropdown_selector.click()

            project_option = self.page.get_by_text(project_name, exact=True)
            expect(project_option).to_be_visible(timeout=5000)
            project_option.click()

            # Fetch Program, Project End Date, and Department
            program_value = self.program_input.input_value()
            print(f"✅ Program is auto-filled with: '{program_value}'")

            project_end_date_value = self.project_end_date_input.input_value()
            print(f"✅ Project End Date is auto-filled with: '{project_end_date_value}'")

            department_value = self.department_input.input_value()
            print(f"✅ Department is auto-filled with: '{department_value}'")

            print("✅ Successfully set requisition for Other Office.")

        except TimeoutError as te:
            print(f"❌ Timeout Error: Element not found or not visible. Details: {te}")
            raise te   # <-- Important: stop test if key element not found
        except Exception as e:
            print(f"❌ Error while setting requisition for Other Office. Details: {e}")
            raise e  
        
    def set_requisition_information(self, source_of_fund, remarks):
        """
        Sets requisition information by selecting the Source of Fund
        and entering Remarks.
        """
        self.select_option_from_dropdown(self.fund_source_selector, source_of_fund, "Source of Fund")
        self.input_in_element(self.fund_source_remarks_selector, remarks, "Remarks")


            
