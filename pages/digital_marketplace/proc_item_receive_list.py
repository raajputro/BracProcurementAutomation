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

    def item_receive_details_view(self):
        mrr_no = self.page.locator("//td[@title and starts-with(@title, 'MRR-')]/a")
        print("Count total item received:" + str(mrr_no.count()))
        for i in range(mrr_no.count()):
            print(mrr_no.nth(i).inner_text())
            self.click_on_btn(self.mrr_no_hyperlink.nth(i))
            self.wait_for_timeout(2000)
