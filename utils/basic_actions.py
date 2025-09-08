# this page contains all the common actions to be performed in this project
from playwright.sync_api import expect
import os
import re
from typing import Optional
from pathlib import Path


def is_element_visible(elem):
    return elem.is_visible()


class BasicActions:
    def __init__(self, page):
        self.page = page
        self.main_nav = self.page.locator('//*[@class="top_nav_container"]')

    def navigate_to_page(self, main_nav_val, sub_nav_val):
        # Navigate via Main Nav
        self.main_nav.get_by_text(main_nav_val).click()
        self.page.wait_for_timeout(5000)

        '''Sub menu level is 2, then we go from parent to first child'''
        try:
            # Navigate to Parent Sub Menu
            parent_item = self.page.locator(
                f'xpath=//li[@class="menu-parent"]/div[contains(text(),"{sub_nav_val[0]}")]')
            self.wait_to_load_element(parent_item)
            parent_item.click()
            if len(sub_nav_val) == 3:
                sub_item_1 = self.page.locator(
                    f'xpath=//li[@class="sub_arrow"]//child::div/span[text()="{sub_nav_val[1]}"]').first
                sub_item_2 = self.page.get_by_role("link", name=sub_nav_val[2])
                self.wait_to_load_element(sub_item_1)
                sub_item_1.hover()
                self.wait_to_load_element(sub_item_2)
                sub_item_2.click()
            elif len(sub_nav_val) == 2:
                sub_item_1 = self.page.get_by_role("link", name=sub_nav_val[1])
                self.wait_to_load_element(sub_item_1)
                sub_item_1.click()
            else:
                print(f"Please check your sec_menu list and update it properly!")

            self.page.wait_for_timeout(5000)
            self.get_full_page_screenshot(f"{main_nav_val} Navigation Success")
            print(f"{main_nav_val} Navigation Success!!")
        except Exception as e:
            print(f"Missing {e}")

    def get_screen_shot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots/" + name + ".png")

    def get_full_page_screenshot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots_taken/" + name + ".png", full_page=True)

    def navigate_to_url(self, given_url):
        # self.page.goto(given_url, wait_until="networkidle", timeout=120000)
        self.page.goto(given_url, wait_until='domcontentloaded')

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


    def upload_file(self, container, file_path: str, index: int = 0, timeout: int = 30000):
        """
        Uploads a file using the hidden input inside #selector_fileId_{index}
        and waits until the corresponding hidden field is populated.
        """
        p = Path(file_path).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")

        # file_input = self.page.locator(f"#selector_fileId_{index} input[type='file']")
        file_input = self.page.locator(f"{container} input[type='file']")
        file_input.wait_for(state="attached", timeout=timeout)

        # This bypasses the OS dialog and triggers the 'change' event.
        file_input.set_input_files(str(p))

        # App-specific confirmation: hidden field should get a non-empty value.
        index = int(container.split("_")[-1])
        hidden_after_upload = self.page.locator(f"#fileHiddenId_{index}")
        expect(hidden_after_upload).to_have_value(re.compile(r".+"), timeout=timeout)

        # Optional: return what the app stored (filename / token, etc.)
        return hidden_after_upload.input_value()

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