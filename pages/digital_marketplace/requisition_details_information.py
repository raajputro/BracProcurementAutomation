import re

from utils.basic_actionsdm import BasicActionsDM


class RequisitionDetailsInformation(BasicActionsDM):

    def __init__(self, page, logger=None):
        super().__init__(page)

        self.page = page
        self.logger = logger
        self.fa_no_hyperlink = page.locator('a[style="text-decoration: underline;"][onclick^="showFrameworkDetails("]')

    ##################### small helper so we can log easily #####################
    def _log(self, message: str):
        if self.logger:
            self.logger.step(message)
