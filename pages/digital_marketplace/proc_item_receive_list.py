from pages.digital_marketplace.procurement_home_page import ProcurementHomePage
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import expect


class ProcItemReceiveListPage(ProcurementHomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)

        self.search_input = page.get_by_placeholder("Search Number.")
        self.search_icon = page.locator('//*[@id="layout-body-ajax"]/div[1]/div/div/h3/div/div[2]')

        self.mrr_no_hyperlink = page.locator('a[onclick^="gotItemList"]')

    def search_item_receive_order(self, receivable_item):
        self.click_on_btn(self.search_input)
        self.input_in_element(self.search_input, receivable_item)
        self.click_on_btn(self.search_icon)
        self.wait_for_timeout(2000)

    # Main code
    def item_receive_details_view_1(self):
        mrr_no = self.page.locator("//td[@title and starts-with(@title, 'MRR-')]/a")
        print("Count total item received:" + str(mrr_no.count()))
        for i in range(mrr_no.count()):
            print(mrr_no.nth(i).inner_text())
            self.click_on_btn(self.mrr_no_hyperlink.nth(i))
            self.wait_for_timeout(2000)

    def item_receive_details_view(self):
        mrr_no_links = self.page.locator("//td[@title and starts-with(@title, 'MRR-')]/a")
        total_links = mrr_no_links.count()
        print("Count total item received:", total_links)

        for i in range(total_links):
            mrr_text = mrr_no_links.nth(i).inner_text()
            print(mrr_text)

            # Wait for new tab to open
            with self.page.context.expect_page() as new_page_info:
                mrr_no_links.nth(i).click()

                new_page = new_page_info.value
                new_page.wait_for_load_state("domcontentloaded")

                print(f"Opened MRR details for the item receive: {mrr_text}")

                # do something in new tab if needed...
                self.wait_for_timeout(2000)

                # Close the new tab
                new_page.close()
                print(f"Closed the item receive tab for: {mrr_text}")

            # Switch back to the original list page
            self.page.bring_to_front()
