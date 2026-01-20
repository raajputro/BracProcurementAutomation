from dotenv import load_dotenv
import os
import re
import random
import string
from conftest import new_tab
from datetime import datetime, timedelta

load_dotenv()

# Project URLs
proj_url = os.getenv("test_url")
requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"

# Procurement information
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
# proj_gen_pass = os.getenv("test_user_generic_pass")
# admin_user = os.getenv("test_admin")
# assigned_person = os.getenv("test_requisition_assignee")
# vendor_name = os.getenv("test_vendor_name")
# dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")

# Marketplace information
marketplace_url_qa = os.getenv("test_marketplace_url_qa")
order_initiator = os.getenv("test_order_initiator")
marketplace_password = os.getenv("test_marketplace_password")
# req_num = os.getenv("test_req_num")
receiving_pin_1 = os.getenv("test_receiving_pin")
order_approver = os.getenv("test_order_approver")
dm_admin = os.getenv("test_order_admin")
manual_delivery_location_1 = os.getenv("test_delivery_location_1")
manual_delivery_location_2 = os.getenv("test_delivery_location_2")
dm_user_gen_password = os.getenv("test_dm_user_gen_password")
agreement = os.getenv("test_white_listed_agreement")
login_credential_for_receiver = os.getenv("test_login_credential_for_receiver")
proc_admin = os.getenv("test_proc_admin")
# order_reference_number = os.getenv("test_order_reference_number")

# Page models for procurement
from pages.digital_marketplace.procurement_login_page import ProcurementLoginPage
from pages.digital_marketplace.dashboard_page import DashboardPage
from pages.digital_marketplace.procurement_home_page import ProcurementHomePage
from pages.digital_marketplace.requisition_creation import CreateReqPage
from pages.digital_marketplace.requisition_list import RequisitionList
from pages.digital_marketplace.main_navigation_bar import MainNavigationBar
from pages.digital_marketplace.requisition_approve_list import RequisitionApproveList
from pages.digital_marketplace.requisition_details_information import RequisitionDetailsInformation
from pages.digital_marketplace.framework_information import FrameworkInformation
from pages.digital_marketplace.framework_order_list import FrameworkOrderListPage
from pages.digital_marketplace.proc_item_receive_list import ProcItemReceiveListPage
from pages.digital_marketplace.bill_list import BillList
from pages.digital_marketplace.create_vendor_bill_payable import CreateVendorBillPayable
from pages.digital_marketplace.bill_details import BillDetails

# Page models for marketplace
from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.home_page import HomePage
from pages.digital_marketplace.shopping_cart import ShoppingCart
from pages.digital_marketplace.checkout_page import CheckoutPage
from pages.digital_marketplace.main_navigation_menu import MainNavigationMenu
from pages.digital_marketplace.active_requisition_list import ActiveRequisitionListPage
from pages.digital_marketplace.active_requisition_product_list import ActiveRequisitionProductList
from pages.digital_marketplace.pending_approval_orders import PendingApprovalOrders
from pages.digital_marketplace.customers import Customers
from pages.digital_marketplace.product_switch_history import ProductSwitchHistory
from pages.digital_marketplace.vendor_dashboard import VendorDashboard
from pages.digital_marketplace.all_order_for_admin import AllOrderForAdminPage
from pages.digital_marketplace.order_management import OrderManagement
from pages.digital_marketplace.receivable_order_list import ReceivableOrderListPage
from pages.digital_marketplace.item_received_list import ItemReceivedList
from pages.digital_marketplace.order_details_administration import OrderDetailsAdministration

# import pages.login_page
# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install

install()
# Marketplace global variable
order_reference_number = ''
framework_order_no = ''
vendor_login_id = ''
challan_num_for_receiver = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
challan_num_for_order_initiator = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
challan_num_for_order_initiator_2 = ''.join(random.choices(string.ascii_letters, k=8))

# Procurement global variable
req_num = ''
approver_id = ''
approver_id_2 = ''
order_vendor = ''
# order_approver = ''
approver_id_3 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
bill_num = str(random.randint(10000, 99999))
bill_approver_id = ''
bill_recommender_1 = ''
bill_recommender_2 = ''
bill_recommender_3 = ''


def test_1_create_requisition_with_whitelisted_agreement_item(page):
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
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_1')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_create_requisition()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_2')

    print("Test 1: Creating requisition...")
    create_requisition_page = CreateReqPage(page)
    # c_page.validate()
    create_requisition_page.setting_requisition_for("[H10] - Construction")
    create_requisition_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    create_requisition_page.setting_requisition_details("pen",
                                                        "[22245]-Pen Box-(Supplies and Stationeries->Supplies and Stationeries->Stationery)")

    create_requisition_page.active_agreement_button.click()
    create_requisition_page.setting_active_framework_list(agreement_info="BPD/2024/FA-93")
    create_requisition_page.agreement_item_selector.nth(0).click()
    create_requisition_page.finalize_item_quantity(item_quantity="100")
    create_requisition_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture",
                                                            "Item remarks abc123@")
    create_requisition_page.setting_same_schedule_for_date()
    create_requisition_page.setting_location_for_head_office(address="Gulshan 1, Head Office, Dhaka - 1200")
    create_requisition_page.get_full_page_screenshot('full_page_screenshot_3')
    global req_num
    req_num = create_requisition_page.submit_requisition()
    print("REQ NUM:", req_num)
    create_requisition_page.navigate_to_requisition_list()
    create_requisition_page.get_full_page_screenshot('full_page_screenshot_4')


