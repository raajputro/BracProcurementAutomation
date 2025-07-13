# this page contains all the test cases for the samplePage
#from resources.resource_file import TestResources
import os
from dotenv import load_dotenv
load_dotenv()

proj_url = os.getenv("test_url")
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")

# Page models
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.procurement_home_page import ProcurementHomePage
from pages.cr3_page import CreateReqPage
from pages.requisition_list import RequisitionList
from pages.main_navigation_bar import MainNavigationBar

# Import for beautiful reporting
from rich.traceback import install
install()

req_num = ''
approver_id = ''
approver_id2 = ''

def test_one(page):
    s_page  = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=proj_user,
        pass_word=proj_pass
    )


def test_two(page):
    d_page = DashboardPage(page)
    d_page.goto_procurement()
    d_page.get_full_page_screenshot('modular_test_2')


def test_three(page):
    p_page = ProcurementHomePage(page)
    p_page.navigate_to_create_requisition()
    p_page.get_full_page_screenshot('modular_test_3')
    p_page.wait_for_timeout(7500)


def test_four(page):
    c_page = CreateReqPage(page)
    c_page.validate()
    c_page.setting_requisition_for("[H04] - Procurement-BRAC")
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "Tor for Item","1000","25")
    c_page.setting_requisition_for_details("[5102010107-05] Remuneration","gl remarks","30-07-2025", "Head Office", "ABC Road")
    c_page.get_full_page_screenshot('full_page_screenshot_1')
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    c_page.get_full_page_screenshot('full_page_screenshot_2')


def test_six(page):
    r_page = RequisitionList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/list")
    r_page.get_full_page_screenshot('modular_test_7')
    global approver_id
    approver_id = str(int(r_page.search_requisition(req_num)))
    print("APPROVER ID:", approver_id)
    r_page.get_full_page_screenshot('modular_test_8')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('modular_test_9')


def test_seven(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=approver_id,
        pass_word="abc123$"
    )
    r_page = RequisitionList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/list")
    r_page.get_full_page_screenshot('modular_test_77')
    global approver_id2
    approver_id2 = str(int(r_page.search_requisition(req_num)))
    print("APPROVER ID2:", approver_id)
    r_page.get_full_page_screenshot('modular_test_88')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('modular_test_99')