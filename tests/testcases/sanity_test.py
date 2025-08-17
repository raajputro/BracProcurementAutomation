from dotenv import load_dotenv
import os
import re
import random
from conftest import new_tab

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
delivery_location = os.getenv("test_delivery_location")
receiving_pin = os.getenv("test_receiving_pin")
# order_approver = os.getenv("test_order_approver")
order_admin = os.getenv("test_order_admin")
manual_delivery_location = os.getenv("test_manual_delivery_location")
dm_user_gen_password = os.getenv("test_dm_user_gen_password")
agreement = os.getenv("test_white_listed_agreement")
login_credential_for_receiver = os.getenv("test_login_credential_for_receiver")
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
from pages.digital_marketplace.administration import Administration
from pages.digital_marketplace.all_order_for_admin import AllOrderForAdminPage
from pages.digital_marketplace.order_management import OrderManagement
from pages.digital_marketplace.receivable_order_list import ReceivableOrderListPage
from pages.digital_marketplace.item_received_list import ItemReceivedList

# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install

install()
order_reference_number = ''
# vendor_name = ''
order_vendor = ''
framework_order_no = ''
vendor_login_id = ''

req_num = ''
approver_id = ''
approver_id_2 = ''
order_approver = ''
approver_id_3 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
bill_num = str(random.randint(10000, 99999))


def test_1_login_to_create_and_submit_requisition(page):
    s_page = ProcurementLoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass
    )

    # def test_2_go_to_procurement_page(page):
    d_page = DashboardPage(page)
    d_page.goto_procurement()
    d_page.get_full_page_screenshot('full_page_screenshot_1')

    # def test_3_navigate_to_create_req_from_proc_dashboard(page):
    p_page = ProcurementHomePage(page)
    p_page.navigate_to_create_requisition()
    p_page.get_full_page_screenshot('full_page_screenshot_2')
    # p_page.wait_for_timeout(7500)

    # def test_4_create_and_submit_requisition(page):
    print("Test 1: Creating requisition...")
    c_page = CreateReqPage(page)
    # c_page.validate()
    c_page.setting_requisition_for("[H10] - Construction")
    c_page.setting_requisition_information("BRAC Fund", "Remarks for funding")
    c_page.setting_requisition_details("pen",
                                       "[22245]-Pen Box-(Supplies and Stationeries->Supplies and Stationeries->Stationery)")

    c_page.active_agreement_button.click()
    c_page.setting_active_framework_list(agreement_info="BPD/2024/FA-93")
    c_page.agreement_item_selector.nth(0).click()
    c_page.finalize_item_quantity(item_quantity="100")
    # c_page.wait_for_timeout(7500)
    c_page.setting_requisition_for_details("[1202010501-01] Furniture and Fixture", "Item remarks abc123@")
    c_page.setting_same_schedule_for_date()
    c_page.setting_location_for_head_office(address="Gulshan 1, Head Office, Dhaka - 1200")
    c_page.get_full_page_screenshot('full_page_screenshot_3')
    global req_num
    req_num = c_page.submit_requisition()
    print("REQ NUM:", req_num)
    c_page.navigate_to_requisition_list()
    c_page.get_full_page_screenshot('full_page_screenshot_4')


def test_2_find_approver_of_the_requisition(page):
    print("Test 2: Finding approver of the requisition...")
    r1_page = RequisitionList(page)
    r1_page.get_full_page_screenshot('full_page_screenshot_5')
    r1_page.search_requisition(req_num)

    global approver_id
    approver_id = str(int(r1_page.find_approver_id()))
    print("APPROVER ID:", approver_id)
    r1_page.get_full_page_screenshot('full_page_screenshot_6')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_7')
    m_page.wait_for_timeout(2000)


