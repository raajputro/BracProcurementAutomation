# this page contains all the test cases for the samplePage
import os
import random
import pytest
import sys

from playwright.sync_api import sync_playwright

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from conftestmiley import page
from pages.test_login import ResetHubPage

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
proj_env = os.getenv("test_env")


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

@pytest.mark.reporting(
    functional_specification="test_1",
    test_description="Verify that staff can successfully login as Requisition Initiator" )

def test_1_login_to_create_requisition(page, logger):
    
    reset_page = ResetHubPage(page)

    link = reset_page.generate_reset_link(
        env=proj_env,
        username=proj_user,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")

    logger.step(f" 📥 Logging in as user: {proj_user}")


def test_2_go_to_procurement_page(page):
    d_page = DashboardPage(page)
    d_page.goto_procurement()
    d_page.get_full_page_screenshot('full_page_screenshot_1')


@pytest.mark.reporting(
    functional_specification="test_1",
    test_description="Verify that initiator can successfully Create and Submit Requisition")

def test_3_create_and_submit_requisition(page, logger):
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Create Requisition"]

    print("Test 4: Creating requisition...")
    c_page = CreateReqPage(page)
    c_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
#     c_page.wait_for_timeout(30000)

    #c_page.validate()
    c_page.setting_requisition_for(item1["office_name"])
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "Tor for Item","100","19")
    c_page.setting_requisition_for_details("[1104010301-02] Advance to Staff against Expenses","gl remarks",c_page.select_date(20), "Head Office", "ABC Road")
    c_page.get_full_page_screenshot('full_page_screenshot_3')
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    logger.step(f" 📥 Requisition Created: {req_num}")
    c_page.get_full_page_screenshot('full_page_screenshot_4')


@pytest.mark.reporting(
    functional_specification="test_2",
    test_description="Verify that the user can Find Budget Recommender of the requisition successfully")

def test_4_find_budget_recommender_of_the_requisition(page, logger):
    print("Test 5: Finding Budget Recommender of the requisition...")
    r_page = RequisitionList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition List"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    r_page.get_full_page_screenshot('full_page_screenshot_5')
    r_page.search_requisition(req_num)
    global approver_id
    approver_id = str(int(r_page.find_approver_id()))
    print("Budget Recommender:", approver_id)
    logger.step(f" 📥 Requisition Budget Recommender is : {approver_id}")
    r_page.get_full_page_screenshot('full_page_screenshot_6')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_7')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_2",
    test_description="Verify that the Budget Recommender can login and approve the requisition successfully")

def test_5_login_as_budget_recommender_and_approve(page, logger):
    print("Test 6: Logging in as budget recommender and approving requisition...")
    reset_page = ResetHubPage(page)

    link = reset_page.generate_reset_link(
        env=proj_env,
        username=approver_id,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")
    logger.step(f" 📥 Logging in as user: {approver_id}")
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition Approve List"]
    r_page = RequisitionApproveList(page)
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    r_page.get_full_page_screenshot('full_page_screenshot_8')
    print(f"Req Number: {req_num}")
    r_page.search_requisition(req_num)
    r_page.select_requisition(req_num)
    r_page.approve_requisition()
    r_page.confirmation_message_approve()
    logger.step(f" 📥 Requisition Approved Sucessfully: {req_num}")
    r_page.get_full_page_screenshot('full_page_screenshot_9')
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_10')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_2",
    test_description="Verify that the requistion initiator can Find approver of the requisition successfully")

def test_6_find_approver_of_the_requisition(page, logger):
    print("Test 6: Finding approver of the requisition again...")

    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=proj_user,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")
    logger.step(f" 📥 Logging in as user: {proj_user}")

    r_page = RequisitionList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition List"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    r_page.get_full_page_screenshot('full_page_screenshot_11')
    r_page.search_requisition(req_num)
    global approver_id_2
    approver_id_2 = str(int(r_page.find_approver_id()))
    print("APPROVER ID 2:", approver_id_2)
    logger.step(f" 📥 Requisition Approver is : {approver_id_2}")
    r_page.get_full_page_screenshot('full_page_screenshot_12')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_13')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_2",
    test_description="Verify that the requistion approver can login and approve requisition successfully")

