from symtable import Class

from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class Administration(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.dashboard = page.locator('i[class="nav-icon fas fa-desktop"]')

        # write down all the elements here with locator format
        self.acknowledge_button = page.locator("a.btn.btn-default", has_text="Acknowledge")
        self.yes_button = page.locator("button[onclick='acknowledgeSubmit()']")

        self.send_back_button = page.locator("a.btn.btn-default", has_text="Send Back")
        self.reasons_textarea = page.locator("textarea[name='reasons']")
        self.submit_send_back_button = page.get_by_role("button", name="Send Back")

    def dashboard_heading(self):
        heading = self.page.locator("h1").first.text_content()
        # text = heading
        print(heading)
        self.wait_for_timeout(2000)

    def goto_dashboard(self):
        self.dashboard.click()

    def click_vendor_acknowledge(self, order_reference_no):
        # self.input_in_element(self.acknowledge_button, order_reference_no).click()
        self.acknowledge_button.click()
        self.yes_button.click()
        self.wait_for_timeout(5000)

    def click_vendor_send_back(self, send_back_reasons):
        self.send_back_button.click()
        self.input_in_element(self.reasons_textarea, send_back_reasons)
        self.submit_send_back_button.click()
        self.wait_for_timeout(5000)
