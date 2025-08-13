# this page contains all the common actions to be performed in this project
from playwright.sync_api import expect
import os
from typing import Optional


def is_element_visible(elem):
    return elem.is_visible()


class BasicActions:
    def __init__(self, page):
        self.page = page

    def get_screen_shot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots/" + name + ".png")

    def get_full_page_screenshot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots_taken/" + name + ".png", full_page=True)

    def navigate_to_url(self, given_url):
        self.page.goto(given_url, wait_until="networkidle", timeout=60000)

    def verify_by_title(self, title):
        expect(self.page).to_have_title(title)

    def press_button(self, btnName):
        self.page.keyboard.press(btnName)

    def wait_for_timeout(self, timeout):
        self.page.wait_for_timeout(timeout)

    @staticmethod
    def wait_to_load_element(elem):
        elem.wait_for(state='visible')
        # print('waited for the elem')

    @staticmethod
    def click_on_btn(btn):
        btn.click()

    @staticmethod
    def click_on_btn(btn, timeout: Optional[int] = 5000):
        btn.wait_for(state='visible', timeout=timeout)
        btn.click()

    @staticmethod
    def input_in_element(elem, input_text):
        # elem.to_be_visible()
        elem.click()
        elem.fill(input_text)

    @staticmethod
    def select_from_list_by_value(elem, value):
        elem.click()
        elem.select_option(value)

    def select_from_list_by_text(self, elem, text):
        elem.wait_for(state='visible')
        self.page.wait_for_timeout(500)
        elem.fill(text)
        # Add a wait for the dropdown to appear
        self.page.wait_for_selector(f'div:text-matches("{text}", "i")', state='visible')
        # Use get_by_text with exact match and wait for it to be visible
        text_locator = self.page.get_by_text(text, exact=True)
        text_locator.wait_for(state='visible', timeout=3000)
        text_locator.click()

    def select_from_dropdown(self, elem, text):
        elem.click()
        self.page.get_by_text(text, exact=True).click()
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)

    def select_option_from_dropdown(self, elem, text):
        elem.wait_for(state='visible')
        elem.click()
        elem.fill(text)
        # Wait for the dropdown options to appear
        self.page.wait_for_selector(f'div:text-matches("{text}", "i")', state='visible')
        # Click on the first matching option
        self.page.get_by_text(text).click()

    def clear_browser_cache(self):
        try:
            origin = self.page.evaluate("location.origin")
            self.page.evaluate("localStorage.clear(); sessionStorage:clear();")
            cdp = self.page.context.new_cdp_session(self.page)
            cdp.send(
                "Storage.clearDataForOrigin",
                {
                    "origin": origin,
                    "storageTypes": ",".join([
                        "cookies",
                        "local_storage",
                        "session_storage",
                        "indexeddb",
                        "cache_storage",
                        "service_workers"
                    ])
                }
            )

            self.page.context.clear_cookies()
            self.page.context.clear_permissions()
        except Exception as e:
            print(f"⚠️ Failed to clear cache: {e}")