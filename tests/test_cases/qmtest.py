import os
import random

from dotenv import load_dotenv

from conftest import new_tab

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
#======================================================================================================================
# # Environment Data
proj_url = os.getenv("test_url")
eTender_url = os.getenv("etender_url")
vendor1 = os.getenv("vendor1")
vendor2 = os.getenv("vendor2")



proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
proj_gen_pass = os.getenv("test_user_generic_pass")
admin_user = os.getenv("test_admin")
assigned_person = os.getenv("test_requisition_assignee")
vendor_name = os.getenv("test_vendor_name")
dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")
tender_approver = os.getenv("test_tender_approver")
evaluation_approver = os.getenv("test_evaluation_approver") 
evaluation_recommender = os.getenv("test_evaluation_recommender")
opening_approver = os.getenv("test_opening_approver")
work_order_approver = os.getenv("test_work_order_approver")

#======================================================================================================================
#======================================================================================================================
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
from pages.tender_initiation_list import TenderInitiationList
from pages.tender_details_page import TenderDetails
from pages.create_direct_purchase import CreateDirectPurchase
from pages.direct_purchase_list import DirectPurchaseList
from pages.item_receive import ItemReceive
from pages.create_vendor_bill_payable import CreateVendorBillPayable
from pages.vendor_bill_payable_list import BillList
from pages.bill_details_information import BillDetails
from pages.eTender_login import EtenderLoginPage
from pages.vendor_participation import VendoParticipation
from pages.Participate_in_Tender import PerticipateTenderList
from pages.tender_list import TenderList
from pages.e_tender_details_page import ETenderDetails
from pages.tender_shot_list import TenderShortList
from pages.prepare_short_list import PrepareShortList
from pages.tender_evaluation_list import TenderEvaluationList
from pages.financial_evaluation import FinancialEvaluation
from pages.create_noal import CreateNoal
from pages.create_work_order import CreateWorkOrder
from pages.purchase_order_list import PurchaseOrderList
from pages.purchase_order_details_information import PurchaseOrderDetailsInformation

from datetime import datetime, timedelta


# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install
install()

req_num = ''
approver_id = ''
approver_id_2 = ''
approver_id_3 = ''
approver_id_4 = ''
tender_num = ''
work_order_num = ''
opening_date_str = ''
submission_date_str = ''
challan_num = str(random.randint(10000,99999))
bill_num = str(random.randint(10000,99999))
item_1_qty = '1000'
item_1_unit = '25'
# Get the current date and time


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
    c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture","gl remarks","30-09-2025", "Head Office", "ABC Road")
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
    t_page.select_Quotation_method()
    t_page.fill_remarks("Remarks for tender initiation")
    t_page.go_to_save_next()

    global tender_num
    tender_num = t_page.get_tender_number()
    print("Purchase number: "+tender_num)

    t_page.select_all_items()
    t_page.add_item_to_grid()
    t_page.go_to_save_next()

    t_page.same_delivery_schedule()
    # t_page.estimated_delivery_date_with_text("01-09-2025")
    t_page.estimated_delivery_date_with_text(t_page.add_days_to_current_date(10))
    
    t_page.delivery_location_dropdown_select()
    t_page.delivery_location("Dhaka, Bangladesh")
    t_page.default_evaluation_criteria("Manufacturer authorization letter")
    t_page.tender_submission_criteria("TIN Certificate")
    t_page.go_to_save_next()

    t_page.tender_template_selection("QM Template")
    current_time = datetime.now()
    global submission_date_str, opening_date_str
    submission_date_str = (current_time + timedelta(minutes=7)).strftime("%d-%m-%Y %I:%M %p")
    opening_date_str = (current_time + timedelta(minutes=9)).strftime("%d-%m-%Y %I:%M %p")
    print("Submission Date:", submission_date_str)
    print("Opening Date:", opening_date_str)
    t_page.submission_date(submission_date_str)
    t_page.opening_date(opening_date_str)
    t_page.opening_place("BRAC Center, 75 Mohakhali, Dhaka-1212")
    t_page.opening_offer_validity("30")
    t_page.terms_condition_template_selection("QM Terms And Conditions")
    t_page.award_notification_template_selection("QM Award Notifications")
    t_page.tender_approver_selecting(tender_approver)
    t_page.go_to_save_next()

    t_page.committee_type_selection("Evaluation committee")
    t_page.member_type_selection("APPROVER")
    t_page.select_member(evaluation_approver)
    t_page.add_committee_member_to_grid()
    t_page.committee_type_selection("Evaluation committee")
    t_page.member_type_selection("RECOMMENDER") 
    t_page.select_member(evaluation_recommender)
    t_page.add_committee_member_to_grid()
    t_page.committee_type_selection("Opening committee")
    t_page.member_type_selection("APPROVER")
    t_page.select_member(opening_approver)
    t_page.add_committee_member_to_grid()
    t_page.submit_tender_initiation()
    t_page.confirm_submission()
    t_page.get_full_page_screenshot('full_page_screenshot_25')
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_30')
    r2_page.wait_for_timeout(5000)