def test_7_login_as_approver_and_approve_2(page, logger):
    print("Test 7: Logging in as second approver and approving requisition...")

    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=approver_id_2,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")

    logger.step(f" 📥 Logging in as user: {approver_id_2}")
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition Approve List"]
    r_page = RequisitionApproveList(page)
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    r_page.get_full_page_screenshot('full_page_screenshot_14')
    r_page.search_requisition(req_num)
    r_page.select_requisition(req_num)
    r_page.approve_requisition()
    r_page.confirmation_message_approve()
    logger.step(f" 📥 Approver successfully approved the requisition")
    r_page.get_full_page_screenshot('full_page_screenshot_15')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_16')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_2",
    test_description="Verify that the requistion approved successfully")

def test_8_check_requisition_approved(page, logger):
    print("Test 8: Checking requisition status after approval...")

    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=approver_id_2,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")
 
    logger.step(f" 📥 Logging in as user: {proj_user}")
    r_page = RequisitionList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition List"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)

    r_page.navigate_to_url(requisition_list_url)
    r_page.get_full_page_screenshot('full_page_screenshot_17')
    r_page.search_requisition(req_num)
    r_page.get_full_page_screenshot('full_page_screenshot_18')
    req_status = r_page.find_requisition_status()
    print("REQ STATUS:", req_status)
    logger.step(f" 📥 Requisition Status: {req_status}")

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_19')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_3",
    test_description="Verify that the requistion assigned successfully")
 
