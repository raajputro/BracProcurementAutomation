# this page contains all the test cases for the samplePage
#from resources.resource_file import TestResources
from dotenv import load_dotenv
import os
import random

load_dotenv()

proj_url = os.getenv("test_url")
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
proj_gen_pass = os.getenv("test_user_generic_pass")
admin_user = os.getenv("test_admin")
assigned_person = os.getenv("test_requisition_assignee")
vendor_name = os.getenv("test_vendor_name")
dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")


# Page models
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.procurement_home_page import ProcurementHomePage
from pages.cr3_page import CreateReqPage
from pages.requisition_list import RequisitionList
from pages.main_navigation_bar import MainNavigationBar
from pages.requisition_approve_list import RequisitionApproveList
from pages.procurement_page_navigation_bar import ProcurementPageNavigationBar
from pages.assign_req import AssignRequisition
from pages.requisition_accept_list import RequisitionAcceptList
from pages.create_tender_initiation import CreateTenderInitiation
from pages.create_direct_purchase import CreateDirectPurchase
from pages.direct_purchase_list import DirectPurchaseList
from pages.item_receive import ItemReceive
from pages.create_vendor_bill_payable import CreateVendorBillPayable



# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install
install()

req_num = ''
approver_id = ''
approver_id_2 = ''
purchase_num = ''
challan_num = str(random.randint(10000,99999))
bill_num = str(random.randint(10000,99999))


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
    c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture","gl remarks","30-07-2025", "Head Office", "ABC Road")
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


def test_9_check_requisition_assign(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=admin_user,
        pass_word=proj_gen_pass
    )

    r_page = AssignRequisition(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/assignRequisitions")
    r_page.assigning_person(assigned_person)
    r_page.search_requisition_for_assigning(req_num)
    r_page.add_item_to_assign(req_num)
    r_page.assigning_items()
    r_page.get_full_page_screenshot('full_page_screenshot_22')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_23')
    r2_page.wait_for_timeout(5000)

def test_10_requisition_accept(page):
    req_num2 = "REQ20250004556"
    s_page = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=str(int(assigned_person)),
        pass_word=proj_gen_pass
    )

    r_page = RequisitionAcceptList(page)
    r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/assignedRequisitionShowList")
    r_page.search_requisition(req_num)
    r_page.select_all_requisitions()
    r_page.accept_requisition()
    r_page.get_full_page_screenshot('full_page_screenshot_24')
    r_page.confirm_acceptance()


def test_11_create_tender_initiation(page):
    req_num2 = "REQ20250004556"
    t_page = CreateTenderInitiation(page)
    t_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/methodSelection/show")
    t_page.search_requisition(req_num)
    t_page.select_all_items()
    t_page.select_direct_purchase_method()
    t_page.fill_remarks("Tender initiation done!")
    t_page.submit_tender_initiation()
    t_page.confirm_submission()
    t_page.get_full_page_screenshot('full_page_screenshot_25')


def test_12_create_direct_purchase(page):
    req_num2 = "REQ20250004556"
    t_page = CreateDirectPurchase(page)
    try:
        t_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/directPurchase/show")
        t_page.search_vendor(vendor_name)
        t_page.same_delivery_schedule()
        t_page.estimated_delivery_date_with_text("31/08/2025")
        t_page.delivery_location_dropdown_select()
        t_page.delivery_location("Dhaka, Bangladesh")
        t_page.search_item_by_name(req_num)
        t_page.select_all_items()
        t_page.save_and_next()
        t_page.get_full_page_screenshot('full_page_screenshot_26_1')
        global purchase_num
        purchase_num = t_page.get_purchase_order_number()
        print("Purchase number: "+purchase_num)
        t_page.get_full_page_screenshot('full_page_screenshot_26_2')
        t_page.template_selection()
        t_page.direct_purchase_approver_selecting(dp_approver)
        t_page.get_full_page_screenshot('full_page_screenshot_26')
        t_page.submit_direct_purchase()
        t_page.confirm_submission()
        t_page.get_full_page_screenshot('full_page_screenshot_27')
    except Exception as e:
        t_page.get_full_page_screenshot('full_page_screenshot_test_12')
        print(e)

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_28')
    r2_page.wait_for_timeout(5000)


def test_13_approve_direct_purchase(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=str(int(dp_approver)),
        pass_word=proj_gen_pass
    )

    t_page = DirectPurchaseList(page)
    try:
        t_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/directPurchase/list")
        t_page.search_purchase_order(purchase_num)
        # t_page.navigate_to_direct_purchase_detail_page(purchase_num)
        # t_page.approve_direct_purchase_from_details_page()
        t_page.select_direct_purchase_order(purchase_num)
        t_page.approve_direct_purchase()
        t_page.confirmation_message_approve()
        t_page.get_full_page_screenshot('full_page_screenshot_29')
    except Exception as e:
        t_page.get_full_page_screenshot('full_page_screenshot_test_13')
        print(e)

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_30')
    r2_page.wait_for_timeout(5000)


# def test_14_item_recieve(page):
#     s_page = LoginPage(page)
#     s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         user_name=str(int(assigned_person)),
#         pass_word=proj_gen_pass
#     )
#
#     t_page = ItemReceive(page)
#     t_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/itemReceive/show")
#     t_page.search_order_for_item_receive(purchase_num)
#     t_page.set_challan_number(challan_num)
#     t_page.challan_date("31-08-2025")
#     t_page.received_date("31-08-2025")
#     t_page.select_all_items()
#     t_page.submit_item_receive()
#     t_page.confirm_submission()
#     t_page.get_full_page_screenshot('full_page_screenshot_31')
#
#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_32')
#     r2_page.wait_for_timeout(5000)
#
#
# def test_15_bill_creation_and_submit(page):
#     s_page = LoginPage(page)
#     s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         user_name=str(int(bill_creator)),
#         pass_word=proj_gen_pass
#     )
#
#     t_page = CreateVendorBillPayable(page)
#     t_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/thirdPartyBillPayable/show")
#     t_page.search_vendor(vendor_name)
#     t_page.search_challan_number(challan_num)
#     t_page.bill_number(bill_num)
#     t_page.bill_date_with_text("31-08-2025")
#     t_page.bill_receive_date_with_text("31-08-2025")
#     t_page.select_all_items()
#     t_page.submit_bill()
#     t_page.get_full_page_screenshot('full_page_screenshot_33')
#     t_page.confirm_submission()
#     t_page.get_full_page_screenshot('full_page_screenshot_34')