def test_13_approve_tender_initiation(page, new_tab):
    print("Test 14: ...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(tender_approver)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    t_page = TenderInitiationList(page)
    try:
        tender_initiation_list_url = proj_url + "/procurementDashboard/myDashboard#!/tenderInitiation/list"
        t_page.navigate_to_url(tender_initiation_list_url)
        t_page.search_tender(tender_num)
        new_page = new_tab(lambda p:t_page.navigate_to_tender_detail_page(tender_num))
        b_page = TenderDetails(new_page)
        b_page.approve_tender_from_details_page()
        b_page.get_full_page_screenshot('full_page_screenshot_29')
        new_page.close()
    except Exception as e:
        t_page.get_full_page_screenshot('full_page_screenshot_test_13')
        print(e)

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_30')
    r2_page.wait_for_timeout(5000)

def test_14_vendor1_participation_in_tender(page):
    print("Test 14: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name="Skylark",
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    # tender_num="BPD/2025/RFQ-1864"
    x_page = PerticipateTenderList(page)
    x_page.go_to_participate_in_tender()
    x_page.get_full_page_screenshot('full_page_screenshot_30_1')
    x_page.wait_for_timeout(15000)
    x_page.search_tender_EoI(tender_num)
    x_page.get_full_page_screenshot('full_page_screenshot_30_2')
    x_page.click_apply_button_for_tender(tender_num)
    x_page.get_full_page_screenshot('full_page_screenshot_30_3')
    document_location = r"C:\Users\shamima.sultana\Downloads\upload_file.pdf"
    x_page.fill_criteria_row("Manufacturer authorization letter", "Yes", "All good", document_location)
    x_page.get_full_page_screenshot('full_page_screenshot_30_4')
    x_page.fill_required_document_fields("TIN Certificate", "Here is the document", document_location)
    x_page.get_full_page_screenshot('full_page_screenshot_30_5')
    x_page.click_on_save_and_next()
    x_page.get_full_page_screenshot('full_page_screenshot_30_6')
    x_page.selecting_item("Glue Stick (Fevi Stick)")
    x_page.selecting_technical_button("Glue Stick (Fevi Stick)", "Yes", "All good", document_location)
    x_page.get_full_page_screenshot('full_page_screenshot_30_7')
    x_page.selecting_financial_button("Glue Stick (Fevi Stick)", "BDT", "15")
    x_page.get_full_page_screenshot('full_page_screenshot_30_8')
    x_page.click_on_submit()
    x_page.get_full_page_screenshot('full_page_screenshot_30_9')
    s_page.logout()
    s_page.get_full_page_screenshot('full_page_screenshot_30_10')

def test_16_tender_opening(page,new_tab):
    print("Test 16: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name=str(int(opening_approver)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    x_page = TenderList(page)
    x_page.go_to_tender_list()
    x_page.search_tender(tender_num)

    new_page = new_tab(lambda p:x_page.navigate_to_tender_details_page(tender_num))
    b_page = ETenderDetails(new_page)
    b_page.wait_until(opening_date_str)
    b_page.click_open_button()
    b_page.confirm_open_tender() 
    b_page.get_full_page_screenshot('full_page_screenshot_32_1')
    new_page.close()

    s_page.logout()
    s_page.get_full_page_screenshot('full_page_screenshot_32_2')  

def test_17_tender_shortlist(page,new_tab):
    print("Test 17: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name=assigned_person,
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    supplier_name="Skylark Printers"
    x_page = TenderShortList(page)
    x_page.go_to_tender_short_list()
    x_page.search_tender(tender_num)
    new_page = new_tab(lambda p:x_page.click_tender_number(tender_num))
    b_page = PrepareShortList(new_page)
    b_page.click_details_of_item(req_num, "Glue Stick (Fevi Stick)")
    b_page.get_full_page_screenshot('full_page_screenshot_33_1')
    document_location = r"C:\Users\shamima.sultana\Downloads\upload_file.pdf"
    b_page.fill_supplier_details(supplier_name, True,"All good", document_location, 5, 0)
    # b_page.fill_supplier_details("Inventory Test", False,"Not responsive",document_location)
    # b_page.fill_supplier_details("sadia enterprise 2", False,"Not responsive",document_location)
    b_page.get_full_page_screenshot('full_page_screenshot_33_2')
    b_page.click_shortlist_button()
    b_page.get_full_page_screenshot('full_page_screenshot_33_3')
    b_page.fill_recommendation_field("Ready to approve")
    b_page.get_full_page_screenshot('full_page_screenshot_33_4')    
    b_page.click_forward_to_committee()
    b_page.get_full_page_screenshot('full_page_screenshot_33_5')
    new_page.close()
    s_page.logout()
    s_page.get_full_page_screenshot('full_page_screenshot_33_6')

def test_18_Evaluation_recommender_approve(page,new_tab):
    print("Test 18: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name=str(int(evaluation_recommender)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    supplier_name="Skylark Printers"
    x_page = TenderEvaluationList(page)
    x_page.go_to_tender_evaluation_list()
    x_page.search_tender(tender_num)
    new_page = new_tab(lambda p:x_page.click_tender_number(tender_num))
    b_page = FinancialEvaluation(new_page)
    b_page.click_select_all_recommendations()
    b_page.get_full_page_screenshot('full_page_screenshot_34_1')
    b_page.click_bulk_accept()
    b_page.selecting_confirm_yes()
    b_page.get_full_page_screenshot('full_page_screenshot_34_2')
    new_page.close()
    s_page.logout()

def test_19_Evaluation_approver_approve(page,new_tab):
    print("Test 19: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name=evaluation_approver,
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    supplier_name="Skylark Printers"
    x_page = TenderEvaluationList(page)
    x_page.go_to_tender_evaluation_list()
    x_page.search_tender(tender_num)
    new_page = new_tab(lambda p:x_page.click_tender_number(tender_num))
    b_page = FinancialEvaluation(new_page)
    b_page.click_nominate_for_award()
    b_page.selecting_confirm_yes()
    b_page.get_full_page_screenshot('full_page_screenshot_35_1')
    new_page.close()
    s_page.logout()

def test_20_Creating_Noal(page,new_tab):
    print("Test 20: ...")
    s_page = EtenderLoginPage(page)
    s_page.perform_login(
        given_url=eTender_url,
        user_name=assigned_person,
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )

    supplier_name="Skylark Printers"
    x_page = CreateNoal(page)
    x_page.click_create_noal()
    x_page.search_tender(tender_num)
    x_page.select_items_by_tender_supplier_payment_type(tender_num,supplier_name,"Bank")
    x_page.get_full_page_screenshot('full_page_screenshot_36_1')
    x_page.click_submit_button()
    x_page.get_full_page_screenshot('full_page_screenshot_36_2')
    x_page.confirm_submission()
    x_page.get_full_page_screenshot('full_page_screenshot_36_3')
    s_page.logout()

def test_21_Create_Work_Order(page):
    print("Test 21: Create Work Order...")
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=assigned_person,
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    work_order_url = proj_url + "/procurementDashboard/myDashboard#!/workOrder/show"
    tender_num = "BPD/FA/2025/RFQ-251"
    noal_number = "NOAL2025149"
    r_page = CreateWorkOrder(page)
    r_page.navigate_to_url(work_order_url)
    r_page.get_full_page_screenshot('full_page_screenshot_37_1')
    tender_num = "BPD/2025/RFQ-1812"  
    supplier_name="Skylark Printers"
    r_page.select_vendor(supplier_name)
    r_page.select_payment_mode("Bank")
    r_page.select_first_checkbox_by_noal_and_tender(noal_number,tender_num)
    r_page.get_full_page_screenshot('full_page_screenshot_37_2')
    r_page.add_item_to_grid()
    r_page.same_delivery_schedule()
    delivary_date = r_page.add_days_to_current_date(5)
    r_page.estimated_delivery_date_with_text(delivary_date)
    r_page.delivery_location_dropdown_select()
    r_page.delivery_location("Dhaka, Bangladesh")
    r_page.go_to_save_next()
    global work_order_num
    work_order_num = r_page.get_work_order_number()
    r_page.select_purchase_order_template("Purchase Order Template")
    r_page.select_payment_template("Purchase Order Payment")
    r_page.select_terms_template("Purchase Order Terms and Condions")
    r_page.work_order_approver_selecting(work_order_approver)
    r_page.get_full_page_screenshot('full_page_screenshot_37_3')
    r_page.submit_work_order()
    r_page.get_full_page_screenshot('full_page_screenshot_37_4')
    #  logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_39')
    r2_page.wait_for_timeout(5000) 


def test_21_Approving_Work_Order(page,new_tab):
    print("Test 21: Approving Work Order...")
    s_page = LoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(work_order_approver)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    work_order_list_url = proj_url + "/procurementDashboard/myDashboard#!/workOrder/list"
    # work_order_num = "BPD/2025/PO-1554"
    r_page = PurchaseOrderList(page)
    r_page.navigate_to_url(work_order_list_url)
    r_page.get_full_page_screenshot('full_page_screenshot_38_1')
    r_page.search_work_order(work_order_num)
    new_page = new_tab(lambda p:r_page.click_on_work_order_num(work_order_num))
    b_page = PurchaseOrderDetailsInformation(new_page)
    b_page.approve_work_order()
    b_page.get_full_page_screenshot('full_page_screenshot_38_2')
    new_page.close()
    r_page.refresh()
    r_page.find_work_order_status()
    b_page.get_full_page_screenshot('full_page_screenshot_38_3')
    # logout from the page
    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_39')
    r2_page.wait_for_timeout(5000)

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
    t_page.search_order_for_item_receive(work_order_num)
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
    t_page.bill_date_with_text(t_page.add_days_to_current_date())
    t_page.bill_receive_date_with_text(t_page.add_days_to_current_date())
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