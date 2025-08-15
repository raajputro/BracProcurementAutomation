from linecache import clearcache
from pickletools import string1

from dotenv import load_dotenv
import os
import random

load_dotenv()

proc_url = os.getenv("test_url")
proc_user = os.getenv("test_user_name")
proc_pass = os.getenv("test_user_pass")
marketplace_url_stg = os.getenv("test_marketplace_url_stg")
marketplace_url_qa = os.getenv("test_marketplace_url_qa")
order_initiator = os.getenv("test_order_initiator")
marketplace_password = os.getenv("test_marketplace_password")
req_num = os.getenv("test_req_num")
review_req_num = os.getenv("test_review_req_num")

delivery_location = os.getenv("test_delivery_location")
receiving_pin = os.getenv("test_receiving_pin")
order_approver = os.getenv("test_order_approver")
order_admin = os.getenv("test_order_admin")
manual_delivery_location = os.getenv("test_manual_delivery_location")
dm_user_gen_password = os.getenv("test_dm_user_gen_password")
agreement = os.getenv("test_white_listed_agreement")
login_credential_for_receiver = os.getenv("test_login_credential_for_receiver")

# order_reference_number = os.getenv("test_order_reference_number")

# proj_gen_pass = os.getenv("test_user_generic_pass")
# admin_user = os.getenv("test_admin")
# assigned_person = os.getenv("test_requisition_assignee")
# # vendor_name = os.getenv("test_vendor_name")
# dp_approver = os.getenv("test_dp_approver")
# bill_creator = os.getenv("test_bill_creator")

# Page models
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
# from pages.digital_marketplace.item_received_list import ReceivableItemListPage
from pages.digital_marketplace.administration import Administration
from pages.digital_marketplace.all_order_for_admin import AllOrderForAdminPage
from pages.digital_marketplace.order_management import OrderManagement
from pages.digital_marketplace.receivable_order_list import ReceivableOrderListPage
from pages.digital_marketplace.item_received_list import ItemReceivedList
from pages.digital_marketplace.orders_public_store import OrdersPublicStore

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
approver_id = ''
approver_id_2 = ''
purchase_num = ''
challan_num = str(random.randint(10000, 99999))
bill_num = str(random.randint(10000, 99999))


