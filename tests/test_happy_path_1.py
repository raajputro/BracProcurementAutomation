# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.erp_procurement.dashboard_page import DashboardPage
from pages.erp_procurement.login_page import LoginPage
from resources.resource_file import TestResources
from playwright.sync_api import sync_playwright
from pages.erp_procurement.procurement_page_navigation_bar import ProcurementPageNavigationBar
from pages.erp_procurement.create_direct_purchase import CreateDirectPurchase
from pages.erp_procurement.direct_purchase_list import DirectPurchaseList

# Variables used to run this test
purchase_order_number = ''

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
    s_page  = LoginPage(resource)
    s_page.navigate_to_url(TestResources.test_url)
    s_page.perform_login(
        user_name=TestResources.test_user_name,
        pass_word=TestResources.test_user_pass
    )
    #s_page.get_screen_shot('modular_test_1')

def test_two(resource):
    print("Test Two")
    r_page = DashboardPage(resource)
    try:
        r_page.closing_add()
        r_page.goto_procurement()
        r_page.get_full_page_screenshot('modular_test_2')
    except Exception as e:
        r_page.get_full_page_screenshot('test_2_error')
        raise e

def test_three(resource):
    r_page = ProcurementPageNavigationBar(resource)
    try:
        r_page.click_purchase_order()
        r_page.click_direct_purchase()
        r_page.click_create_direct_purchase()
        r_page.get_full_page_screenshot('modular_test_3')
    except Exception as e:
        r_page.get_full_page_screenshot('test_3_error')
        raise e
    
# def test_four(resource): 
#     r_page = CreateTenderInitiation(resource)
#     try:
        
#         r_page.search_requisition(TestResources.test_requisition_number)
#         r_page.select_all_items()
#         r_page.select_direct_purchase_method()
#         r_page.fill_remarks("This is a test remark for the tender initiation.")
#         r_page.submit_tender_initiation()
#         r_page.confirm_submission()
#         # r_page.get_full_page_screenshot('modular_test_7')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_4_error')
#         raise e

def test_four(resource):
    r_page = CreateDirectPurchase(resource)
    try:
        r_page.search_vendor(TestResources.test_vendor_name)
        r_page.same_delivery_schedule()
        r_page.estimated_delivery_date_with_text("24/11/2026")
        r_page.delivery_location_dropdown_select()
        # r_page.delivery_location_Other()
        r_page.delivery_location("Dhaka, Bangladesh")
        r_page.search_item_by_name(TestResources.test_requisition_number)
        r_page.select_all_items()
        r_page.save_and_next()
        global purchase_order_number
        purchase_order_number = r_page.get_purchase_order_number()
        print("Ord number:", purchase_order_number)
        r_page.template_selection()
        r_page.direct_purchase_approver_selecting(TestResources.test_purchase_approver)
        r_page.submit_direct_purchase()
        r_page.confirm_submission()
        r_page.get_full_page_screenshot('modular_test_4')
    except Exception as e:
        r_page.get_full_page_screenshot('test_4_error')
        raise e
print("xyzPurchase Order Number:", purchase_order_number)
    
def test_five(resource):
    r_page = DirectPurchaseList(resource)
    try:
        print("DPL Ord number:", purchase_order_number)
        r_page.search_purchase_order(purchase_order_number)
        # r_page.select_direct_purchase_order()
        # r_page.approve_direct_purchase()
        # r_page.confirmation_message_approve()
        # r_page.get_full_page_screenshot('modular_test_5')
    except Exception as e:
        r_page.get_full_page_screenshot('test_5_error')
        raise e


# def test_two(resource):
#     d_page = DashboardPage(resource)
#     d_page.goto_procurement()
#     #d_page.get_screen_shot('modular_test_2')

# def test_three(resource):
#     p_page = ProcurementHomePage(resource)
#     p_page.navigate_to_create_requisition()
#     #p_page.get_screen_shot('modular_test_3')

# def test_four(resource):
#     c_page = CreateRequisitionPage(resource)
#     try:
#         c_page.verify_by_title("Create Requisition")
#         #c_page.get_screen_shot('modular_test_4')
#         c_page.select_requisition_for_self()
#         c_page.input_project_name("[H04] - Procurement-BRAC")
#         c_page.input_source_of_fund("BRAC")
#         c_page.input_item_information("[19190]-Glue-(Supplies and Stationeries->Supplies and Stationeries->Stationery)", "BAG")
#         c_page.wait_for_timeout(10000)
#         c_page.input_item_quantity("10")
#         c_page.input_item_unit_price("100")
#         c_page.set_delivery_schedule()
#         c_page.set_requisition_details()        # Providing GL details also
#         c_page.wait_for_timeout(5000)
#         c_page.get_full_page_screenshot('modular_test_5')
#         c_page.add_item_to_grid()
#         c_page.get_full_page_screenshot('modular_test_6')
#         c_page.save_requisition()
#         #c_page.confirm_submit_requisition()
#         c_page.get_full_page_screenshot('modular_test_7')
#         c_page.wait_for_timeout(5000)
#         c_page.track_requisition_number()
#         c_page.get_full_page_screenshot('modular_test_8')
#     except Exception as e:
#         c_page.get_full_page_screenshot('test_four_error')
#         raise e
# def test_five(resource):
#     r_page = RequisitionApproveList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
#         r_page.search_requisition(r_page.requisition_number)
#         r_page.select_requisition()
#         r_page.approve_requisition()
#         r_page.confirmation_message_aprrove()
#         r_page.get_full_page_screenshot('modular_test_10')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_four_error')
#         raise e


# def test_six(resource):
#     r_page = RequisitionApproveList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
#         r_page.search_requisition(r_page.requisition_number)
#         r_page.navigate_to_requisition_detail_page()
#         r_page.approve_requisition_from_details_page()
#         r_page.get_full_page_screenshot('modular_test_11')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_four_error')
#         raise e
# <<<<<<< HEAD
# def test_seven(resource):
#     r_page = AssignRequisition(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/assignRequisitions")
#         r_page.assigning_person(assigned_person=TestResources.test_requisition_assignee)
#         r_page.search_requisition_for_assigning(requisition_number=TestResources.test_requisition_number)
#         r_page.add_item_to_assign()
#         r_page.get_full_page_screenshot('modular_test_12')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_12_error')
#         raise e
# =======
# def test_seven(resource):
#     print("Test Seven")
#     r_page = AssignRequisition(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/assignRequisitions")
#         r_page.assigning_person(assigned_person=TestResources.test_requisition_assignee)
#         r_page.search_requisition_for_assigning(requisition_number=TestResources.test_requisition_number)
#         r_page.add_item_to_assign()
#         r_page.get_full_page_screenshot('modular_test_12')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_12_error')
#         raise e
# >>>>>>> 1b94c398858621bbb62e2556c3ce5cd90f000609
    
# def test_eight(resource):
#     r_page = RequisitionAcceptList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/dashboard#!/requisition/assignedRequisitionShowList")
#         r_page.search_requisition(requisition_number=TestResources.test_requisition_number)
#         r_page.select_all_requisitions()
#         r_page.accept_requisition()
#         r_page.confirm_acceptance()
#         r_page.get_full_page_screenshot('modular_test_12')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_12_error')
#         raise e
    
# def test_nine(resource):
#     r_page = MainNavigationBar(resource)
#     try:
#         r_page.exit()
#         r_page.logout()
#         r_page.get_full_page_screenshot('modular_test_12')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_12_error')
#         raise e
        
