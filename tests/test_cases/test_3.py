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
item_1_qty = '1000'
item_1_unit = '25'

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
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Create Requisition"]

    print("Test 4: Creating requisition...")
    c_page = CreateReqPage(page)
    c_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    requisition_data = {
        'office_name': "[H04] - Procurement-BRAC",
    }
    #c_page.validate()
    c_page.setting_requisition_for(requisition_data["office_name"])
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "Tor for Item",item_1_qty,item_1_unit)
    c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture","gl remarks","30-07-2025", "Head Office", "ABC Road")
    c_page.get_full_page_screenshot('full_page_screenshot_3')
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    c_page.get_full_page_screenshot('full_page_screenshot_4')


def test_5_find_budget_recommender_of_the_requisition(page):
    print("Test 5: Finding approver of the requisition...")

    r_page = RequisitionList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition List"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)

    # r_page.navigate_to_url(requisition_list_url)
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


def test_6_login_as_budget_recommender_and_approve(page):
    print("Test 6: Logging in as approver and approving requisition...")
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=approver_id,
        pass_word=proj_pass,
        timeout=60000  # Increased timeout for login
    )
    r_page = RequisitionApproveList(page)
    r_page.navigate_to_url(requisition_approve_url)
    r_page.get_full_page_screenshot('full_page_screenshot_8')
    print(f"Req Number: {req_num}")
    # r_page.wait_for_timeout(10000)
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
    print("Test 7: Finding approver of the requisition again...")
    s_page  = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass
    )

    r_page = RequisitionList(page)
    r_page.navigate_to_url(requisition_list_url)
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
    print("Test 8: Logging in as second approver and approving requisition...")
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=approver_id_2,
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    r_page = RequisitionApproveList(page)
    r_page.navigate_to_url(requisition_approve_url)
    r_page.get_full_page_screenshot('full_page_screenshot_14')
    # r_page.search_requisition(req_num)
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
    print("Test 9: Checking requisition status after approval...")
    s_page  = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass
    )

    r_page = RequisitionList(page)
    r_page.navigate_to_url(requisition_list_url)
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


def test_10_check_requisition_assign(page):
    print("Test 10: Assigning requisition to a person...")
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=admin_user,
        pass_word=proj_gen_pass,
        given_url=proj_url,
        timeout=60000  # Increased timeout for login
    )

    r_page = AssignRequisition(page)
    r_page.navigate_to_url(requisition_assign_url)
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

def test_11_requisition_accept(page):
    print("Test 11: Accepting requisition...")
    req_num2 = "REQ20250004556"
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    print("Assigned person:", assigned_person)
    print("assigned person:", str(int(assigned_person)))
    print("assigned person type:", type(assigned_person))

    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(assigned_person)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    r_page = RequisitionAcceptList(page)
    r_page.navigate_to_url(requisition_accept_url)
    r_page.search_requisition(req_num)
    r_page.select_all_requisitions()
    r_page.accept_requisition()
    r_page.get_full_page_screenshot('full_page_screenshot_24')
    r_page.confirm_acceptance()


def test_12_create_tender_initiation(page):
    print("Test 12: Creating tender initiation...")
    req_num2 = "REQ20250004556"
    t_page = CreateTenderInitiation(page)
    t_page.navigate_to_url(tender_initiation_url)
    t_page.search_requisition(req_num)
    t_page.select_all_items()
    t_page.select_direct_purchase_method()
    t_page.fill_remarks("Tender initiation done!")
    t_page.submit_tender_initiation()
    t_page.confirm_submission()
    t_page.get_full_page_screenshot('full_page_screenshot_25')


def test_13_create_direct_purchase(page):
    print("Test 13: Creating direct purchase...")
    req_num2 = "REQ20250004556"
    t_page = CreateDirectPurchase(page)
    try:
        t_page.navigate_to_url(direct_purchase_url)
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


