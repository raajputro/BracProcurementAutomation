# this page contains all the test cases for the samplePage
import os
import random
from conftest import new_tab

# For validation
# from playwright.sync_api import expect

# Import for beautiful reporting
from rich.traceback import install
install()

from dotenv import load_dotenv
load_dotenv()

#======================================================================================================================
#======================================================================================================================
# Project URLs
proj_url = os.getenv("test_url")
requisition_list_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/list"
requisition_approve_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/authorizationList"
requisition_assign_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignRequisitions"
requisition_accept_url = proj_url + "/procurementDashboard/myDashboard#!/requisition/assignedRequisitionShowList"
tender_initiation_url = proj_url + "/procurementDashboard/myDashboard#!/methodSelection/show"
direct_purchase_url = proj_url + "/procurementDashboard/myDashboard#!/directPurchase/show"
direct_purchase_list_url = proj_url + "/procurementDashboard/myDashboard#!/directPurchase/list"
item_receive_url = proj_url + "/procurementDashboard/myDashboard#!/itemReceive/show"
vendor_bill_payable_url = proj_url + "/procurementDashboard/myDashboard#!/thirdPartyBillPayable/show"
bill_payable_url = proj_url + "/procurementDashboard/myDashboard#!/thirdPartyBillPayable/billList"

#======================================================================================================================
# # Environment Data
proj_user = "ahsan.habib" # os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")
proj_gen_pass = os.getenv("test_user_generic_pass")
admin_user = os.getenv("test_admin")
assigned_person = os.getenv("test_requisition_assignee")
vendor_name = os.getenv("test_vendor_name")
dp_approver = os.getenv("test_dp_approver")
bill_creator = os.getenv("test_bill_creator")


#======================================================================================================================
#======================================================================================================================
# Page models
from pages.login_page import LoginPage



def test_1_navigate(page):
    s_page  = LoginPage(page)
    s_page.perform_login(
        given_url=proj_url,
        user_name=proj_user,
        pass_word=proj_pass
    )
    s_page.get_full_page_screenshot("Login Complete")
    sec_menu = ["Member", "Member", "Member Setup"]
    # s_page.navigate_to_page(main_nav_val="Microfinance", sub_nav_val = sec_menu)
    s_page.navigate_to_page(main_nav_val="Microfinance", sub_nav_val=sec_menu)
    s_page.get_full_page_screenshot("Navigating to Microfinance")

    sec_menu = ["Requisition", "Requisition Assign", "Requisition Accept List"]
    # s_page.navigate_to_page(main_nav_val="Microfinance", sub_nav_val = sec_menu)
    s_page.navigate_to_page(main_nav_val="Procurement", sub_nav_val=sec_menu)
    s_page.get_full_page_screenshot("Navigating to Procurement")

    s_page.perform_logout()
    s_page.get_full_page_screenshot("Logout Complete")

