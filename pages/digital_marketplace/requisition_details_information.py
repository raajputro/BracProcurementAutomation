import re

from utils.basic_actionsdm import BasicActionsDM


class RequisitionDetailsInformation(BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)

        self.page = page
        self.fa_no_hyperlink = page.locator('a[style="text-decoration: underline;"][onclick^="showFrameworkDetails("]')