def test_14_approve_direct_purchase(page):
    print("Test 14: Approving direct purchase...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(dp_approver)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    t_page = DirectPurchaseList(page)
    try:
        t_page.navigate_to_url(direct_purchase_list_url)
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

#
def test_15_item_receive(page):
    print("Test 15: Receiving items...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(assigned_person)),
        pass_word=proj_gen_pass,
        timeout=60000
    )
    t_page = ItemReceive(page)
    t_page.navigate_to_url(item_receive_url)
    t_page.search_order_for_item_receive(purchase_num)
    t_page.set_challan_number(challan_num)
    # t_page.challan_date("31-08-2025")
    # t_page.received_date("31-08-2025")
    t_page.receive_place("Dhaka, Bangladesh")
    t_page.select_all_items()
    t_page.submit_item_receive()
    t_page.confirm_submission()
    t_page.get_full_page_screenshot('full_page_screenshot_31')

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_32')
    r2_page.wait_for_timeout(5000)



def test_16_bill_creation_and_submit(page):
    print("Test 16: Creating and submitting vendor bill payable...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(bill_creator)),
        pass_word=proj_gen_pass,
        timeout=60000
    )
    t_page = CreateVendorBillPayable(page)
    t_page.navigate_to_url(vendor_bill_payable_url)
    t_page.search_vendor(vendor_name)

    t_page.search_challan_number(challan_num)
    t_page.bill_number(bill_num)
    t_page.bill_date_with_text("31-08-2025")
    t_page.bill_receive_date_with_text("31-08-2025")
    t_page.select_all_items()
    t_page.submit_bill()
    t_page.get_full_page_screenshot('full_page_screenshot_33')
    t_page.confirm_submission()
    t_page.get_full_page_screenshot('full_page_screenshot_34')

    l2_page = BillList(page)

    l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)
    global bill_recommender1
    bill_recommender1 = str(int(l2_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 1: {bill_recommender1}")

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_35')
    r2_page.wait_for_timeout(5000)


def test_17_vendor_bill_recommender1_approval(page, new_tab):
    print("Test 17: Vendor bill recommender1 approval...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender1,
        pass_word=proj_gen_pass,
        timeout=60000
    )

    l2_page = BillList(page)
    l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    # # Opening new tab
    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)

    # # Preparing document location
    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, 'utils', 'upload_file.pdf')
    b_page.upload_document(document_location)

    print(f"Document directory: {document_location}")

    # #  Continuing rest of the test
    b_page.get_full_page_screenshot('full_page_screenshot_36')
    b_page.select_bill_type("Regular")
    b_page.get_full_page_screenshot('full_page_screenshot_37')
    b_page.approve_bill()
    b_page.get_full_page_screenshot('full_page_screenshot_38')

    # # Closing new tab
    new_page.close()

    # # Continuing rest of the test in parent tab
    l3_page = BillList(page)
    l3_page.navigate_to_url(bill_payable_url)
    l3_page.search_bill(bill_num)
    global bill_recommender2
    bill_recommender2 = str(int(l3_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 2: {bill_recommender2}")

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_39')
    r2_page.wait_for_timeout(5000)


def test_18_vendor_bill_recommender2_approval(page, new_tab):
    print("Test 18: Vendor bill recommender2 approval...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender2,
        pass_word=proj_gen_pass,
        timeout=60000
    )
    l2_page = BillList(page)
    l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)
    b_page.approve_bill()
    b_page.get_full_page_screenshot('full_page_screenshot_40')
    new_page.close()

    l3_page = BillList(page)
    l3_page.navigate_to_url(bill_payable_url)
    l3_page.search_bill(bill_num)
    l3_page.wait_for_timeout(5000)
    l3_page.get_full_page_screenshot('full_page_screenshot_41')
    global bill_approver_id
    bill_approver_id = str(int(l3_page.find_approver_id(bill_num)))
    print(f"Bill Approver : {bill_approver_id}")

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_41')
    r2_page.wait_for_timeout(5000)


def test_19_vendor_bill_approver_approval(page, new_tab):
    print("Test 19: Vendor bill approver approval...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=bill_approver_id,
        pass_word=proj_gen_pass,
        timeout=60000
    )

    l2_page = BillList(page)
    l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)
    b_page.wait_for_timeout(5000)
    b_page.approve_bill()
    b_page.get_full_page_screenshot('full_page_screenshot_42')
    new_page.close()

    l3_page = BillList(page)
    l3_page.navigate_to_url(bill_payable_url)
    l3_page.search_bill(bill_num)
    l3_page.wait_for_timeout(5000)
    bill_status=l3_page.find_bill_status(bill_num)
    print("Bill STATUS:", bill_status)
    l3_page.get_full_page_screenshot('full_page_screenshot_43')
