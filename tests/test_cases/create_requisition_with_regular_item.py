# this page contains all the test cases for the samplePage
import os
import random

from conftest import new_tab

# For validation
# from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install
install()

from dotenv import load_dotenv
load_dotenv()

#======================================================================================================================
#======================================================================================================================
# Project URLs
proj_url = os.getenv("test_url")

#======================================================================================================================
# # Environment Data
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
proj_gen_pass = os.getenv("test_user_generic_pass")
admin_user = os.getenv("test_admin")
assigned_person = os.getenv("test_requisition_assignee")
vendor_name = os.getenv("test_vendor_name")
dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")


#======================================================================================================================
#======================================================================================================================
# Page models
from pages.erp_procurement.login_page import LoginPage
from pages.erp_procurement.dashboard_page import DashboardPage
from pages.erp_procurement.procurement_home_page import ProcurementHomePage
from pages.erp_procurement.create_requisition import CreateRequisitionPage

#======================================================================================================================
#======================================================================================================================
# # Global variables
req_num = ''
approver_id = ''
approver_id_2 = ''
approver_id_3 = ''
approver_id_4 = ''
bill_approver_id = ''
purchase_num = ''
challan_num = str(random.randint(10000,99999))
bill_num = str(random.randint(10000,99999))
bill_recommender1 = ''
bill_recommender2 = ''

#======================================================================================================================
#======================================================================================================================
# #User Data
RequisitionForInfo = {
        'office': "Dhaka(DO0015)",
        'project': "[H04] - Procurement-BRAC"
    }
RequisitionInformation = {
        'source_of_fund': "Dutch Embassyy",
        'remarks': "Creating requisition for regular item."
    }



#======================================================================================================================
#======================================================================================================================
# # ============================================ Test Cases onwards =============================================== # #
login_page_obj = None
def test_1_login_to_create_requisition(page):
    global login_page_obj
    login_page_obj = LoginPage(page)
    login_page_obj.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass
    )


def test_2_create_and_submit_requisition(page):

    """
    Test Case 1: Login to the ERP Procurement system and create & submit a requisition for white listed agreement item.

    Objective:
        To validate that a user can successfully log in to the ERP Procurement system,
        create a requisition using a whitelisted framework agreement item,
        provide all necessary requisition details, and submit it successfully —
        generating a unique requisition number for further processing.

    Steps:
        1. Login to the procurement portal using valid credentials.
        2. Navigate to the procurement dashboard.
        3. Capture a full-page screenshot for verification.
        4. Go to the "Create Requisition" page.
        5. Set up requisition details such as department, funding source, and remarks.
        6. Add items, select active framework agreements, and finalize quantities.
        7. Add scheduling and location details.
        8. Submit the requisition and record the generated requisition number.
        9. Navigate to the requisition list to confirm successful creation.
    """
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Create Requisition"]

    print("Test 4: Creating requisition...")
    c_page = CreateRequisitionPage(page)
    c_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    c_page.validate_create_requisition_heading()
    # c_page.setting_requisition_for_HO(RequisitionForInfo['project'])
    c_page.setting_requisition_for_OO(
        office_name=RequisitionForInfo['office'],
        project_name=RequisitionForInfo['project']
    )
    c_page.set_requisition_information(
        source_of_fund=RequisitionInformation['source_of_fund'],
        remarks=RequisitionInformation['remarks']
    )