def test_9_check_requisition_assign(page, logger):
    print("Test 9: Assigning requisition to a person...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=admin_user,
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")


    logger.step(f" 📥 Logging in as user: {admin_user}")
    r_page = AssignRequisition(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition Assign", "Assign Requisition"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    r_page.assigning_person(assigned_person)
    logger.step(f" 📥 Assigning requisition to user: {assigned_person}")
    r_page.search_requisition_for_assigning(req_num)
    r_page.add_item_to_assign(req_num)
    r_page.assigning_items()
    r_page.get_full_page_screenshot('full_page_screenshot_22')
    logger.step(f" 📥 Requisition Assigned successfully: {req_num}")

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_23')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_3",
    test_description="Verify that the assigned person can accept the requisition successfully")

def test_10_requisition_accept(page, logger):
    print("Test 10: Accepting requisition...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=str(int(assigned_person)),
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")


    logger.step(f" 📥 Logging in as user: {assigned_person}")
    r_page = RequisitionAcceptList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Requisition", "Requisition Assign", "Requisition Accept List"]
    r_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # r_page.navigate_to_url(requisition_accept_url)
    r_page.search_requisition(req_num)
    r_page.select_all_requisitions()
    r_page.accept_requisition()
    r_page.get_full_page_screenshot('full_page_screenshot_24')
    r_page.confirm_acceptance()
    logger.step(f" 📥 Requisition Accepted successfully: {req_num}")


@pytest.mark.reporting(
    functional_specification="test_4",
    test_description="Verify that the tender initiation can be created successfully")

def test_11_create_tender_initiation(page, logger):
    print("Test 11: Creating tender initiation...")
    t_page = CreateTenderInitiation(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Procurement Process", "Create Tender Initiation"]
    t_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # t_page.navigate_to_url(tender_initiation_url)
    t_page.search_requisition(req_num)
    t_page.select_all_items()
    t_page.select_direct_purchase_method()
    t_page.fill_remarks("Tender initiation done!")
    t_page.submit_tender_initiation()
    t_page.confirm_submission()
    logger.step(f" 📥 Tender Initiation created successfully for Requisition: {req_num}")
    t_page.get_full_page_screenshot('full_page_screenshot_25')


@pytest.mark.reporting(
    functional_specification="test_5",
    test_description="Verify that the direct purchase can be created successfully")

def test_12_create_direct_purchase(page, logger):
    print("Test 12: Creating direct purchase...")
    t_page = CreateDirectPurchase(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Purchase Order", "Direct Purchase", "Create Direct Purchase"]
    t_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)

    # t_page.navigate_to_url(direct_purchase_url)
    t_page.search_vendor(vendor_name)
    t_page.same_delivery_schedule()
    t_page.estimated_delivery_date_with_text(t_page.select_date(20))
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
    logger.step(f" 📥 Direct Purchase created successfully: {purchase_num}")
    t_page.get_full_page_screenshot('full_page_screenshot_27')

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_28')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_6",
    test_description="Verify that the direct purchase approver can approve direct purchase successfully")

def test_13_approve_direct_purchase(page, logger):
    print("Test 13: Approving direct purchase...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
        env=proj_env,
        username=str(int(dp_approver)),
    )
    
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")
 
    logger.step(f" 📥 Logging in as user: {dp_approver}")
    t_page = DirectPurchaseList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Purchase Order", "Direct Purchase", "Direct Purchase List"]
    t_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    try:
        # t_page.navigate_to_url(direct_purchase_list_url)
        t_page.search_purchase_order(purchase_num)
        t_page.select_direct_purchase_order(purchase_num)
        t_page.approve_direct_purchase()
        t_page.confirmation_message_approve()
        logger.step(f" 📥 Direct Purchase Approved successfully: {purchase_num}")
        t_page.get_full_page_screenshot('full_page_screenshot_29')
    except Exception as e:
        t_page.get_full_page_screenshot('full_page_screenshot_test_13')
        print(e)
    
    logger.step(f" 📥 Direct Purchase created successfully: {purchase_num}")

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_30')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_7",
    test_description="Verify that the item receive can be done successfully")

def test_14_item_receive(page, logger):
    print("Test 14: Receiving items...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
         env=proj_env,
         username=str(int(assigned_person)),
     )
     
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")   

    logger.step(f" 📥 Logging in as user: {assigned_person}")
    t_page = ItemReceive(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Item Receive", "Item Receive"]
    # t_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    t_page.navigate_to_url(item_receive_url)
    t_page.search_order_for_item_receive(purchase_num)
    t_page.set_challan_number(challan_num)
    t_page.receive_place("Dhaka, Bangladesh")
    t_page.select_all_items()
    t_page.submit_item_receive()
    t_page.confirm_submission()
    logger.step(f" 📥 Items received successfully and challan No is : {challan_num}")
    t_page.get_full_page_screenshot('full_page_screenshot_31')

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_32')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_8",
    test_description="Verify that the vendor bill creation and submission can be done successfully and bill recommender1 are identified")

def test_15_bill_creation_and_submit(page, logger):
    print("Test 15: Creating and submitting vendor bill payable...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
         env=proj_env,
         username=str(int(bill_creator)),
     )
     
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")

    logger.step(f" 📥 Logging in as user: {bill_creator}")
    t_page = CreateVendorBillPayable(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Bill Payable", "Create Vendor Bill Payable"]
    t_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # t_page.navigate_to_url(vendor_bill_payable_url)
    t_page.search_vendor(vendor_name)

    t_page.search_challan_number(challan_num)
    t_page.bill_number(bill_num)
    t_page.bill_date_with_text(t_page.select_date())
    t_page.bill_receive_date_with_text(t_page.select_date())
    t_page.select_all_items()
    t_page.submit_bill()
    t_page.get_full_page_screenshot('full_page_screenshot_33')
    t_page.confirm_submission()
    logger.step(f" 📥 Vendor Bill Payable created and submitted successfully: {bill_num}")
    t_page.get_full_page_screenshot('full_page_screenshot_34')

    l2_page = BillList(page)

    l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)
    global bill_recommender1
    bill_recommender1 = str(int(l2_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 1: {bill_recommender1}")
    logger.step(f" 📥 Bill Recommender 1 is : {bill_recommender1}")

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_35')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_9",
    test_description="Verify that the vendor bill recommender1 can approve the bill successfully and bill recommender2 are identified")

def test_16_vendor_bill_recommender1_approval(page, new_tab, logger):
    print("Test 16: Vendor bill recommender1 approval...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
         env=proj_env,
         username=bill_recommender1,
     )
     
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")
    

    logger.step(f" 📥 Logging in as user: {bill_recommender1}")
    l2_page = BillList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    l2_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    # # Opening new tab
    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)

    # # Preparing document location
    current_dir = os.getcwd()
    # print(f"Current directory: {current_dir}")
    document_location = os.path.join(current_dir, 'utils', 'upload_file.pdf')
    b_page.upload_document(document_location)

    # print(f"Document directory: {document_location}")

    # #  Continuing rest of the test
    b_page.get_full_page_screenshot('full_page_screenshot_36')
    b_page.select_bill_type("Regular")
    b_page.get_full_page_screenshot('full_page_screenshot_37')
    b_page.approve_bill()
    logger.step(f" 📥 Vendor Bill Recommender1 approved the bill successfully: {bill_num}")
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
    logger.step(f" 📥 Bill Recommender 2 is : {bill_recommender2}")
    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_39')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_9",
    test_description="Verify that the vendor bill recommender2 can approve the bill successfully")

