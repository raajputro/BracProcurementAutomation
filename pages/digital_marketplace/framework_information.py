import re

from utils.basic_actionsdm import BasicActionsDM


class FrameworkInformation(BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)

        self.page = page
        self.vendor_info = page.locator('//*[@id="proposal-process"]/div[1]/div/div[4]/div/div/div[2]')

    def get_vendor_info(self):
        vendor = self.vendor_info.inner_text()
        vendor_name = vendor.split(":")[0].strip()
        print("Requisition vendor name: " + vendor_name)
        return vendor_name
