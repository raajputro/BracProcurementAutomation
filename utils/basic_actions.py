# this page contains all the common actions to be performed in this project
from datetime import datetime, timedelta
import os
import re
from typing import Optional
from pathlib import Path
from playwright.sync_api import expect
from datetime import datetime
import time


def is_element_visible(elem):
    return elem.is_visible()


class BasicActions:
    def __init__(self, page):
        self.page = page
        self.main_nav = self.page.locator('//*[@class="top_nav_container"]')

    def validate_heading(self, validation_point, element_name: str):
            """
            Validates if the given locator is visible.
            Prints the element text if visible, otherwise prints the given element_name
            and the current visible heading.
            """
            try:
                expect(validation_point).to_be_visible()
                element_text = validation_point.text_content()
                visible_name = element_text.strip() if element_text else element_name
                print(f"✅ Validation passed: '{visible_name}' is visible.")
            except Exception as e:
                # Try to get the current visible heading
                try:
                    current_heading = self.page.get_by_role("heading").first.text_content()
                    current_heading = current_heading.strip() if current_heading else "No heading found"
                except Exception:
                    current_heading = "No heading found"

                print(f"❌ Validation failed: '{element_name}' is not visible on the page.")
                print(f"🔹 Current visible heading: '{current_heading}'")
                print(f"Error details: {e}")


    def print_important_toast(self, toast_msg: str):
        """
        Print a toast message in bold, with a yellow highlight and black text.
        This makes it highly visible in terminal or console outputs.
        """
        highlight = "\033[1m\033[30m\033[103m"  # Bold + black text + bright yellow background
        reset = "\033[0m"

        print(f"{highlight} 🔔 {toast_msg} 🔔 {reset}")


    def select_date(self,extra_days: int = 0) -> str:
        # Get current date and add extra days
        new_date = datetime.now().date() + timedelta(days=extra_days)
        # Format to 'DD-MM-YYYY' as required by the input field
        return new_date.strftime('%d-%m-%Y')
    
    def wait_until(self, target_time_str: str):
        """Wait until the given time before proceeding."""
        target_time = datetime.strptime(target_time_str, "%d-%m-%Y %I:%M %p")
        now = datetime.now()
        seconds_to_wait = (target_time - now).total_seconds()

        if seconds_to_wait > 0:
            print(f" Waiting {int(seconds_to_wait)} seconds until: {target_time_str}")
            time.sleep(seconds_to_wait)
        else:
            print(f" Opening time {target_time_str} already passed or is now.")


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
                sub_item_2 = self.page.get_by_role("link", name=sub_nav_val[2], exact=True)
                if sub_item_1.is_visible():
                # self.wait_to_load_element(sub_item_1)
                    sub_item_1.hover()
                if sub_item_2.is_visible():
                # self.wait_to_load_element(sub_item_2)
                    sub_item_2.click()
                else:
                    print(f"Please check your sec_menu list and update it properly!")
            elif len(sub_nav_val) == 2:
                sub_item_1 = self.page.get_by_role("link", name=sub_nav_val[1], exact=True)
                if sub_item_1.is_visible:
                    # .wait_to_load_element(sub_item_1)
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

    # @staticmethod
    # def input_in_element(elem, input_text):
    #     # elem.to_be_visible()
    #     elem.click()
    #     elem.fill(input_text)
    @staticmethod
    def input_in_element(elem, input_text, field_name):
        """
        Inputs text into the given element after ensuring it is visible.
        Prints which field was filled.
        """
        try:
            expect(elem).to_be_visible(timeout=5000)
            elem.click()
            elem.fill(input_text)
            print(f"✅ {field_name}: '{input_text}'")
        except TimeoutError as te:
            print(f"❌ Timeout Error: {field_name} field not visible. Details: {te}")
            raise te
        except Exception as e:
            print(f"❌ Error while entering text in {field_name}. Details: {e}")
            raise e

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

    # def select_option_from_dropdown(self, elem, text):
    #     elem.wait_for(state='visible')
    #     elem.click()
    #     elem.fill(text)
    #     # Wait for the dropdown options to appear
    #     self.page.wait_for_selector(f'div:text-matches("{text}", "i")', state='visible')
    #     # Click on the first matching option
    #     self.page.get_by_text(text).click()

    # def select_option_from_dropdown(self, elem, value, field_name):
    #     """
    #     Selects an option from a searchable dropdown.
    #     Types the given value, waits for matching options, and selects it.
    #     Prints clear messages for success, missing options, or errors.
    #     """
    #     try:
    #         expect(elem).to_be_visible(timeout=5000)
    #         elem.click()
    #         elem.type(value)
    #         print(f"✅ Typed '{value}' into {field_name} dropdown.")

    #         # Wait briefly for dropdown options to load
    #         self.page.wait_for_timeout(1000)

    #         options = self.page.locator(f"div:text-matches('{value}', 'i')")
    #         count = options.count()

    #         if count == 0:
    #             print(f"⚠️ No matching option found for '{value}' in {field_name} dropdown.")
    #             return

    #         option = options.first
    #         expect(option).to_be_visible(timeout=5000)
    #         option.click()
    #         print(f"✅ {field_name} selected: '{value}'")

    #     except TimeoutError as te:
    #         print(f"❌ Timeout Error: Could not select '{value}' in {field_name} dropdown. Details: {te}")
    #         raise te
    #     except Exception as e:
    #         print(f"❌ Error while selecting value in {field_name} dropdown. Details: {e}")
    #         raise e
    from playwright.sync_api import expect, TimeoutError

    def select_option_from_dropdown(self, elem, value, field_name):
        """
        Selects the first matching option from a searchable dropdown.
        Steps:
        1. Clicks and types into the dropdown input.
        2. Waits for suggestions to appear.
        3. Selects the first matching suggestion.
        4. Prints detailed logs for success or failure.

        Args:
            elem: Playwright locator for the dropdown input element.
            value (str): The text value to search/select.
            field_name (str): The field label (for logging clarity).
        """
        try:
            print(f"➡ Step: Selecting '{value}' from {field_name} dropdown")

            # Ensure the input is visible and focusable
            expect(elem).to_be_visible(timeout=5000)
            elem.click()
            elem.fill("")  # Clear previous text if any
            elem.type(value)
            print(f"✅ Typed '{value}' into {field_name} dropdown.")

            # Try to find matching options (retry 3 times if slow UI)
            option_found = False
            for attempt in range(3):
                options = self.page.get_by_text(value, exact=False)
                count = options.count()
                if count > 0:
                    option_found = True
                    break
                self.page.wait_for_timeout(500)  # small retry delay

            if not option_found:
                print(f"⚠️ No data found named: '{value}' in {field_name} dropdown.")
                return

            # Select the first matching option
            first_option = options.first
            expect(first_option).to_be_visible(timeout=5000)
            option_text = first_option.inner_text().strip()
            first_option.click()

            print(f"✅ {field_name} selected: '{option_text}'")

        except TimeoutError:
            print(f"❌ Timeout Error: Could not select '{value}' in {field_name} dropdown.")
            raise
        except Exception as e:
            print(f"❌ Error while selecting value in {field_name} dropdown. Details: {e}")
            raise


    def upload_file(self, container, file_path: str, index: int = 0, timeout: int = 120000):
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