def test_3_login_as_approver_and_approve_requisition(page):
    print("Test 3: Logging in as approver and approving requisition...")
    s_page = ProcurementLoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=approver_id,
        # user_name="9026",
        pass_word=proj_pass,
        timeout=60000  # Increased timeout for login
    )

    # def test_7_approver_goto_procurement(page):
    d_page = DashboardPage(page)
    # d_page.close_modal.click()
    d_page.menu_click_procurement_hyperlink()

    # def test_8_approver_goto_procurement_and_approve(page):
    p_page = ProcurementHomePage(page)
    p_page.navigate_to_requisition_approve_list()

    r2_page = RequisitionApproveList(page)
    r2_page.get_full_page_screenshot('full_page_screenshot_8')
    r2_page.search_requisition(req_num)
    # r2_page.search_requisition(requisition_number="REQ20250014472")
    r2_page.select_requisition()
    r2_page.approve_requisition()
    r2_page.get_full_page_screenshot('full_page_screenshot_9')
    r2_page.wait_for_timeout(2000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_10')
    m_page.wait_for_timeout(2000)


def test_4_find_approver_of_the_requisition_2(page):
    print("Test 4: Finding approver of the requisition again...")
    s_page = ProcurementLoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        # user_name="6008",
        user_name=proj_user,
        pass_word=proj_pass,
        timeout=60000
    )
    d_page = DashboardPage(page)
    d_page.goto_procurement()

    p_page = ProcurementHomePage(page)
    p_page.navigate_to_requisition_list()

    r1_page = RequisitionList(page)
    r1_page.get_full_page_screenshot('full_page_screenshot_11')
    r1_page.search_requisition(req_num)
    # r1_page.search_requisition(requisition_number="REQ20250014472")
    global approver_id_2, order_approver
    global order_approver
    order_approver = r1_page.find_approver_id()
    approver_id_2 = str(int(r1_page.find_approver_id()))
    print("APPROVER ID 2:", approver_id_2)
    r1_page.get_full_page_screenshot('full_page_screenshot_12')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_13')
    m_page.wait_for_timeout(2000)


def test_5_login_as_approver_2_and_approve_requisition(page):
    print("Test 5: Logging in as second approver and approving requisition...")
    s_page = ProcurementLoginPage(page)
    # s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        given_url=proj_url,
        user_name=approver_id_2,
        # user_name="155790",
        pass_word=proj_pass,
        timeout=60000  # Increased timeout for login
    )
    d_page = DashboardPage(page)
    d_page.goto_procurement()

    p_page = ProcurementHomePage(page)
    p_page.navigate_to_requisition_approve_list()

    r2_page = RequisitionApproveList(page)
    r2_page.get_full_page_screenshot('full_page_screenshot_14')
    r2_page.search_requisition(req_num)
    # r2_page.search_requisition(requisition_number="REQ20250014472")
    r2_page.select_requisition()
    r2_page.approve_requisition()
    r2_page.get_full_page_screenshot('full_page_screenshot_15')
    r2_page.wait_for_timeout(2000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_16')
    # m_page.wait_for_timeout(2000)


def test_6_check_requisition_approved(page, new_tab):
    print("Test 6: Checking requisition status after approval...")
    s_page = ProcurementLoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name="6008",
        # user_name=proj_user,
        pass_word=proj_pass,
        timeout=60000
    )
    d_page = DashboardPage(page)
    d_page.goto_procurement()

    p_page = ProcurementHomePage(page)
    p_page.navigate_to_requisition_list()

    r1_page = RequisitionList(page)
    # r1_page.search_requisition(req_num)
    r1_page.search_requisition(requisition_number="REQ20250014472")
    req_status = r1_page.find_requisition_status()
    print("REQ STATUS:", req_status)
    # expect(req_status).to_be_equal("Approved")
    # r1_page.goto_requisition_details_information()
    # r1_page.requisition_no.nth(0).click()

    new_page = new_tab(lambda p: r1_page.goto_requisition_details_information())
    req_details = RequisitionDetailsInformation(new_page)
    # req_details.fa_no_hyperlink.nth(0).click()
    req_details.wait_for_timeout(2000)

    new_page_2 = new_tab(lambda p: req_details.fa_no_hyperlink.nth(0).click())
    framework_info = FrameworkInformation(new_page_2)

    global order_vendor
    order_vendor = framework_info.get_vendor_info()
    framework_info.wait_for_timeout(2000)
    new_page_2.close()

    req_details.wait_for_timeout(2000)
    new_page.close()

    r1_page = RequisitionList(page)
    r1_page.wait_for_timeout(5000)

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_16')


# Marketplace flow
# Order initiation
def test_11_order_initiation(page):
    login_page = LoginPage(page)
    login_page.navigate_to_url(marketplace_url_qa)
    login_page.perform_login_for_common_login(
        # user_name="0000"+order_initiator,
        user_name="0000" + proj_user,
        pass_word=marketplace_password
    )
    home_page = HomePage(page)
    home_page.verify_welcome_message()
    home_page.wait_for_timeout(2000)
    home_page.goto_shopping_cart()

    cart_page = ShoppingCart(page)
    # cart_page.select_vendor_for_requisition("REQ20250014490")
    # cart_page.select_vendor_for_requisition("REQ20250014417")
    # cart_page.select_vendor_for_requisition(requisition_number="REQ20250014472")
    cart_page.select_vendor_for_requisition_2(requisition_number="REQ20250014472")
    # cart_page.select_order_vendor(vendor="Plan for demand")
    # cart_page.select_order_vendor(vendor=vendor_name)
    cart_page.wait_for_timeout(2000)
