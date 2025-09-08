# this page contains all the test cases for the samplePage
from resources.resource_file import TestResources
from pages.erp_procurement.create_requisition_page import CreateRequisitionPage
from pages.erp_procurement.login_page import LoginPage
from resources.resource_file import TestResources

from rich.traceback import install
install()

tr = TestResources()
def test_one(page):    
    print("TR:", tr.practice_value)
    s_page  = LoginPage(page)
    try:
        s_page.navigate_to_url(TestResources.test_url)
        s_page.perform_login(
            user_name=TestResources.test_user_name,
            pass_word=TestResources.test_user_pass
        )
        tr.practice_value = "112BRAC"
    except Exception as e:
        s_page.get_full_page_screenshot('test_one_error')
        raise e
    #s_page.get_screen_shot('modular_test_1')

# def test_two(resource):
#     d_page = DashboardPage(resource)
#     d_page.goto_procurement()
# #     #d_page.get_screen_shot('modular_test_2')
#
# def test_three(resource):
#     p_page = ProcurementHomePage(resource)
#     p_page.navigate_to_create_requisition()
#     #p_page.get_screen_shot('modular_test_3')

def test_four(page):
    c_page = CreateRequisitionPage(page)    
    print("RT:", tr.practice_value)
    try:
        c_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/create")
        c_page.verify_by_title("Create Requisition")
        c_page.get_screen_shot('modular_test_4')
        c_page.set_requisition_for_HO_and_project(
            True,
            "[H04] - Procurement-BRAC")
        c_page.set_requisition_information(
            "BRAC",#"112BRAC",
            "requisition remarks")
        c_page.set_requisition_details(
            "[19190]-Glue-(Supplies and Stationeries->Supplies and Stationeries->Stationery)",
            "BAG",
            "10",
            "150")
        c_page.wait_for_timeout(10000)
        c_page.set_requisition_project_delivery_schedule(
            "[5102010107-05] Remuneration",
            "05-07-2025",
            "Central Store")
        c_page.wait_for_timeout(5000)
        #c_page.get_full_page_screenshot('modular_test_5')

        c_page.add_item_to_grid()
        #c_page.get_full_page_screenshot('modular_test_6')

        c_page.save_requisition()
        c_page.get_full_page_screenshot('modular_test_7')
        #c_page.wait_for_timeout(5000)

        #c_page.track_requisition_number()
        #c_page.get_full_page_screenshot('modular_test_8')
    except Exception as e:
        c_page.get_full_page_screenshot('test_four_error')
        raise e

# def test_five(resource):
#     r_page = RequisitionApproveList(resource)
#     try:
#         r_page.navigate_to_url("https://env28.erp.bracits.net/procurementDashboard/myDashboard#!/requisition/authorizationList")
#         r_page.search_requisition("REQ20250004335")
#         r_page.select_requisition()
#         r_page.approve_requisition()
#         r_page.get_full_page_screenshot('modular_test_10')
#     except Exception as e:
#         r_page.get_full_page_screenshot('test_five_error')
#         raise e
