# this page contains all the common actions to be performed in this project
from playwright.sync_api import expect
import os
import re
from typing import Optional
from pathlib import Path


def is_element_visible(elem):
    return elem.is_visible()


class BasicActionsDM:
    def __init__(self, page):
        self.page = page

    # Current working directory = cwd
    def get_screen_shot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots/" + name + ".png")

    def get_full_page_screenshot(self, name):
        self.page.screenshot(path=os.getcwd() + "/screenshots_taken/" + name + ".png", full_page=True)

    def navigate_to_url(self, given_url):
        self.page.goto(given_url, wait_until="networkidle", timeout=60000)

    def press_button(self, btnName):
        self.page.keyboard.press(btnName)

    def wait_for_timeout(self, timeout):
        self.page.wait_for_timeout(timeout)

    def click_requisition_and_interact_with_button(self, url: str, button_locator: str):
        # Click on the requisition hyperlink
        self.page.goto(url)

        # Wait for the hyperlink to be clickable and click on it
        requisition_link = self.page.locator('a[href*="RequisitionList"]')  # Assuming this locator
        requisition_link.click()

        # Wait for the new tab to open
        new_tab = self.page.context.wait_for_event('page')  # Wait for the new tab to open
        new_tab.wait_for_load_state('networkidle')  # Wait until the page is fully loaded

        # Click the button in the new tab using the provided locator
        button = new_tab.locator(button_locator)
        button.click()
        print("Button clicked in new tab")

    def verify_by_title(self, title):
        expect(self.page).to_have_title(title)

    @staticmethod
    def verify_text(self, locator, expected_text):
        # Wait until the text appears and matches
        expect(locator).to_have_text(expected_text)
        # Fetch and print the actual text
        actual_text = locator.text_content().strip()
        print(actual_text)
        return actual_text

    @staticmethod
    def wait_to_load_element(elem):
        elem.wait_for(state='visible')
        # print('waited for the elem')

    @staticmethod
    def click_on_openLoginFormBtn(openLoginFormBtn):
        openLoginFormBtn.click()

    @staticmethod
    def click_on_btn(btn):
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

    # @staticmethod
    def character_input(self, locator, text, delay_ms=200):
        for char in text:
            locator.type(char, delay=delay_ms)

    def select_option_from_dropdown(self, elem, text):
        elem.wait_for(state='visible')
        elem.click()
        elem.fill(text)
        # Wait for the dropdown options to appear
        self.page.wait_for_selector(f'div:text-matches("{text}", "i")', state='visible')
        # Click on the first matching option
        self.page.get_by_text(text).click()

    @staticmethod
    def click_on_btn(btn, timeout: Optional[int] = 5000):
        btn.wait_for(state='visible', timeout=timeout)
        btn.click()

    # @staticmethod
    # def click_on_btn_1(locator):
    #     locator.wait_for(state="visible", timeout=5000)
    #     locator.click()

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

    def wait_for_selector(self, locator, state='visible', timeout=5000):
        """
        Waits for a selector to reach the specified state.

        :param locator: Locator object to wait on.
        :param state: State to wait for. One of: 'attached', 'detached', 'visible', 'hidden'.
        :param timeout: Max time to wait in milliseconds.
        """
        try:
            locator.wait_for(state=state, timeout=timeout)
        except TimeoutError:
            print(f"Timeout: Locator did not become '{state}' within {timeout}ms.")