def test_17_vendor_bill_recommender2_approval(page, new_tab, logger):
    print("Test 17: Vendor bill recommender2 approval...")
    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
         env=proj_env,
         username=bill_recommender2,
     )
     
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")


    logger.step(f" 📥 Logging in as user: {bill_recommender2}")
    l2_page = BillList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    l2_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)
    b_page.approve_bill()
    logger.step(f" 📥 Vendor Bill Recommender2 approved the bill successfully: {bill_num}")
    b_page.get_full_page_screenshot('full_page_screenshot_40')
    new_page.close()

    l3_page = BillList(page)
    l3_page.navigate_to_url(bill_payable_url)
    l3_page.search_bill(bill_num)
    l3_page.wait_for_timeout(5000)
    l3_page.get_full_page_screenshot('full_page_screenshot_41')
    global bill_approver_id
    bill_approver_id = str(int(l3_page.find_approver_id(bill_num)))
    logger.step(f" 📥 Bill Approver is : {bill_approver_id}")
    print(f"Bill Approver : {bill_approver_id}")

    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_41')
    r2_page.wait_for_timeout(5000)


@pytest.mark.reporting(
    functional_specification="test_9",
    test_description="Verify that the vendor bill approver can approve the bill successfully and bill status is approved")

def test_18_vendor_bill_approver_approval(page, new_tab, logger):
    print("Test 18: Vendor bill approver approval...")

    reset_page = ResetHubPage(page)
    link = reset_page.generate_reset_link(
         env=proj_env,
         username=bill_approver_id,
     )
     
    print("Generated Link:" + link)
    reset_page.open_generated_link(link)
    assert isinstance(link, str) and link.startswith("http")

    logger.step(f" 📥 Logging in as user: {bill_approver_id}")
    l2_page = BillList(page)
    main_menu_item = "Procurement"
    sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    l2_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # l2_page.navigate_to_url(bill_payable_url)
    l2_page.search_bill(bill_num)

    new_page = new_tab(lambda p:l2_page.click_on_bill_num(bill_num))
    b_page = BillDetails(new_page)
    b_page.wait_for_timeout(5000)
    b_page.approve_bill()
    logger.step(f" 📥 Vendor Bill Approver approved the bill successfully: {bill_num}")
    b_page.get_full_page_screenshot('full_page_screenshot_42')
    new_page.close()

    l3_page = BillList(page)
    l3_page.navigate_to_url(bill_payable_url)
    l3_page.search_bill(bill_num)
    l3_page.wait_for_timeout(5000)
    bill_status=l3_page.find_bill_status(bill_num)
    print("Bill STATUS:", bill_status)
    logger.step(f" 📥 Vendor Bill Status after approval: {bill_status}")
    l3_page.get_full_page_screenshot('full_page_screenshot_43')
