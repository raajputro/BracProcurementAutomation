# # this page contains all the test cases for the samplePage
# import pytest
# from pages.login_page import LoginPage
# from resources.resource_file import TestResources
# from playwright.sync_api import sync_playwright
#
#
# @pytest.fixture(scope='session', autouse=True)
# def resource():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
#         page.close()
#         context.close()
#         browser.close()
#
#
# def test_one(resource):
#     s_page  = LoginPage(resource)
#     s_page.navigate_to_url(TestResources.test_url)
#     s_page.perform_login(
#         user_name=TestResources.test_user_name,
#         pass_word=TestResources.test_user_pass
#     )
#     s_page.get_screen_shot('modular_test_one')
#
