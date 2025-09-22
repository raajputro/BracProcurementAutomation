from dotenv import load_dotenv
import os
import re
import random
import string
from conftest import new_tab
from datetime import datetime, timedelta

from pages.digital_marketplace.bill_list import BillList

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
from pages.digital_marketplace.framework_order_list import FrameworkOrderListPage
from pages.digital_marketplace.proc_item_receive_list import ProcItemReceiveListPage

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

# For validation
from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install

install()
order_reference_number = ''
framework_order_no = ''
vendor_login_id = ''
# order_number = ''

req_num = ''
approver_id = ''
approver_id_2 = ''
order_vendor = ''
# order_approver = ''
approver_id_3 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
challan_num_for_receiver = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
challan_num_for_order_initiator = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
challan_num_for_order_initiator_2 = ''.join(random.choices(string.ascii_letters, k=8))
bill_num = str(random.randint(10000, 99999))
bill_recommender1 = ''
bill_recommender2 = ''
bill_approver_id = ''


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
    home_page.get_full_page_screenshot('full_page_screenshot_52')
    home_page.wait_for_timeout(2000)

    order_list = OrderManagement(page)
    order_list.click_order_management_menu()

    receivable_order_list_page = ReceivableOrderListPage(page)
    receivable_order_list_page.goto_receivable_order_list()
    current_date = datetime.today().strftime("%d-%m-%Y")
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
    current_date = datetime.today().strftime("%d-%m-%Y")
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


def test_13_item_receive_by_order_initiator_as_receiver(page):
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
    current_date = datetime.today().strftime("%d-%m-%Y")
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
    current_date = datetime.today().strftime("%d-%m-%Y")
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
    current_date = datetime.today().strftime("%d-%m-%Y")
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
    document_location = os.path.join(current_dir, "utils", "zip.zip")
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
    current_date = datetime.today().strftime("%d-%m-%Y")
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