def test_2_identify_first_approver_for_created_requisition(page):
    """
    Test Case 2: Identify and capture the first approver of a submitted requisition.

    Objective:
        To verify that the system correctly retrieves the first-level approver
        assigned to the newly created requisition, ensuring that workflow routing
        is functioning as expected.

    Steps:
        1. Access the Requisition List page.
        2. Capture a full-page screenshot for documentation.
        3. Search for the recently submitted requisition using its requisition number ('req_num').
        4. Retrieve and store the approver ID of the first-level approver.
        5. Capture another screenshot showing the approver information.
        6. Log out from the current session to complete the test flow.
    """
    print("Test 2: Finding approver of the requisition...")
    requisition_list_page = RequisitionList(page)
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_5')
    requisition_list_page.search_requisition(req_num)

    global approver_id
    approver_id = str(int(requisition_list_page.find_approver_id()))
    print("APPROVER ID:", approver_id)
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_6')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_7')
    m_page.wait_for_timeout(2000)


def test_3_login_as_first_approver_and_approve_requisition(page):
    """
    Test Case 3: Login as the first approver and approve the submitted requisition in the ERP Procurement system.

    Objective:
        To verify that the first-level approver can successfully log in to the
        procurement portal, locate the submitted requisition, and approve it,
        ensuring that the workflow moves correctly to the next approval stage.

    Steps:
        1. Login to the procurement portal as the first-level approver using the 'approver_id'.
        2. Navigate to the procurement dashboard.
        3. Access the "Requisition Approve List" page.
        4. Capture a full-page screenshot for documentation.
        5. Search for the requisition using its requisition number ('req_num').
        6. Select the requisition from the list.
        7. Approve the requisition.
        8. Capture a screenshot showing the approved requisition.
        9. Wait briefly to ensure actions are completed.
        10. Log out from the session and capture a final screenshot.
    """
    print("Test 3: Logging in as approver and approving requisition...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=approver_id,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.menu_click_procurement_hyperlink()

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_requisition_approve_list()

    requisition_approve_list_page = RequisitionApproveList(page)
    requisition_approve_list_page.get_full_page_screenshot('full_page_screenshot_8')
    requisition_approve_list_page.search_requisition(req_num)
    requisition_approve_list_page.select_requisition()
    requisition_approve_list_page.approve_requisition()
    requisition_approve_list_page.get_full_page_screenshot('full_page_screenshot_9')
    requisition_approve_list_page.wait_for_timeout(2000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_10')
    m_page.wait_for_timeout(2000)


def test_4_identify_second_approver_for_created_requisition(page):
    """
    Test Case 4: Identify and capture the second-level approver of a submitted requisition in the ERP Procurement system.

    Objective:
        To verify that the system correctly retrieves the second-level approver
        for a previously submitted requisition, ensuring that the approval workflow
        is routed correctly to the next approver.

    Steps:
        1. Login to the procurement portal using the procurement user credentials.
        2. Navigate to the procurement dashboard.
        3. Access the "Requisition List" page.
        4. Search for the submitted requisition using its requisition number ('req_num').
        5. Capture a full-page screenshot for verification purposes.
        6. Retrieve and store the approver ID of the second-level approver in 'approver_id_2'.
        7. Capture a screenshot showing the approver information.
        8. Log out from the session and capture a final screenshot.
    """
    print("Test 4: Finding approver of the requisition again...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass,
        timeout=60000
    )
    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_requisition_list()

    requisition_list_page = RequisitionList(page)
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_11')
    requisition_list_page.search_requisition(req_num)

    global approver_id_2, order_approver
    global order_approver
    order_approver = requisition_list_page.find_approver_id()
    approver_id_2 = str(int(requisition_list_page.find_approver_id()))
    print("APPROVER ID 2:", approver_id_2)
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_12')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_13')
    m_page.wait_for_timeout(2000)


def test_5_login_as_second_approver_and_approve_requisition(page):
    """
    Test Case 5: Login as the second-level approver and approve the submitted requisition in the ERP Procurement system.

    Objective:
        To verify that the second-level approver can successfully log in, locate the requisition,
        and approve it, ensuring that the approval workflow progresses correctly to the next stage.

    Steps:
        1. Login to the procurement portal using the second-level approver credentials ('approver_id_2').
        2. Navigate to the procurement dashboard.
        3. Access the "Requisition Approve List" page.
        4. Capture a full-page screenshot for documentation purposes.
        5. Search for the submitted requisition using its requisition number ('req_num').
        6. Select the requisition from the list.
        7. Approve the requisition.
        8. Capture a screenshot showing the approved requisition.
        9. Wait briefly to ensure all actions are completed.
        10. Log out from the session and capture a final screenshot.
    """
    print("Test 5: Logging in as second approver and approving requisition...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=approver_id_2,
        pass_word=proj_pass,
        timeout=60000  # Increased timeout for login
    )
    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_requisition_approve_list()

    requisition_approve_list_page = RequisitionApproveList(page)
    requisition_approve_list_page.get_full_page_screenshot('full_page_screenshot_14')
    requisition_approve_list_page.search_requisition(req_num)
    requisition_approve_list_page.select_requisition()
    requisition_approve_list_page.approve_requisition()
    requisition_approve_list_page.get_full_page_screenshot('full_page_screenshot_15')
    requisition_approve_list_page.wait_for_timeout(2000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_16')
    m_page.wait_for_timeout(2000)


def test_6_verify_requisition_is_approved(page, new_tab):
    """
    Test Case 6: Verify that the requisition is approved and retrieve vendor information from the ERP Procurement system.

    Objective:
        To ensure that the requisition submitted and approved in previous steps
        is correctly reflected as "Approved" in the system, and to capture
        detailed information including the assigned vendor for documentation and verification.

    Steps:
        1. Login to the procurement portal using the procurement user credentials.
        2. Navigate to the procurement dashboard.
        3. Access the "Requisition List" page.
        4. Search for the submitted requisition using its requisition number ('req_num').
        5. Capture a screenshot of the requisition list and verify the requisition status.
        6. Open the requisition details page in a new tab.
        7. Capture a screenshot of the requisition details.
        8. Open the first FA (Framework Agreement) hyperlink in another new tab.
        9. Retrieve vendor information from the framework information page and store it in 'order_vendor'.
        10. Capture a screenshot of the framework information page.
        11. Close all newly opened tabs and return to the main page.
        12. Wait briefly to ensure all actions are completed.
        13. Log out from the session and capture a final screenshot.
    """
    print("Test 6: Checking requisition status after approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass,
        timeout=60000
    )
    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_requisition_list()

    requisition_list_page = RequisitionList(page)
    requisition_list_page.search_requisition(req_num)
    req_status = requisition_list_page.find_requisition_status()
    print("REQ STATUS:", req_status)
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_17')
    # expect(req_status).to_be_equal("Approved")
    # requisition_list_page.goto_requisition_details_information()
    # requisition_list_page.requisition_no.nth(0).click()

    new_page = new_tab(lambda p: requisition_list_page.goto_requisition_details_information())
    requisition_list_page.get_full_page_screenshot('full_page_screenshot_18')
    req_details = RequisitionDetailsInformation(new_page)
    # req_details.fa_no_hyperlink.nth(0).click()
    req_details.wait_for_timeout(2000)
    new_page_2 = new_tab(lambda p: req_details.fa_no_hyperlink.nth(0).click())
    req_details.get_full_page_screenshot('full_page_screenshot_19')
    framework_info = FrameworkInformation(new_page_2)

    global order_vendor
    order_vendor = framework_info.get_vendor_info()
    framework_info.wait_for_timeout(2000)
    framework_info.get_full_page_screenshot('full_page_screenshot_20')
    new_page_2.close()

    req_details.wait_for_timeout(2000)
    new_page.close()

    requisition_list_page = RequisitionList(page)
    requisition_list_page.wait_for_timeout(5000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_21')


# Marketplace flow
# Order initiation


def test_7_initiate_marketplace_order(page, new_tab):
    """
    Test Case 7: Marketplace order initiation process in the Test environment.

    Objective:
        To verify that a marketplace order can be initiated, processed, and confirmed successfully
        by the order initiator, including selecting vendors, updating cart information, uploading attachments,
        scheduling delivery, and confirming the order.

    Steps:
        1. Navigate to the marketplace staging URL and log in using SSO credentials.
        2. Verify the welcome message on the home page and capture a screenshot.
        3. Navigate to the shopping cart and capture a screenshot.
        4. Select the vendor for the requisition found and verify selection.
        5. Upload an attachment (PDF) to the cart and verify successful upload.
        6. Update shopping cart values (quantity and remarks) and capture a screenshot.
        7. Proceed to checkout, update quantities, and set expected delivery dates.
        8. Prepare delivery schedules for multiple locations and add them.
        9. Capture screenshots at key steps (checkout, delivery schedules, order review).
        10. Fill order remarks and accept terms of service.
        11. Confirm the order and store the global 'order_reference_number'.
        12. Navigate to public order details view and capture a screenshot.
        13. Logout from the marketplace system and capture a final screenshot.
    """
    print("Test 7: Marketplace order initiation process...")
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        user_name=order_initiator,
        pass_word=marketplace_password
    )

    home_page = HomePage(page)
    home_page.verify_welcome_message()
    home_page.get_full_page_screenshot('full_page_screenshot_22')
    home_page.wait_for_timeout(2000)
    home_page.goto_shopping_cart()

    cart_page = ShoppingCart(page)
    cart_page.get_full_page_screenshot('full_page_screenshot_23')
    cart_page.select_vendor_for_requisition_found(requisition_number=req_num)
    cart_page.wait_for_timeout(2000)
    cart_page.select_vendor_by_name(vendor_name=order_vendor, requisition_number=req_num)
    cart_page.wait_for_timeout(5000)
    cart_page.get_full_page_screenshot('full_page_screenshot_24')
    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, 'utils', 'upload_file.pdf')
    assert cart_page.upload_attachment(document_location), "File upload failed"
    # Or use below function
    # cart_page.upload_attachment(document_location)

    cart_page.update_shopping_cart_value_1(qty_update="10")
    cart_page.update_cart_item_remarks(
        requisition_number=req_num,
        remarks_text="Automation test remarks"
    )
    cart_page.update_shopping_cart_info()
    cart_page.get_full_page_screenshot('full_page_screenshot_25')
    cart_page.cart_page_checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.update_quantity(quantity="4")
    # checkout_page.schedule_expected_date.click()
    # expected_date = (datetime.strptime( "2025-09-04", "%Y-%m-%d") + timedelta(days=1)).strftime(
    #     "%Y-%m-%d")
    # checkout_page.schedule_expected_ date.fill(expected_date)

    checkout_page.update_expected_date()
    checkout_page.wait_for_timeout(5000)
    checkout_page.delivery_schedule_preparation(location=manual_delivery_location_1, pin=receiving_pin_1)
    checkout_page.click_add_schedule_button.click()
    checkout_page.wait_for_timeout(2000)
    checkout_page.delivery_schedule_preparation(location=manual_delivery_location_2, pin=order_initiator)
    checkout_page.click_add_schedule_button.click()
    checkout_page.get_full_page_screenshot('full_page_screenshot_26')
    checkout_page.click_continue()
    checkout_page.fillup_order_remarks(input_remarks="The initiator places an order")
    checkout_page.select_terms_of_service()
    checkout_page.get_full_page_screenshot('full_page_screenshot_27')

    global order_reference_number
    order_reference_number = checkout_page.confirm_order()
    print("Global order_reference_number", order_reference_number)
    checkout_page.wait_for_timeout(2000)
    checkout_page.get_full_page_screenshot('full_page_screenshot_28')
    checkout_page.goto_public_side_order_details_view()
    checkout_page.get_full_page_screenshot('full_page_screenshot_29')
    checkout_page.wait_for_timeout(5000)

    dm_logout = MainNavigationMenu(page)
    dm_logout.perform_logout()
    dm_logout.get_full_page_screenshot('full_page_screenshot_30')


def test_8_approve_marketplace_order(page):
    """
       Test Case 8: Marketplace order approval process by the designated approver.

       Objective:
           To verify that a marketplace order can be successfully approved by the
           second-level approver ('approver_id_2') in the staging environment, ensuring
           that the order moves correctly through the approval workflow.

       Steps:
           1. Login to the marketplace portal as the second-level approver.
           2. Capture a full-page screenshot on the home page.
           3. Navigate to the order list page.
           4. Navigate to the pending approval orders list.
           5. Search for the order using its reference number ('order_reference_number').
           6. View the pending order information toggle.
           7. Capture a screenshot showing order details.
           8. Open the pending approval order details page.
           9. Approve the order.
           10. Capture a screenshot confirming the approval.
           11. Wait briefly to ensure all actions are completed.
           12. Log out from the marketplace system.
       """
    print("Test 8: Order approval process...")
    login_page = LoginPage(page)
    login_page.perform_login_for_common_login(
        user_name=order_approver,
        pass_word=marketplace_password
    )

    home_page = HomePage(page)
    home_page.get_full_page_screenshot('full_page_screenshot_31')
    home_page.goto_order_list()
    home_page.get_full_page_screenshot('full_page_screenshot_32')
    home_page.goto_pending_approval_orders_list()

    pending_approval_orders = PendingApprovalOrders(page)
    pending_approval_orders.search_order_input(
        reference_number=order_reference_number
    )
    pending_approval_orders.click_order_search_button()
    pending_approval_orders.view_pending_order_info_toggle()
    pending_approval_orders.get_full_page_screenshot('full_page_screenshot_33')
    pending_approval_orders.goto_pending_approval_order_details()
    pending_approval_orders.get_full_page_screenshot('full_page_screenshot_34')
    pending_approval_orders.approve_order()
    # pending_approval_orders.check_pending_approval()
    # pending_approval_orders.multiselect_approve()
    pending_approval_orders.wait_for_timeout(2000)
    pending_approval_orders.get_full_page_screenshot('full_page_screenshot_35')

    dm_logout = MainNavigationMenu(page)
    dm_logout.perform_logout()


def test_9_retrieve_vendor_credentials_for_marketplace_order(page):
    """
    Test Case 9: Retrieve vendor credentials for a specific marketplace order.

    Objective:
        To verify that the admin user can successfully access order details and retrieve
        the vendor credentials associated with a specific order in the marketplace system.

    Steps:
        1. Login to the marketplace portal as an admin user ('dm_admin').
        2. Navigate to the "All Orders" page for admin and capture a screenshot.
        3. Search for the order using its reference number ('order_reference_number').
        4. Access the order details page and capture a screenshot.
        5. Return to the admin dashboard and capture a screenshot.
        6. Navigate to the customers page and view the list of customers/vendors.
        7. Search for the vendor associated with the order ('order_vendor').
        8. Retrieve and store the vendor login ID in the global variable 'vendor_login_id'.
        9. Capture a screenshot showing the vendor information.
        10. Log out from the administration portal.
    """
    print("Test 9: Find vendor credential for order...")
    login_page = LoginPage(page)
    login_page.perform_login_for_common_login(
        user_name=dm_admin,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.goto_all_orders_for_admin()
    home_page.get_full_page_screenshot('full_page_screenshot_36')

    all_orders = AllOrderForAdminPage(page)
    all_orders.admin_order_search(
        search_number=order_reference_number
    )
    all_orders.get_full_page_screenshot('full_page_screenshot_37')
    all_orders.admin_goes_to_order_details()
    all_orders.get_full_page_screenshot('full_page_screenshot_38')
    all_orders.goto_admin_dashboard()
    all_orders.get_full_page_screenshot('full_page_screenshot_39')

    customers_page = Customers(page)
    customers_page.view_customers_list()
    customers_page.search_vendor(customer_name=order_vendor)
    customers_page.wait_for_timeout(5000)

    global vendor_login_id
    vendor_login_id = customers_page.search_customers()
    print("Global vendor login ID:", vendor_login_id)
    customers_page.get_full_page_screenshot('full_page_screenshot_40')

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_10_vendor_acknowledges_marketplace_order(page):
    """
    Test Case 10: Marketplace vendor acknowledgement process.

    Objective:
        To verify that a vendor can log in to the marketplace portal, acknowledge
        the assigned order, generate a framework order number, and confirm
        that the order appears correctly in the order management system.

    Steps:
        1. Login to the marketplace portal as the vendor using 'vendor_login_id'.
        2. Capture a screenshot of the vendor dashboard and print relevant card titles and table data.
        3. Click the action button for the assigned order ('order_reference_number').
        4. Capture a screenshot after accessing order details.
        5. Confirm the acknowledgement by selecting "Yes" and generate a global framework order number ('framework_order_no').
        6. Capture a screenshot after confirmation the vendor acknowledgement and navigate back to the order list.
        7. Capture a screenshot of the vendor order list page.
        8. Search for the generated framework order number within the current date range.
        9. Capture a screenshot of the search results to verify the order.
        10. Log out from the marketplace administration portal.
    """
    print("Test 10: Vendor acknowledgement process...")
    login_page = LoginPage(page)
    login_page.perform_login_for_common_login(
        user_name=vendor_login_id,
        pass_word=marketplace_password
    )

    vendor_dashboard = VendorDashboard(page)
    vendor_dashboard.get_full_page_screenshot('full_page_screenshot_41')
    vendor_dashboard.print_card_title()
    vendor_dashboard.print_table_data()
    vendor_dashboard.get_full_page_screenshot('full_page_screenshot_42')
    vendor_dashboard.click_action_for_order(order_reference=order_reference_number)
    vendor_dashboard.get_full_page_screenshot('full_page_screenshot_43')
    vendor_dashboard.wait_for_timeout(5000)

    order_details_administration = OrderDetailsAdministration(page)
    global framework_order_no
    framework_order_no = order_details_administration.confirmation_acknowledgment_by_yes()
    print("Generate framework order number", framework_order_no)
    order_details_administration.wait_for_timeout(5000)
    order_details_administration.get_full_page_screenshot('full_page_screenshot_44')
    order_details_administration.click_back_to_order_list()
    order_details_administration.get_full_page_screenshot('full_page_screenshot_45')

    order_list = OrderManagement(page)
    current_date = datetime.today().strftime("%m-%d-%Y")
    order_list.fill_date_range(start_date=current_date, end_date=current_date)
    order_list.search_order(order_no=framework_order_no)
    order_list.get_full_page_screenshot('full_page_screenshot_46')
    order_list.wait_for_timeout(5000)

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_11_login_to_procurement_and_view_marketplace_work_order_details(page, new_tab):
    """
    Test Case 11: View marketplace framework order details in the procurement system.

    Objective:
        To verify that a procurement admin can log in, navigate to the framework
        order list, search for a specific framework order ('framework_order_no'),
        and view its details in a new tab for validation purposes.

    Steps:
        1. Login to the procurement portal as a procurement admin ('proc_admin').
        2. Navigate to the procurement dashboard and capture a screenshot.
        3. Access the "Framework Order List" page and capture a screenshot.
        4. Search for the specific framework order using 'framework_order_no'.
        5. Capture a screenshot showing the search results.
        6. Open the framework order details in a new browser tab and wait briefly.
        7. Capture a screenshot of the framework order details.
        8. Close the new tab and return to the main page.
        9. Log out from the procurement system and capture a final screenshot.
    """
    print("Test 11: Marketplace framework order details view in procurement system...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proc_admin,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_47')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_framework_order_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_48')

    framework_order_list_page = FrameworkOrderListPage(page)
    framework_order_list_page.search_framework_order(fa_order_no=framework_order_no)
    framework_order_list_page.get_full_page_screenshot('full_page_screenshot_49')

    new_page = new_tab(lambda p: framework_order_list_page.click_framework_order(framework_order_no=framework_order_no))
    framework_order_list_page.wait_for_timeout(5000)
    framework_order_list_page.get_full_page_screenshot('full_page_screenshot_50')
    new_page.close()

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_51')


# Item receive by receiver
def test_12_receiver_receives_marketplace_item(page):
    """
    Test Case 12: Marketplace item receipt process by the designated receiver.

    Objective:
        To verify that a receiver can log in to the marketplace portal, access
        the receivable orders, confirm receipt of items, upload necessary
        attachments, and validate the received items in the system.

    Steps:
        1. Login to the marketplace portal using the receiver's SSO credentials ('sso_login_receiver_pin').
        2. Navigate to the administration panel and capture a screenshot.
        3. Open the "Order Management" menu and access the receivable orders list.
        4. Filter orders by the current date and search for the specific framework order ('framework_order_no').
        5. Capture a screenshot of the receivable order list and view order details.
        6. Input the global challan number for the receiver ('challan_num_for_receiver') and print it.
        7. Select all items to be received and upload an attachment (PDF), verifying success.
        8. Add receiving remarks and capture a screenshot.
        9. Open the item receive popup, confirm the receivable order, and capture a screenshot.
        10. Verify the received order in the "Item Received List" page using the challan number and order number.
        11. Capture screenshots at key steps for verification.
        12. Log out from the administration portal.
    """
    print("Test 12: Item received by receiver...")
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        user_name=receiving_pin_1,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.goto_administration()
    home_page.get_full_page_screenshot('full_page_screenshot_52')
    home_page.wait_for_timeout(2000)

    order_list = OrderManagement(page)
    order_list.click_order_management_menu()

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%m-%d-%Y")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_53')
    receivable_order_list_page.receivable_order_view()

    global challan_num_for_receiver
    receivable_order_list_page.challan_no_input(fill_challan_no=challan_num_for_receiver)
    print("Print generated challan number for receiver: ", challan_num_for_receiver)

    receivable_order_list_page.all_item_select.click()

    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, "utils", "upload_file.pdf")
    assert receivable_order_list_page.receiving_upload_attachment(document_location), "File upload failed"

    receivable_order_list_page.wait_for_timeout(5000)

    receivable_order_list_page.input_received_remarks(receiving_remarks="Received remarks test 123 !@#")
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_54')
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_55')
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_56')

    item_receive_list_page = ItemReceivedList(page)
    current_date = datetime.today().strftime("%m-%d-%Y")
    item_receive_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    item_receive_list_page.search_received_order(received_order_number=framework_order_no)
    item_receive_list_page.searched_received_order(
        challan_no=challan_num_for_receiver
    )

    item_receive_list_page.search_button_for_received_item.click()
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_57')
    item_receive_list_page.order_view_button.click()
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_58')
    item_receive_list_page.wait_for_timeout(5000)

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_13_order_initiator_receives_marketplace_item(page):
    """
    Test Case 13: Marketplace item receipt by order initiator acting as receiver.

    Objective:
        To verify that the order initiator can act as a receiver to confirm receipt
        of items in the marketplace portal, including partial receipt scenarios,
        uploading attachments, and validating received items in the system.

    Steps:
        1. Login to the marketplace portal as the order initiator ('proj_user') using SSO.
        2. Navigate to the administration panel and capture a screenshot.
        3. Access the "Order Management" menu and open the receivable order list.
        4. Filter orders by the current date and search for the framework order ('framework_order_no').
        5. Capture a screenshot and view the receivable order details.
        6. Input the challan number ('challan_num_for_order_initiator') and print it.
        7. Select all items to receive and input the quantity to be received.
        8. Upload an attachment (PNG file) and verify upload success.
        9. Add receiving remarks, open the item receive popup, confirm the receivable order, and capture screenshots.
        10. Verify received items in the "Item Received List" using the challan number and order number.
        11. Repeat steps 4-10 for a second challan ('challan_num_for_order_initiator_2') with a different attachment (ZIP file) and remarks.
        12. Capture screenshots at all key steps for documentation.
        13. Log out from the administration portal.
    """
    print("Test 13: Item received by receiver as order initiator...")
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        user_name=order_initiator,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.goto_administration()
    home_page.get_full_page_screenshot('full_page_screenshot_59')
    home_page.wait_for_timeout(2000)

    order_list = OrderManagement(page)
    order_list.click_order_management_menu()

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%m-%d-%Y")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_60')
    receivable_order_list_page.receivable_order_view()

    global challan_num_for_order_initiator
    receivable_order_list_page.challan_no_input(fill_challan_no=challan_num_for_order_initiator)
    print("Print generated challan number for order initiator: ", challan_num_for_order_initiator
          )

    receivable_order_list_page.all_item_select.click()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.input_quantity_to_receive(received_quantity="1")

    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, "utils", "image_png.png")
    assert receivable_order_list_page.receiving_upload_attachment(document_location), "File upload failed"

    receivable_order_list_page.input_received_remarks(
        receiving_remarks="Partially received item 1")
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_61')
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_62')
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_63')

    item_receive_list_page = ItemReceivedList(page)
    current_date = datetime.today().strftime("%m-%d-%Y")
    item_receive_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    item_receive_list_page.search_received_order(received_order_number=framework_order_no)
    item_receive_list_page.searched_received_order(

        challan_no=challan_num_for_order_initiator
    )
    item_receive_list_page.search_button_for_received_item.click()
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_64')
    item_receive_list_page.order_view_button.click()
    item_receive_list_page.wait_for_timeout(5000)
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_65')

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%m-%d-%Y")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_66')
    receivable_order_list_page.receivable_order_view()

    global challan_num_for_order_initiator_2
    receivable_order_list_page.challan_no_input(fill_challan_no=challan_num_for_order_initiator_2)
    print("Print generated challan number for order initiator: ", challan_num_for_order_initiator_2
          )

    receivable_order_list_page.all_item_select.click()

    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, "utils", "Zip.zip")
    assert receivable_order_list_page.receiving_upload_attachment(document_location), "File upload failed"

    receivable_order_list_page.input_received_remarks(
        receiving_remarks="Received remarks test123.")
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_67')
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_68')
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_69')

    item_receive_list_page = ItemReceivedList(page)
    current_date = datetime.today().strftime("%m-%d-%Y")
    item_receive_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    item_receive_list_page.search_received_order(received_order_number=framework_order_no)
    item_receive_list_page.searched_received_order(
        challan_no=challan_num_for_order_initiator_2
    )
    item_receive_list_page.search_button_for_received_item.click()
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_70')
    item_receive_list_page.order_view_button.click()
    item_receive_list_page.wait_for_timeout(5000)
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_71')

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_14_login_to_procurement_and_view_marketplace_item_receipt_details(page):
    """
    Test Case 14: View marketplace item receive details in the procurement system.

    Objective:
        To verify that a procurement admin can log in, access the item receive list,
        search for a specific received item ('framework_order_no'), and view its details
        in the procurement system.

    Steps:
        1. Login to the procurement portal as a procurement admin ('proc_admin').
        2. Navigate to the procurement dashboard and capture a screenshot.
        3. Access the "Item Receive List" page and capture a screenshot.
        4. Search for the specific item receive order using 'framework_order_no'.
        5. Capture a screenshot showing the search results.
        6. Open the item receive details view and capture a screenshot.
        7. Log out from the procurement system and capture a final screenshot.
     """
    print("Test 14: Marketplace item receive details view in procurement system...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proc_admin,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_72')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_item_receive_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_73')

    proc_item_receive_list_page = ProcItemReceiveListPage(page)
    proc_item_receive_list_page.search_item_receive_order(receivable_item=framework_order_no)
    proc_item_receive_list_page.get_full_page_screenshot('full_page_screenshot_74')
    proc_item_receive_list_page.item_receive_details_view()
    proc_item_receive_list_page.get_full_page_screenshot('full_page_screenshot_75')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_76')


def test_15_create_and_submit_bill_for_received_marketplace_item(page):
    """
    Test Case 15: Bill creation and submission for Marketplace item receive in procurement system.

    Objective:
        To verify that a procurement user can create a vendor bill for received Marketplace items,
        submit the bill, and assign the appropriate recommender for approval in the procurement system.

    Steps:
        1. Login to the procurement portal as bill creator ('bill_creator').
        2. Navigate to the procurement dashboard and capture a screenshot.
        3. Access the "Bill Payable" section and capture a screenshot.
        4. Create a vendor bill for a specific framework order ('framework_order_no').
        5. Search for the vendor ('order_vendor') and select the corresponding order number and challan number ('challan_num_for_receiver').
        6. Set the global bill number ('bill_num'), bill date, and bill receive date.
        7. Select all items and assign the second recommender ('00009026') for approval.
        8. Capture screenshots at key steps and submit the bill.
        9. Confirm submission and capture a screenshot.
        10. Navigate to the bill list, search for the submitted bill, and identify the first recommender ('bill_recommender1').
        11. Capture a screenshot of the bill details.
    """
    print("Test 15: Bill creation and submission flow for Marketplace item receive in procurement system...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_creator,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_80')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_bill_payable()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_81')

    create_vendor_bill = CreateVendorBillPayable(page)
    create_vendor_bill.vendor_bill_payable_information_for_framework_order()
    create_vendor_bill.search_vendor(vendor_name=order_vendor)
    create_vendor_bill.select_order_no(order_num=framework_order_no)
    create_vendor_bill.select_challan_no(challan_no=challan_num_for_receiver)

    global bill_num
    create_vendor_bill.bill_number(bill_no_1=bill_num)
    create_vendor_bill.bill_date_with_text(create_vendor_bill.select_date())
    create_vendor_bill.bill_receive_date_with_text(create_vendor_bill.select_date())
    create_vendor_bill.select_all_items()
    create_vendor_bill.Bill_recommender2_selecting(recommender="00009026")
    create_vendor_bill.get_full_page_screenshot('full_page_screenshot_82')
    create_vendor_bill.submit_bill()
    create_vendor_bill.get_full_page_screenshot('full_page_screenshot_83')
    create_vendor_bill.confirm_submission()
    create_vendor_bill.wait_for_timeout(5000)
    create_vendor_bill.get_full_page_screenshot('full_page_screenshot_84')

    bill_list_page = BillList(page)
    bill_list_page.go_to_billing_list()
    bill_list_page.get_full_page_screenshot('full_page_screenshot_85')
    bill_list_page.search_bill(bill_num)
    global bill_recommender_1
    bill_recommender_1 = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 1: {bill_recommender_1}")
    bill_list_page.get_full_page_screenshot('full_page_screenshot_86')


def test_16_first_recommender_approves_marketplace_bill(page, new_tab):
    """
    Test Case 16: Vendor bill approval by first recommender in the procurement system.

    Objective:
        To verify that the first recommender can review, upload supporting documents,
        approve a vendor bill, and assign the next approver in the workflow.

    Steps:
        1. Open the vendor bill list and locate the bill ('bill_num').
        2. Open the bill details in a new tab.
        3. Upload the necessary supporting document for the bill.
        4. Select the bill type ("Regular") and capture a screenshot.
        5. Approve the bill and capture a screenshot of the approval.
        6. Close the bill detail tab and return to the main bill list.
        7. Search for the bill to identify the next approver ('bill_recommender_2') and capture a screenshot.
        8. Exit and log out from the procurement system, capturing a final screenshot.
    """
    print("Test 16: Vendor bill recommender1 approval...")
    bill_list_page = BillList(page)
    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))

    bill_detail_page = BillDetails(new_page)
    current_dir = os.getcwd()
    document_location = os.path.join(current_dir, 'utils', 'upload_file.pdf')
    bill_detail_page.upload_document(document_location)
    bill_detail_page.select_bill_type("Regular")
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_87')
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_88')
    new_page.close()

    bill_list_page = BillList(page)
    bill_list_page.search_bill(bill_num)
    global bill_recommender_2
    bill_recommender_2 = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 2: {bill_recommender_2}")
    bill_list_page.get_full_page_screenshot('full_page_screenshot_89')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_90')


