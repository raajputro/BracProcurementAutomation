# this page contains all the test cases for the samplePage
# from resources.resource_file import TestResources
from dotenv import load_dotenv
import os
import random

from pages.digital_marketplace.procurement_login_age import ProcurementLoginPage

load_dotenv()

proc_url = os.getenv("test_url")
proc_user = os.getenv("test_user_name")
proc_pass = os.getenv("test_user_pass")
agreement = os.getenv("test_white_listed_agreement")
proj_gen_pass = os.getenv("test_user_generic_pass")
admin_user = os.getenv("test_admin")
assigned_person = os.getenv("test_requisition_assignee")
vendor_name = os.getenv("test_vendor_name")
dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")

# Page models
from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.dashboard_page import DashboardPage
from pages.digital_marketplace.procurement_home_page import ProcurementHomePage
from pages.digital_marketplace.cr3_page import CreateReqPage
from pages.digital_marketplace.requisition_list import RequisitionList
from pages.digital_marketplace.main_navigation_bar import MainNavigationBar
from pages.digital_marketplace.requisition_approve_list import RequisitionApproveList
# from pages.assign_req import AssignRequisition
# from pages.requisition_accept_list import RequisitionAcceptList
# from pages.create_tender_initiation import CreateTenderInitiation
# from pages.create_direct_purchase import CreateDirectPurchase
# from pages.direct_purchase_list import DirectPurchaseList
# from pages.item_receive import ItemReceive
# from pages.create_vendor_bill_payable import CreateVendorBillPayable


# For validation

# Import for beautiful reporting
from rich.traceback import install

install()

req_num = ''
approver_id = ''
approver_id_2 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
bill_num = str(random.randint(10000, 99999))


def test_1_login_to_create_requisition(page):
    s_page = ProcurementLoginPage(page)
    s_page.navigate_to_url(proc_url)
    s_page.perform_login(
        user_name=proc_user,
        pass_word=proc_pass
    )


def test_2_go_to_procurement_page(page):
    d_page = DashboardPage(page)
    d_page.goto_procurement()
    d_page.get_full_page_screenshot('full_page_screenshot_1')


def test_3_navigate_to_create_req_from_prod_dashboard(page):
    p_page = ProcurementHomePage(page)
    p_page.navigate_to_create_requisition()
    p_page.get_full_page_screenshot('full_page_screenshot_2')
    p_page.wait_for_timeout(5000)


def test_4_create_and_submit_requisition(page):
    c_page = CreateReqPage(page)
    # c_page.validate()
    c_page.setting_requisition_for("[H10] - Construction")
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    # c_page.setting_requisition_details()
    c_page.fill_item_information_1()
    c_page.fill_agreement_information()
    c_page.finalize_agreement_item_and_quantity()
    c_page.setting_requisition_for_details()
    c_page.setting_same_schedule_for_date()
    # c_page.setting_same_schedule_for_location("Head Office")
    c_page.setting_same_schedule_for_location()
    c_page.get_full_page_screenshot('3. Requisition details view beofore saving or submitting')
    global req_num
    # req_num = c_page.setting_save_requisition()
    # print("Requisition Number:", req_num)
    # c_page.get_full_page_screenshot('full_page_screenshot_4')

    req_num = c_page.submit_requisition()
    print("Requisition Number:", req_num)
    c_page.get_full_page_screenshot('full_page_screenshot_4')
