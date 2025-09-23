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
requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"
requisition_approve_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/authorizationList"
requisition_assign_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignRequisitions"
requisition_accept_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignedRequisitionShowList"
tender_initiation_url = proj_url + "/procurementDashboard/myDashboard#!/methodSelection/show"
direct_purchase_url = proj_url + "/procurementDashboard/myDashboard#!/directPurchase/show"
direct_purchase_list_url = proj_url + "/procurementDashboard/myDashboard#!/directPurchase/list"
item_receive_url = proj_url + "/procurementDashboard/myDashboard#!/itemReceive/show"
vendor_bill_payable_url = proj_url + "/procurementDashboard/myDashboard#!/thirdPartyBillPayable/show"
bill_payable_url = proj_url + "/procurementDashboard/myDashboard#!/thirdPartyBillPayable/billList"

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
from pages.erp_procurement.cr3_page import CreateReqPage
from pages.erp_procurement.requisition_list import RequisitionList
from pages.erp_procurement.main_navigation_bar import MainNavigationBar
from pages.erp_procurement.requisition_approve_list import RequisitionApproveList
from pages.erp_procurement.assign_req import AssignRequisition
from pages.erp_procurement.requisition_accept_list import RequisitionAcceptList
from pages.erp_procurement.create_tender_initiation import CreateTenderInitiation
from pages.erp_procurement.create_direct_purchase import CreateDirectPurchase
from pages.erp_procurement.direct_purchase_list import DirectPurchaseList
from pages.erp_procurement.item_receive import ItemReceive
from pages.erp_procurement.create_vendor_bill_payable import CreateVendorBillPayable
from pages.erp_procurement.vendor_bill_payable_list import BillList
from pages.erp_procurement.bill_details_information import BillDetails

#======================================================================================================================
#======================================================================================================================
# # Global variables
req_num = 'REQ20250014967'
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
item1 = {
        'office_name': "[H04] - Procurement-BRAC",
        'fund': "BRAC Fund",
        'remarks': "Remarks for funding",
        'item_name': "Glue Stick (Fevi Stick)",
        'quantity': "1000",
        'unit': "25",
        "gl_code": "1202010501-01",
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


def test_3_create_and_submit_requisition(page):
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Create Requisition"]

    print("Test 4: Creating requisition...")
    c_page = CreateReqPage(page)
    c_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)

    #c_page.validate()
    c_page.setting_requisition_for(item1["office_name"])
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details(item_info_1="glue",item_info_2="[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", item_tor="Tor for Item",measure_unit="Pcs",qty="100",unit_price="19")
    c_page.select_multi_project()
    c_page.set_multi_project_data(row_index=0, project_name="[105]- BRAC Chicken", gl_code="[2101010201-12] Salary Allowance Payable", ref_code=None, area_code=None, qty="60")
    c_page.set_multi_project_data(row_index=1, project_name="[C04]- Administratiion", gl_code="[2101010602-01] Withholding VAT Payable (WVP)", ref_code=None, area_code=None, qty="40")
    c_page.add_requisition_to_grid()
    c_page.schedule_selection(del_date=c_page.select_date(20), del_loc="Head Office", del_loc_details="ABC Road")

    # c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture","gl remarks",c_page.select_date(20), "Head Office", "ABC Road")
    c_page.get_full_page_screenshot('full_page_screenshot_3')
    
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    c_page.get_full_page_screenshot('full_page_screenshot_4')