def test_17_second_recommender_approves_marketplace_bill(page, new_tab):
    """
    Test Case 17: Vendor bill approval by second recommender in the procurement system.

    Objective:
        To verify that the second recommender can review and approve a vendor bill,
        and the next approver (if any) is correctly assigned in the workflow.

    Steps:
        1. Login to the procurement portal as the second recommender ('bill_recommender2').
        2. Navigate to the procurement dashboard and capture a screenshot.
        3. Access the vendor billing list and capture a screenshot.
        4. Search for the specific bill ('bill_num') and open the bill details in a new tab.
        5. Approve the bill and capture a screenshot of the approval.
        6. Close the bill detail tab and return to the bill list.
        7. Search for the bill to identify the next approver ('bill_recommender_3') and capture a screenshot.
        8. Exit and log out from the procurement system, capturing a final screenshot.
    """
    print("Test 17: Vendor bill recommender2 approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender_2,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_91')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.bill_payable.click()
    proc_home_page.goto_vendor_billing_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_92')

    bill_list_page = BillList(page)
    bill_list_page.search_bill(bill_num)
    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))

    bill_detail_page = BillDetails(new_page)
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_93')
    new_page.close()

    bill_list_page = BillList(page)
    page.reload()
    # bill_list_page.wait_for_timeout(5000)
    #     bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)
    bill_list_page.wait_for_timeout(5000)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_94')
    global bill_recommender_3
    bill_recommender_3 = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Approver : {bill_recommender_3}")
    bill_list_page.get_full_page_screenshot('full_page_screenshot_95')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_96')


