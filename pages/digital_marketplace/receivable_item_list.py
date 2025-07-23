
from pages.digital_marketplace.home_page import HomePage
from utils.basic_actionsdm import BasicActionsDM

class ReceivableItemListPage(HomePage, BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        self.page = page



