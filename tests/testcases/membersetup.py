# this page contains all the test cases for the samplePage
#from resources.resource_file import TestResources
import os
from dotenv import load_dotenv

from pages.memberSetup import MemberSetupPage
from pages.microfinace_page import MicrofinancePage

load_dotenv()

proj_url = os.getenv("test_url")
proj_user = os.getenv("test_user_name")
proj_pass = os.getenv("test_user_pass")

# Page models
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


# Import for beautiful reporting
from rich.traceback import install
install()


def test_one(page):
    s_page  = LoginPage(page)
    s_page.navigate_to_url(proj_url)
    s_page.perform_login(
        user_name=proj_user,
        pass_word=proj_pass
    )




def test_two(page):
    d_page = DashboardPage(page)
    d_page.goto_microfinance()
    d_page.get_full_page_screenshot('microfinance')
    p_page = MicrofinancePage(page)
    p_page.goto_membersetup_page()
    q_page =MemberSetupPage(page)
    actual_text=q_page.create_member("[60] - Progoti","Female")
    q_page.get_full_page_screenshot('member_setup')
    assert "Show Member" in actual_text