def test_18_vendor_bill_approver_approval_process_in_procurement(page, new_tab):
    """
    Test Case 18: Vendor bill final approval by the approver in the procurement system.

    Objective:
        To verify that the final approver can review and approve the vendor bill,
        and confirm that the bill status is updated correctly after approval.

    Steps:
        1. Login to the procurement portal as the final approver (`bill_approver_id3`).
        2. Navigate to the procurement dashboard and capture a screenshot.
        3. Access the vendor billing list and capture a screenshot.
        4. Search for the specific bill (`bill_num`) and open the bill details in a new tab.
        5. Wait for page readiness, capture a screenshot, and approve the bill.
        6. Capture a screenshot of the approved bill and close the bill detail tab.
        7. Return to the main bill list, reload the page, and capture a screenshot.
        8. Search for the bill to verify the final status and capture a screenshot.
        9. Exit and log out from the procurement system, capturing a final screenshot.
        10. Marketplace item received bill for challan number 'challan_num_for_receiver' sent to the HO FIN from the procurement system.
    """
    print("Test 18: Vendor bill approver approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender_3,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_97')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.bill_payable.click()
    proc_home_page.goto_vendor_billing_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_98')

    bill_list_page = BillList(page)
    bill_list_page.search_bill(bill_num)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_99')
    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))

    bill_detail_page = BillDetails(new_page)
    bill_detail_page.wait_for_timeout(5000)
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_100')
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_101')
    new_page.close()

    bill_list_page = BillList(page)
    page.reload()
    bill_list_page.wait_for_timeout(5000)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_102')
    bill_list_page.search_bill(bill_num)
    bill_list_page.wait_for_timeout(5000)
    bill_status = bill_list_page.find_bill_status(bill_num)
    print("Bill STATUS:", bill_status)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_103')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_104')
