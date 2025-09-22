from dotenv import load_dotenv
import os
import re
import random
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
# bill_creator = os.getenv("test_bill_creator")

# Marketplace information
# marketplace_url_stg = os.getenv("test_marketplace_url_stg")
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
from pages.digital_marketplace.framework_order_list import FrameworkOrderListPage
from pages.digital_marketplace.proc_item_receive_list import ProcItemReceiveListPage

# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install

install()
order_reference_number = ''
# order_vendor = ''
framework_order_no = ''
vendor_login_id = ''
# order_number = ''

# req_num = ''
approver_id = ''
approver_id_2 = ''
# order_approver = ''
approver_id_3 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
bill_num = str(random.randint(10000, 99999))


def test_1_login_to_create_and_submit_requisition(page):
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


def test_2_find_1st_approver_of_the_requisition(page):
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


def test_3_login_as_1st_approver_and_approve_requisition(page):
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


def test_4_find_2nd_approver_of_the_requisition(page):
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


def test_5_login_as_2nd_approver_and_approve_requisition(page):
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


def test_6_check_requisition_approved(page, new_tab):
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
req_num = "REQ20250014590"
order_vendor = "Plan for demand"


def test_7_order_initiation(page, new_tab):
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
    # cart_page.select_vendor_for_requisition_found(requisition_number="REQ20250014590")
    cart_page.select_vendor_for_requisition_found(requisition_number=req_num)
    cart_page.wait_for_timeout(2000)
    cart_page = ShoppingCart(page)
    # cart_page.select_vendor_by_name(vendor_name="Plan for demand", requisition_number="REQ20250014590")
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
        # requisition_number="REQ20250014590",
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
    # checkout_page.delivery_schedule_preparation(location="manual_delivery_location_1", pin="00175050")
    checkout_page.click_add_schedule_button.click()
    checkout_page.wait_for_timeout(2000)
    # checkout_page.delivery_schedule_preparation(location="manual_delivery_location_2", pin="00006008")
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

    # new_page.close()

    dm_logout = MainNavigationMenu(page)
    dm_logout.perform_logout()
    dm_logout.get_full_page_screenshot('full_page_screenshot_30')


def test_8_order_approve(page):
    print("Test 8: Order approval process...")
    login_page = LoginPage(page)
    # login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        # user_name="00155790",
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


def test_9_find_vendor_credential_for_order(page):
    print("Test 9: Find vendor credential for order...")
    login_page = LoginPage(page)
    # login_page.navigate_to_url(marketplace_url_qa)
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


def test_10_vendor_acknowledgement(page):
    print("Test 10: Vendor acknowledgement process...")
    login_page = LoginPage(page)
    # login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_vendor_login(
        user_name=vendor_login_id,
        pass_word=marketplace_password
    )
    vendor_dashboard = VendorDashboard(page)
    vendor_dashboard.get_full_page_screenshot('full_page_screenshot_41')
    vendor_dashboard.print_card_title()
    vendor_dashboard.print_table_data()
    vendor_dashboard.click_action_for_order(order_reference=order_reference_number)
    vendor_dashboard.get_full_page_screenshot('full_page_screenshot_42')
    vendor_dashboard.wait_for_timeout(5000)

    order_details_administration = OrderDetailsAdministration(page)
    global framework_order_no
    framework_order_no = order_details_administration.confirmation_acknowledgment_by_yes()
    print("Generate framework order number", framework_order_no)
    order_details_administration.wait_for_timeout(5000)
    order_details_administration.get_full_page_screenshot('full_page_screenshot_43')
    order_details_administration.click_back_to_order_list()
    order_details_administration.get_full_page_screenshot('full_page_screenshot_44')

    order_list = OrderManagement(page)
    order_list.search_order(order_no=framework_order_no)
    order_list.get_full_page_screenshot('full_page_screenshot_45')
    order_list.wait_for_timeout(5000)

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_11_login_to_procurement_and_view_work_order_details(page, new_tab):
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
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_46')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.navigate_to_framework_order_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_47')

    framework_order_list_page = FrameworkOrderListPage(page)
    framework_order_list_page.search_framework_order(fa_order_no=framework_order_no)
    framework_order_list_page.get_full_page_screenshot('full_page_screenshot_48')

    new_page = new_tab(lambda p: framework_order_list_page.click_framework_order(framework_order_no=framework_order_no))
    framework_order_list_page.wait_for_timeout(5000)
    framework_order_list_page.get_full_page_screenshot('full_page_screenshot_49')
    new_page.close()

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_50')


