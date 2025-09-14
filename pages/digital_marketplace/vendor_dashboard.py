from symtable import Class

from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM


class VendorDashboard(HomePage, BasicActionsDM):
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

        self.card_title = page.locator("div#pending-acknowledgement-report-card h3.card-title")
        self.table_rows = page.locator("#pending-acknowledgement-report-grid tbody tr")
        self.table = page.locator("table#pending-acknowledgement-report-grid")

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

    def print_card_title(self):
        self.card_title.wait_for(state="visible", timeout=5000)
        print("Card title:", self.card_title.inner_text())

    def print_table_data(self):
        rows = self.table_rows.all()
        if not rows:
            print("No records found in the table")
        else:
            for idx, row in enumerate(rows, start=1):
                print(f"Row {idx}:", row.inner_text())

    # Click action for order details view
    def click_action_for_order(self, order_reference: str, action: str = "View") -> bool:
        row = self.table.locator("tbody tr", has_text=order_reference)
        if row.count() == 0:
            print(f"Order reference '{order_reference}' not found in table.")
            return False

        action_button = row.locator("a", has_text=action)

        if action_button.count() == 0:
            print(f"'{action}' button not found for order '{order_reference}'.")
            return False

        action_button.click()
        print(f"Clicked '{action}' button for order '{order_reference}'")
        return True


