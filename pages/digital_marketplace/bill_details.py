import re, os
from utils.basic_actionsdm import BasicActionsDM


class BillDetails(BasicActionsDM):

    def __init__(self, page):
        super().__init__(page)
        self.document_upload_container = "#selector_fileId_0"
        self.bill_type_selector = page.locator('#billTypeId')
        self.approve_button = page.locator("//input[@type='button' and @value='Approve']")
        self.toast_msg = page.locator('//*[@id="jGrowl"]/div[2]/div[3]')

    def upload_document(self, file_path):
        """
        Upload a document to the bill details page.
        :param file_path: Path to the document file to be uploaded.
        """
        print(f"Uploading file from : {file_path}")
        if os.path.exists(file_path):
            uploaded_file_name = self.upload_file(self.document_upload_container, file_path)
            print(f"Uploaded file name: {uploaded_file_name}")
        else:
            print(f"File not found at path: {file_path}")

    def select_bill_type(self, bill_type):
        """
        Select the type of bill from the dropdown.
        :param bill_type: The type of bill to select (e.g., 'Regular', 'Emergency').
        """
        self.bill_type_selector.select_option(bill_type)
        self.page.wait_for_timeout(2000)

    def approve_bill(self):
        """
        Approve the bill.
        """
        self.wait_to_load_element(self.approve_button)
        self.approve_button.click()
        # self.page.wait_for_timeout(2000)
        self.toast_msg.wait_for(state="visible", timeout=10000)
        toast_msg = self.toast_msg.text_content()
        print(toast_msg)
