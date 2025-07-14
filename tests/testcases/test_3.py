# this page contains all the test cases for the samplePage
#from resources.resource_file import TestResources
from dotenv import load_dotenv
import os

load_dotenv()

proj_url = os.getenv("test_url")
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
proj_gen_pass = os.getenv("test_user_generic_pass")

# Page models
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.procurement_home_page import ProcurementHomePage
from pages.cr3_page import CreateReqPage
from pages.requisition_list import RequisitionList
from pages.main_navigation_bar import MainNavigationBar
from pages.requisition_approve_list import RequisitionApproveList

# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install
install()

req_num = ''
approver_id = ''
approver_id_2 = ''


def test_1_login_to_create_requisition(page):
    s_page  = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=proj_user,
        pass_word=proj_pass
    )


def test_2_go_to_procurement_page(page):
    d_page = DashboardPage(page)
    d_page.goto_procurement()
    d_page.get_full_page_screenshot('full_page_screenshot_1')


def test_3_navigate_to_create_req_from_prod_dashboard(page):
    p_page = ProcurementHomePage(page)
    p_page.navigate_to_create_requisition()
    p_page.get_full_page_screenshot('full_page_screenshot_2')
    p_page.wait_for_timeout(7500)


def test_4_create_and_submit_requisition(page):
    c_page = CreateReqPage(page)
    #c_page.validate()
    c_page.setting_requisition_for("[H04] - Procurement-BRAC")
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "Tor for Item","1000","25")
    c_page.setting_requisition_for_details("[5102010107-05] Remuneration","gl remarks","30-07-2025", "Head Office", "ABC Road")
    c_page.get_full_page_screenshot('full_page_screenshot_3')
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    c_page.get_full_page_screenshot('full_page_screenshot_4')


def test_5_find_approver_of_the_requisition(page):
    r_page = RequisitionList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/list")
    r_page.get_full_page_screenshot('full_page_screenshot_5')
    r_page.search_requisition(req_num)
    global approver_id
    approver_id = str(int(r_page.find_approver_id()))
    print("APPROVER ID:", approver_id)
    r_page.get_full_page_screenshot('full_page_screenshot_6')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_7')
    r2_page.wait_for_timeout(5000)


def test_6_login_as_approver_and_approve(page):
    s_page = LoginPage(page)
    s_page.perform_login(
        user_name=approver_id,
        pass_word=proj_gen_pass
    )

    r_page = RequisitionApproveList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
    r_page.get_full_page_screenshot('full_page_screenshot_8')
    r_page.search_requisition(req_num)
    r_page.select_requisition(req_num)
    r_page.approve_requisition()
    r_page.confirmation_message_approve()
    r_page.get_full_page_screenshot('full_page_screenshot_9')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_10')
    r2_page.wait_for_timeout(5000)

def test_7_find_approver_of_the_requisition_2(page):
    s_page  = LoginPage(page)
    s_page.perform_login(
        user_name=proj_user,
        pass_word=proj_pass
    )

    r_page = RequisitionList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/list")
    r_page.get_full_page_screenshot('full_page_screenshot_11')
    r_page.search_requisition(req_num)
    global approver_id_2
    approver_id_2 = str(int(r_page.find_approver_id()))
    print("APPROVER ID 2:", approver_id_2)
    r_page.get_full_page_screenshot('full_page_screenshot_12')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_13')
    r2_page.wait_for_timeout(5000)


def test_8_login_as_approver_and_approve_2(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=approver_id_2,
        pass_word=proj_gen_pass
    )

    r_page = RequisitionApproveList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
    r_page.get_full_page_screenshot('full_page_screenshot_14')
    r_page.search_requisition(req_num)
    r_page.select_requisition(req_num)
    r_page.approve_requisition()
    r_page.confirmation_message_approve()
    r_page.get_full_page_screenshot('full_page_screenshot_15')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_16')
    r2_page.wait_for_timeout(5000)


def test_9_check_requisition_approved(page):
    s_page  = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=proj_user,
        pass_word=proj_pass
    )

    r_page = RequisitionList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/list")
    r_page.get_full_page_screenshot('full_page_screenshot_17')
    r_page.search_requisition(req_num)
    r_page.get_full_page_screenshot('full_page_screenshot_18')
    req_status = r_page.find_requisition_status()
    print("REQ STATUS:", req_status)
    #expect(req_status).to_be_equal("Approved")

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_19')
    r2_page.wait_for_timeout(5000)