import os
import random

from dotenv import load_dotenv

from conftest import new_tab

load_dotenv()

# Project URLs
proj_url = os.getenv("test_url")
requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"


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
challan_num = str(random.randint(10000,99999))
bill_num = str(random.randint(10000,99999))
# Get the current date and time




# def test_1_login_to_create_requisition(page):
#     s_page  = LoginPage(page)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name="761",
#         pass_word=proj_pass
#     )


# def test_2_go_to_procurement_page(page):
#     d_page = DashboardPage(page)
#     d_page.goto_procurement()
#     d_page.get_full_page_screenshot('full_page_screenshot_1')


# def test_3_navigate_to_create_req_from_prod_dashboard(page):
#     p_page = ProcurementHomePage(page)
#     p_page.navigate_to_create_requisition()
#     p_page.get_full_page_screenshot('full_page_screenshot_2')
#     p_page.wait_for_timeout(7500)


# def test_4_create_and_submit_requisition(page):
#     print("Test 4: Creating requisition...")
#     c_page = CreateReqPage(page)
#     #c_page.validate()
#     c_page.setting_requisition_for("[H04] - Procurement-BRAC")
#     c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
#     c_page.setting_requisition_details("glue","[19193]-Glue Stick (Fevi Stick)-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "Tor for Item","1000","25")
#     c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture","gl remarks","30-08-2025", "Head Office", "ABC Road")
#     c_page.get_full_page_screenshot('full_page_screenshot_3')
#     global req_num
#     req_num = c_page.submit_requisition()
#     print("REQ NUM:", req_num)
#     c_page.get_full_page_screenshot('full_page_screenshot_4')


# def test_5_find_approver_of_the_requisition(page):
#     print("Test 5: Finding approver of the requisition...")
#     r_page = RequisitionList(page)

#     r_page.navigate_to_url(requisition_list_url)
#     r_page.get_full_page_screenshot('full_page_screenshot_5')
#     r_page.search_requisition(req_num)
#     global approver_id
#     approver_id = str(int(r_page.find_approver_id()))
#     print("APPROVER ID:", approver_id)
#     r_page.get_full_page_screenshot('full_page_screenshot_6')

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_7')
#     r2_page.wait_for_timeout(5000)

# # approver_id = "15370"
# # # approver_id = "197363"
# # req_num = "REQ20250014442"
# def test_6_login_as_approver_and_approve(page):
#     print("Test 6: Logging in as approver and approving requisition...")
#     s_page = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name=approver_id,
#         pass_word=proj_pass,
#         timeout=60000  # Increased timeout for login
#     )
#     r_page = RequisitionApproveList(page)
#     requisition_approve_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/authorizationList"
#     r_page.navigate_to_url(requisition_approve_url)
#     r_page.get_full_page_screenshot('full_page_screenshot_8')
#     r_page.search_requisition(req_num)
#     r_page.select_requisition(req_num)
#     r_page.approve_requisition()
#     r_page.confirmation_message_approve()
#     r_page.get_full_page_screenshot('full_page_screenshot_9')

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_10')
#     r2_page.wait_for_timeout(5000)


# def test_7_find_approver_of_the_requisition_2(page):
#     print("Test 7: Finding approver of the requisition again...")
#     s_page  = LoginPage(page)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name=proj_user,
#         pass_word=proj_pass
#     )

#     r_page = RequisitionList(page)
#     requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"
#     r_page.navigate_to_url(requisition_list_url)
#     r_page.get_full_page_screenshot('full_page_screenshot_11')
#     r_page.search_requisition(req_num)
#     global approver_id_2
#     approver_id_2 = str(int(r_page.find_approver_id()))
#     print("APPROVER ID 2:", approver_id_2)
#     r_page.get_full_page_screenshot('full_page_screenshot_12')

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_13')
#     r2_page.wait_for_timeout(5000)


# def test_8_login_as_approver_and_approve_2(page):
#     print("Test 8: Logging in as second approver and approving requisition...")
#     s_page = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name=approver_id_2,
#         pass_word=proj_gen_pass,
#         timeout=60000  # Increased timeout for login
#     )

#     r_page = RequisitionApproveList(page)
#     requisition_approve_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/authorizationList"
#     r_page.navigate_to_url(requisition_approve_url)
#     r_page.get_full_page_screenshot('full_page_screenshot_14')
#     r_page.search_requisition(req_num)
#     r_page.select_requisition(req_num)
#     r_page.approve_requisition()
#     r_page.confirmation_message_approve()
#     r_page.get_full_page_screenshot('full_page_screenshot_15')

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_16')
#     r2_page.wait_for_timeout(5000)


# def test_9_check_requisition_approved(page):
#     print("Test 9: Checking requisition status after approval...")
#     s_page  = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name=proj_user,
#         pass_word=proj_pass
#     )

#     r_page = RequisitionList(page)
#     requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"
#     r_page.navigate_to_url(requisition_list_url)
#     r_page.get_full_page_screenshot('full_page_screenshot_17')
#     r_page.search_requisition(req_num)
#     r_page.get_full_page_screenshot('full_page_screenshot_18')
#     req_status = r_page.find_requisition_status()
#     print("REQ STATUS:", req_status)
#     #expect(req_status).to_be_equal("Approved")

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_19')
#     r2_page.wait_for_timeout(5000)


# def test_10_check_requisition_assign(page):
#     print("Test 10: Assigning requisition to a person...")
#     s_page = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         user_name=admin_user,
#         pass_word=proj_gen_pass,
#         given_url=proj_url,
#         timeout=60000  # Increased timeout for login
#     )