# Order initiation
def test_1_order_initiation(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=order_initiator,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_shopping_cart()

    s_page = ShoppingCart(page)
    s_page.remove_vendor_item()
    s_page.goto_home_page()

    s_page = HomePage(page)
    s_page.go_to_active_requisition_list()

    s_page = ActiveRequisitionListPage(page)
    s_page.search_order_requisition_number(requisition_number=review_req_num)
    s_page.navigate_to_url(
        "https://qamarketplace.bracits.com/Requisition/ActiveRequisitionProductList?requisitionId=3694")

    s_page = ActiveRequisitionProductList(page)
    s_page.add_to_cart_button.nth(0).click()
    s_page.wait_for_timeout(2000)
    s_page.add_to_cart_button.nth(1).click()

    s_page.goto_shopping_cart()

    # Cart update and checkout info. setting for order initiation
    # def test_2_update_cart_to_goto_checkout_page_and_confirm_order(page):
    s_page = ShoppingCart(page)

    global order_vendor
    order_vendor = s_page.select_vendor()

    s_page.item_remarks_update_for_multiple_items()
    s_page.update_shopping_cart_info()
    s_page.update_cart_value_for_multiple_items()
    s_page.update_shopping_cart_info()
    s_page.cart_page_checkout()
    s_page.wait_for_timeout(2000)
    s_page = CheckoutPage(page)
    # s_page.delivery_schedule_preparation(location=delivery_location)
    # s_page.fillup_receiving_pin()
    s_page.delivery_schedule_preparation_item_1(location=delivery_location, pin=receiving_pin)
    s_page.delivery_schedule_preparation_item_2(location=delivery_location, pin=receiving_pin)
    s_page.click_checkout()
    s_page.fillup_order_remarks()
    s_page.select_terms_of_service()

    global order_reference_number
    order_reference_number = s_page.confirm_order()
    print("Global order_reference_number", order_reference_number)
    s_page.wait_for_timeout(2000)
    s_page.goto_public_side_order_details_view()
    s_page.wait_for_timeout(2000)

    s_page = MainNavigationMenu(page)
    s_page.perform_logout()


def test_2_order_review_action(page):
    s_page = LoginPage(page)
    # s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=order_approver,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_order_list()
    s_page.goto_pending_approval_orders_list()

    s_page = PendingApprovalOrders(page)
    s_page.search_order_input(
        reference_number=order_reference_number
    )
    s_page.click_order_search_button()
    s_page.view_pending_order_info_toggle()
    s_page.goto_pending_approval_order_details()
    s_page.wait_for_timeout(2000)
    s_page.open_review_popup()
    s_page.check_review_mandatory_validation()
    s_page.check_minimum_characters_validation()
    s_page.check_max_min_characters_validation()
    s_page.confirm_order_review()
    s_page.wait_for_timeout(2000)

    s_page = MainNavigationMenu(page)
    s_page.perform_logout()


def test_3_edit_review_order(page):
    s_page = LoginPage(page)
    # s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=order_initiator,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_order_list()
    s_page = OrdersPublicStore(page)
    # s_page.search_order_no_or_reference_no(order_no="2025/TRN-2746")
    s_page.search_order_no_or_reference_no(order_no=order_reference_number)
    s_page.order_info_view_by_toggle()
    s_page.view_order_details()
    s_page.goto_administration()
    s_page.wait_for_timeout(2000)

    s_page = OrderManagement(page)
    s_page.order_management_menu.click()
    s_page.orders_submenu.click()
    s_page.wait_for_timeout(2000)
    s_page.search_order(order_no=order_reference_number)
    s_page.order_details_view()
    s_page.wait_for_timeout(2000)
    s_page.edit_review_button.click()
    s_page.wait_for_timeout(2000)

    s_page = ShoppingCart(page)
    s_page.item_remarks_update_for_review_order()
    s_page.update_shopping_cart_info()
    s_page.update_cart_value_for_review_order()
    s_page.update_shopping_cart_info()
    s_page.cart_page_checkout()
    s_page.wait_for_timeout(2000)

    s_page = CheckoutPage(page)
    # s_page.delivery_schedule_preparation(location=delivery_location)
    # s_page.fillup_receiving_pin()
    s_page.schedule_delete_icon.nth(0).click()
    s_page.wait_for_timeout(2000)
    s_page.update_delivery_location_for_review_order_item_1()
    # s_page.wait_for_timeout(2000)
    s_page.update_receiving_person_info_for_review_order(pin=receiving_pin)
    s_page.wait_for_timeout(2000)
    s_page.schedule_edit_button.nth(1).click()
    s_page.wait_for_timeout(2000)
    s_page.update_delivery_schedule_for_review_order()
    s_page.update_delivery_location_for_review_order_item_2()
    s_page.update_schedule_button.nth(1).click()
    s_page.wait_for_timeout(2000)
    s_page.add_remaining_schedule_item_for_review_order(pin=order_initiator)
    s_page.wait_for_timeout(2000)
    s_page.click_add_schedule_button.nth(1).click()
    s_page.wait_for_timeout(2000)
    s_page.click_checkout()
    s_page.wait_for_timeout(2000)
    s_page.fillup_order_remarks_for_review_order()
    s_page.select_terms_of_service()
    s_page.confirm_order()

    s_page = MainNavigationMenu(page)
    s_page.perform_logout()


# Order approver flow
def test_4_order_approver_action(page):
    s_page = LoginPage(page)
    s_page.perform_login_for_common_login(
        user_name=order_approver,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_order_list()
    s_page.goto_pending_approval_orders_list()

    s_page = PendingApprovalOrders(page)
    s_page.search_order_input(
        reference_number=order_reference_number
    )
    s_page.click_order_search_button()
    s_page.view_pending_order_info_toggle()
    s_page.goto_pending_approval_order_details()
    s_page.approve_order()

    s_page = MainNavigationMenu(page)
    s_page.perform_logout()


# Find vendor username
def test_4_find_vendor_info_for_order(page):
    s_page = LoginPage(page)
    # s_page.navigate_to_url(marketplace_url)
    s_page.perform_login_for_common_login(
        user_name=order_admin,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_all_orders_for_admin()

    s_page = AllOrderForAdminPage(page)
    s_page.admin_order_search(
        search_number=order_reference_number
    )
    s_page.admin_goes_to_order_details()
    s_page.goto_admin_dashboard()
    # s_page.wait_for_timeout(5000)

    s_page = Customers(page)
    s_page.view_customers_list()
    # s_page.wait_for_timeout(5000)
    s_page.search_vendor(customer_name=order_vendor)
    s_page.wait_for_timeout(5000)

    global vendor_login_id
    vendor_login_id = s_page.search_customers()
    print("Global vendor login ID:", vendor_login_id)
    # s_page.wait_for_timeout(2000)

    s_page = MainNavigationMenu(page)
    s_page.logout_from_administration()


# Vendor acknowledgment flow
def test_5_vendor_acknowledgement(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=vendor_login_id,
        pass_word=dm_user_gen_password
    )
    s_page = Administration(page)
    s_page.goto_dashboard()
    s_page.dashboard_heading()

    s_page = OrderManagement(page)
    s_page.goto_administration_order_list()
    # Use if needed for open search grid
    # s_page.open_search_grid()
    s_page.search_order(order_no=order_reference_number)
    s_page.order_details_view()
    s_page.wait_for_timeout(2000)

    global framework_order_no
    framework_order_no = s_page.confirmation_acknowledgment_by_yes()
    print("Generate framework order number", framework_order_no)

    s_page = MainNavigationMenu(page)
    s_page.logout_from_administration()


# Receiver receives all assigned items
def test_6_item_receive_by_assigned_receiver(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=login_credential_for_receiver,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_administration()
    s_page.wait_for_timeout(2000)

    s_page = OrderManagement(page)
    s_page.click_order_management_menu()

    s_page = ReceivableOrderListPage(page)
    s_page.goto_receivable_order_list()
    # s_page.search_receivable_order(receivable_order_number=framework_order_no)
    s_page.search_receivable_order(receivable_order_number="BPD/2025/FO-2797")
    s_page.receivable_order_view()
    s_page.challan_no_input(fill_challan_no="All item received for receiver")
    s_page.all_item_select.click()
    s_page.wait_for_timeout(2000)
    s_page.input_received_remarks(receiving_remarks="Item received by receiver")
    s_page.open_item_receive_popup()
    s_page.confirm_button.click()
    s_page.wait_for_timeout(2000)

    s_page = ItemReceivedList(page)
    # s_page.search_received_order(received_order_number=framework_order_no)
    s_page.search_received_order(received_order_number="BPD/2025/FO-2797")
    s_page.received_order_view()

    s_page.wait_for_timeout(5000)
    s_page = MainNavigationMenu(page)
    s_page.logout_from_administration()


# Order initiator receives remaining assigned items
def test_7_item_receive_by_initiator(page):
    s_page = LoginPage(page)
    s_page.navigate_to_url(marketplace_url_qa)
    s_page.perform_login_for_common_login(
        user_name=order_initiator,
        pass_word=marketplace_password
    )
    s_page = HomePage(page)
    s_page.goto_administration()
    s_page.wait_for_timeout(2000)

    s_page = OrderManagement(page)
    s_page.click_order_management_menu()
    s_page = ReceivableOrderListPage(page)
    s_page.goto_receivable_order_list()
    # s_page.search_receivable_order(receivable_order_number=framework_order_no)
    s_page.search_receivable_order(receivable_order_number="BPD/2025/FO-2798")
    s_page.receivable_order_view()
    challan_number_for_initiator = "BPD/2025/FO-2798"
    s_page.challan_no_input(fill_challan_no=challan_number_for_initiator)
    s_page.all_item_select.click()
    s_page.wait_for_timeout(2000)
    s_page.input_received_remarks(receiving_remarks="Item received by initiator")
    s_page.open_item_receive_popup()
    s_page.confirm_button.click()
    s_page.wait_for_timeout(2000)

    # Search received item by challan no. and view details
    s_page = ItemReceivedList(page)

    s_page.searched_received_order(challan_no=challan_number_for_initiator)
    s_page.search_button_for_received_item.click()
    s_page.wait_for_timeout(2000)
    s_page.received_order_view()
    s_page.wait_for_timeout(2000)

    # s_page.wait_for_timeout(5000)
    # s_page = MainNavigationMenu(page)
    # s_page.logout_from_administration()

# # Settled order info. view from public store for admin user
# def test_9_order_details_view_for_admin(page):
#     s_page = HomePage(page)
#     s_page.goto_all_orders_for_admin()
#
#     s_page = AllOrderForAdminPage(page)
#     s_page.admin_order_search(
#         search_number=order_reference_number
#     )
#     s_page.view_order_info_for_admin()
#     s_page.admin_goes_to_order_details()
#
#     s_page = MainNavigationMenu(page)
#     s_page.perform_logout()
#
#
# # Settled order info. view from public store
# def test_10_order_details_view_for_order_initiator(page):
#     s_page = LoginPage(page)
#     s_page.perform_login_for_common_login(
#         user_name=order_initiator,
#         pass_word=marketplace_password
#     )
#     s_page = HomePage(page)
#     s_page.goto_order_list()
#
#     s_page = OrdersPublicStore(page)
#     s_page.search_order_no_or_reference_no(order_no=framework_order_no)
#     s_page.order_info_view_by_toggle()
#     s_page.view_order_details()
#
#     s_page = MainNavigationMenu(page)
#     s_page.perform_logout()
