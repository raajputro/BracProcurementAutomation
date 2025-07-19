# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.digital_marketplace.checkout_page import CheckoutPage
from pages.digital_marketplace.home_page import HomePage
from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.main_navigation_menu import MainNavigationMenu
from pages.digital_marketplace.pending_approval_orders import PendingApprovalOrders
from pages.digital_marketplace.shopping_cart import ShoppingCart
from resources.DMResourceFile import TestResourcesDM
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import sync_playwright

install()


@pytest.fixture(scope='session', autouse=True)
def resource():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()


def test_one(resource):
    print("Test One")
    s_page = LoginPage(resource)
    s_page.navigate_to_url(TestResourcesDM.test_url)
    s_page.perform_login(
        user_name=TestResourcesDM.order_approver_PIN,
        pass_word=TestResourcesDM.order_approver_pass
    )


def test_two(resource):
    print("Test Two")
    r_page = HomePage(resource)
    r_page.goto_order_list()


# Order approval from the pending approval order details page
def test_three(resource):
    print("Test Three")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.search_order_reference_number
    )
    p_page.goto_pending_approval_order_details()
    p_page.approve_order()


# Review the order with a validation check
def test_four(resource):
    print("Test Four")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.search_review_order_reference_number
    )
    p_page.goto_pending_approval_order_details()
    p_page.open_review_popup()
    p_page.check_review_mandatory_validation()
    p_page.check_minimum_characters_validation()
    p_page.remove_review_popup()
    p_page.order_review()


# Preview open for approver
def test_five(resource):
    print("Test Five")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.approver_preview_open
    )
    p_page.goto_pending_approval_order_details()
    p_page.open_preview()


# Order rejection before approval with a validation check
def test_six(resource):
    print("Test Six")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.approver_order_rejection
    )
    p_page.goto_pending_approval_order_details()
    p_page.open_order_rejection_popup()
    p_page.remove_order_rejection_popup()
    p_page.open_order_rejection_popup()
    p_page.check_minimum_characters_validation_for_order_rejection()
    p_page.rejection_max_characters_input()
    p_page.confirm_rejection()


# Single order approval using the searching parameter from the pending approval orders list page
def test_seven(resource):
    print("Test Seven")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.search_order_reference_number
    )
    p_page.check_uncheck_order()
    p_page.confirm_multi_select_approve()


# Multiselect approval from the pending approval orders list page
def test_eight(resource):
    print("Test Eight")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.multi_select_approve1()
    p_page.confirm_multi_select_approve()