#     r_page = AssignRequisition(page)
#     requisition_assign_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignRequisitions"
#     r_page.navigate_to_url(requisition_assign_url)
#     r_page.assigning_person(assigned_person)
#     r_page.search_requisition_for_assigning(req_num)
#     r_page.add_item_to_assign(req_num)
#     r_page.assigning_items()
#     r_page.get_full_page_screenshot('full_page_screenshot_22')

#     r2_page = MainNavigationBar(page)
#     r2_page.exit()
#     r2_page.logout()
#     r2_page.get_full_page_screenshot('full_page_screenshot_23')
#     r2_page.wait_for_timeout(5000)

# def test_11_requisition_accept(page):
#     print("Test 11: Accepting requisition...")
#     req_num2 = "REQ20250004556"
#     s_page = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     print("Assigned person:", assigned_person)
#     print("assigned person:", str(int(assigned_person)))
#     print("assigned person type:", type(assigned_person))

#     s_page.perform_login(
#         given_url=proj_url,
#         user_name=str(int(assigned_person)),
#         pass_word=proj_gen_pass,
#         timeout=60000  # Increased timeout for login
#     )

#     r_page = RequisitionAcceptList(page)
#     requisition_accept_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignedRequisitionShowList"
#     r_page.navigate_to_url(requisition_accept_url)
#     r_page.search_requisition(req_num)
#     r_page.select_all_requisitions()
#     r_page.accept_requisition()
#     r_page.get_full_page_screenshot('full_page_screenshot_24')
#     r_page.confirm_acceptance()


# def test_12_create_tender_initiation(page):
#     print("Test 12: Creating tender initiation...")
#     s_page = LoginPage(page)
#     # s_page.navigate_to_url(proj_url)
#     s_page.perform_login(
#         given_url=proj_url,
#         user_name="761",
#         pass_word=proj_pass,
#         timeout=60000  # Increased timeout for login
#     )
#     req_num2 = "REQ20250014465"
#     t_page = CreateTenderInitiation(page)
#     tender_initiation_url = proj_url + "/procurementDashboard/myDashboard#!/methodSelection/show"
#     t_page.navigate_to_url(tender_initiation_url)
#     t_page.search_requisition(req_num2)
#     t_page.select_all_items()
#     t_page.select_Quotation_method()
#     t_page.fill_remarks("Remarks for tender initiation")
#     t_page.go_to_save_next()

#     global tender_num
#     tender_num = t_page.get_tender_number()
#     print("Purchase number: "+tender_num)

#     t_page.select_all_items()
#     t_page.add_item_to_grid()
#     t_page.go_to_save_next()

#     t_page.same_delivery_schedule()
#     # t_page.estimated_delivery_date_with_text("01-09-2025")
#     t_page.estimated_delivery_date_with_text("31/08/2025")
    
#     t_page.delivery_location_dropdown_select()
#     t_page.delivery_location("Dhaka, Bangladesh")
#     t_page.default_evaluation_criteria("Manufacturer authorization letter")
#     t_page.tender_submission_criteria("TIN Certificate")
#     t_page.go_to_save_next()

#     t_page.tender_template_selection("QM Template")
#     current_time = datetime.now()
#     submission_date_str = (current_time + timedelta(minutes=7)).strftime("%d-%m-%Y %I:%M %p")
#     opening_date_str = (current_time + timedelta(minutes=9)).strftime("%d-%m-%Y %I:%M %p")
#     print("Submission Date:", submission_date_str)
#     print("Opening Date:", opening_date_str)
#     t_page.submission_date(submission_date_str)
#     t_page.opening_date(opening_date_str)
#     t_page.opening_place("BRAC Center, 75 Mohakhali, Dhaka-1212")
#     t_page.opening_offer_validity("30")
#     t_page.terms_condition_template_selection("QM Terms And Conditions")
#     t_page.award_notification_template_selection("QM Award Notifications")
#     t_page.tender_approver_selecting(tender_approver)
#     t_page.go_to_save_next()

#     t_page.committee_type_selection("Evaluation committee")
#     t_page.member_type_selection("APPROVER")
#     t_page.select_member(evaluation_approver)
#     t_page.add_committee_member_to_grid()
#     t_page.committee_type_selection("Evaluation committee")
#     t_page.member_type_selection("RECOMMENDER") 
#     t_page.select_member(evaluation_recommender)
#     t_page.add_committee_member_to_grid()
#     t_page.committee_type_selection("Opening committee")
#     t_page.member_type_selection("APPROVER")
#     t_page.select_member(opening_approver)
#     t_page.add_committee_member_to_grid()
#     t_page.submit_tender_initiation()
#     t_page.confirm_submission()
    # t_page.get_full_page_screenshot('full_page_screenshot_25')

def test_13_approve_tender_initiation(page, new_tab):
    print("Test 14: ...")
    s_page = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=str(int(tender_approver)),
        pass_word=proj_gen_pass,
        timeout=60000  # Increased timeout for login
    )
    tender_num = "BPD/2025/RFQ-1866"
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
        # t_page.select_tender(tender_num)
        # t_page.approve_tender()
        # t_page.confirmation_message_approve()
        # t_page.get_full_page_screenshot('full_page_screenshot_29')
    except Exception as e:
        t_page.get_full_page_screenshot('full_page_screenshot_test_13')
        print(e)

    r2_page = MainNavigationBar(page)
    r2_page.exit()
    r2_page.logout()
    r2_page.get_full_page_screenshot('full_page_screenshot_30')
    r2_page.wait_for_timeout(5000)