# Item receive by receiver
def test_12_item_receive_by_receiver(page):
    print("Test 12: Item received by receiver...")
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        user_name=receiving_pin_1,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.goto_administration()
    home_page.get_full_page_screenshot('full_page_screenshot_51')
    home_page.wait_for_timeout(2000)

    order_list = OrderManagement(page)
    order_list.click_order_management_menu()

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%Y-%m-%d")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_52')

    receivable_order_list_page.receivable_order_view()
    receivable_order_list_page.challan_no_input(fill_challan_no="Item receive by receiver_10")
    receivable_order_list_page.all_item_select.click()
    receivable_order_list_page.input_received_remarks(receiving_remarks="Received remarks test 123 !@#")
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_53')
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_54')
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_55')

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


# Partially received
def test_13_item_receive_by_order_initiator_as_receiver(page):
    print("Test 13: Item received by receiver as order initiator...")
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        # user_name="00006008",
        user_name=order_initiator,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.goto_administration()
    home_page.get_full_page_screenshot('full_page_screenshot_56')
    home_page.wait_for_timeout(2000)

    order_list = OrderManagement(page)
    order_list.click_order_management_menu()

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%Y-%m-%d")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_57')
    receivable_order_list_page.receivable_order_view()
    receivable_order_list_page.challan_no_input(
        fill_challan_no="Partially item receive by receiver as order initiator_11")
    receivable_order_list_page.all_item_select.click()
    receivable_order_list_page.wait_for_timeout(5000)
    receivable_order_list_page.input_quantity_to_receive(received_quantity="1")

    # current_dir = os.getcwd()
    # document_location = os.path.join(current_dir, "utils", 'upload_file.pdf')
    # # receivable_order_list_page.upload_file(document_location)
    # assert receivable_order_list_page.upload_file(document_location), "File upload failed"

    receivable_order_list_page.input_received_remarks(
        receiving_remarks="Received remarks test 123 !@# for initiator partially received item 1")
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)

    item_receive_list_page = ItemReceivedList(page)
    item_receive_list_page.searched_received_order(
        challan_no="Partially item receive by receiver as order initiator_11")
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_58')
    item_receive_list_page.search_button_for_received_item.click()
    item_receive_list_page.order_view_button.click()
    item_receive_list_page.wait_for_timeout(5000)

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%Y-%m-%d")
    receivable_order_list_page.fill_date_range(start_date=current_date, end_date=current_date)
    receivable_order_list_page.search_receivable_order(receivable_order_number=framework_order_no)
    receivable_order_list_page.get_full_page_screenshot('full_page_screenshot_59')
    receivable_order_list_page.receivable_order_view()
    receivable_order_list_page.challan_no_input(
        fill_challan_no="Partially item receive by receiver as order initiator_12")
    receivable_order_list_page.all_item_select.click()
    receivable_order_list_page.input_received_remarks(
        receiving_remarks="Received remarks test 123 !@# for initiator partially received item 6")
    receivable_order_list_page.open_item_receive_popup()
    receivable_order_list_page.confirm_receivable_order()
    receivable_order_list_page.wait_for_timeout(5000)

    item_receive_list_page = ItemReceivedList(page)
    item_receive_list_page.searched_received_order(
        challan_no="Partially item receive by receiver as order initiator_12")
    item_receive_list_page.get_full_page_screenshot('full_page_screenshot_60')
    item_receive_list_page.search_button_for_received_item.click()
    item_receive_list_page.order_view_button.click()
    item_receive_list_page.wait_for_timeout(5000)

    dm_logout = MainNavigationMenu(page)
    dm_logout.logout_from_administration()


def test_14_login_to_procurement_and_view_item_receive_details(page):
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
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_61')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_item_receive_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_62')

    proc_item_receive_list_page = ProcItemReceiveListPage(page)
    proc_item_receive_list_page.search_item_receive_order(receivable_item="BPD/2025/FO-2936")
    # proc_item_receive_list_page.search_item_receive_order(receivable_item=framework_order_no)
    proc_item_receive_list_page.item_receive_details_view()
    # new_page = new_tab(lambda p: proc_item_receive_list_page.item_receive_details_view())
    # new_page.close()

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_')


def test_15_login_to_procurement_and_vendor_bill_creation(page):
    print("Test 15: Bill creation flow for Marketplace item receive in procurement system...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=proc_admin,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_63')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_bill_payable()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_64')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_')
