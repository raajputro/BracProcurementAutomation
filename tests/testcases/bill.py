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
from pages.digital_marketplace.create_vendor_bill_payable import CreateVendorBillPayable
from pages.digital_marketplace.bill_list import BillList
from pages.digital_marketplace.bill_details import BillDetails

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
bill_recommender1 = ''
bill_recommender2 = ''
bill_approver_id = ''


def test_1_bill_creation_and_submit(page):
    print("Test 15: Bill creation and submission flow for Marketplace item receive in procurement system...")
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

    create_vendor_bill = CreateVendorBillPayable(page)
    create_vendor_bill.vendor_bill_payable_information_for_framework_order()
    # create_vendor_bill.search_vendor(vendor_name=order_vendor)
    create_vendor_bill.search_vendor(vendor_name="Plan for demand")
    # create_vendor_bill.select_order_no(order_num=framework_order_no)
    create_vendor_bill.select_order_no(order_num="BPD/2025/FO-2936")
    # create_vendor_bill.select_challan_no(challan_no=challan_num)
    create_vendor_bill.select_challan_no(challan_no="Partially item receive by receiver as order initiator_6")
    bill_num = "QA_bill_1"
    global bill_num
    create_vendor_bill.bill_number(bill_no_1=bill_num)
    create_vendor_bill.bill_date_with_text(create_vendor_bill.bill_date())
    create_vendor_bill.bill_receive_date_with_text(create_vendor_bill.bill_date())
    create_vendor_bill.select_all_items()

    create_vendor_bill.submit_bill()
    create_vendor_bill.get_full_page_screenshot('full_page_screenshot_65')
    create_vendor_bill.confirm_submission()
    create_vendor_bill.get_full_page_screenshot('full_page_screenshot_66')
    create_vendor_bill.wait_for_timeout(5000)

    bill_list_page = BillList(page)
    bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)
    global bill_recommender1
    bill_recommender1 = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 1: {bill_recommender1}")

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_67')


# bill_recommender1 = '761'
# bill_num = '82824'
def test_16_vendor_bill_recommender1_approval(page, new_tab):
    print("Test 16: Vendor bill recommender1 approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender1,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_68')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_vendor_billing_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_69')

    bill_list_page = BillList(page)
    # main_menu_item = "Procurement"
    # sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    # bill_list_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)

    # # Opening new tab
    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))
    bill_detail_page = BillDetails(new_page)

    # # Preparing document location
    current_dir = os.getcwd()
    # print(f"Current directory: {current_dir}")
    document_location = os.path.join(current_dir, 'utils', 'upload_file.pdf')
    bill_detail_page.upload_document(document_location)

    # print(f"Document directory: {document_location}")

    # #  Continuing rest of the test
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_70')
    bill_detail_page.select_bill_type("Regular")
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_71')
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_72')

    # # Closing new tab
    new_page.close()

    # # Continuing rest of the test in parent tab
    bill_list_page = BillList(page)
    bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)
    global bill_recommender2
    bill_recommender2 = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Recommender 2: {bill_recommender2}")

    # logout from the page
    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_73')


def test_17_vendor_bill_recommender2_approval(page, new_tab):
    print("Test 17: Vendor bill recommender2 approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_recommender2,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_68')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_vendor_billing_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_69')

    bill_list_page = BillList(page)
    # main_menu_item = "Procurement"
    # sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    # bill_list_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)

    # # Opening new tab
    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))
    bill_detail_page = BillDetails(new_page)
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_40')
    new_page.close()

    bill_list_page = BillList(page)
    bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)
    bill_list_page.wait_for_timeout(5000)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_41')
    global bill_approver_id
    bill_approver_id = str(int(bill_list_page.find_approver_id(bill_num)))
    print(f"Bill Approver : {bill_approver_id}")

    # logout from the page
    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_73')


def test_18_vendor_bill_approver_approval(page, new_tab):
    print("Test 18: Vendor bill approver approval...")
    proc_login_page = ProcurementLoginPage(page)
    proc_login_page.perform_login(
        given_url=proj_url,
        user_name=bill_approver_id,
        pass_word=proj_pass,
        timeout=60000
    )

    proc_dashboard_page = DashboardPage(page)
    proc_dashboard_page.goto_procurement()
    proc_dashboard_page.get_full_page_screenshot('full_page_screenshot_68')

    proc_home_page = ProcurementHomePage(page)
    proc_home_page.goto_vendor_billing_list()
    proc_home_page.get_full_page_screenshot('full_page_screenshot_69')

    bill_list_page = BillList(page)
    # main_menu_item = "Procurement"
    # sec__menu_item = ["Bill Payable", "Vendor Billing List"]
    # bill_list_page.navigate_to_page(main_nav_val=main_menu_item, sub_nav_val=sec__menu_item)
    # bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)

    new_page = new_tab(lambda p: bill_list_page.click_on_bill_num(bill_num))
    bill_detail_page = BillDetails(new_page)
    bill_detail_page.wait_for_timeout(5000)
    bill_detail_page.approve_bill()
    bill_detail_page.get_full_page_screenshot('full_page_screenshot_42')
    new_page.close()

    bill_list_page = BillList(page)
    bill_list_page.navigate_to_url(bill_payable_url)
    bill_list_page.search_bill(bill_num)
    bill_list_page.wait_for_timeout(5000)
    bill_status = bill_list_page.find_bill_status(bill_num)
    print("Bill STATUS:", bill_status)
    bill_list_page.get_full_page_screenshot('full_page_screenshot_43')

    m_page = MainNavigationBar(page)
    m_page.exit()
    m_page.logout()
    m_page.get_full_page_screenshot('full_page_screenshot_73')
