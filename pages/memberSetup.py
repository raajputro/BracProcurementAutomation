import random
from faker import Faker
from utils.basic_actions import BasicActions


class MemberSetupPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)


        self.nationalid = page.locator('//*[@id="nationalId"]')
        self.projectname = page.locator('//*[@id="project_info_id"]')
        self.assigned_po= page.locator('//*[@id="assignedPO"]')
        self.category = page.locator('//*[@id="memberClassificationId"]')
        self.firstname = page.locator('//*[@id="fName"]')
        self.gender = page.locator('//*[@id="personalInfoDomainGenderId"]')
        self.Marital_Status = page.locator('//*[@id="personalInfoDomainMaritalStatusId"]')
        self.dateofbirth  = page.locator('//*[@id="personalInfoInstanceDateOfBirth"]')
        self.occupation = page.locator('//*[@id="personalInfoDomain.occupationId"]')
        self.fathername = page.locator('//*[@id="memberFatherName"]')
        self.mothername= page.locator('//*[@id="memberMotherName"]')
        self.mobilenumbe= page.locator('//*[@id="contactNo"]')
        self.address = page.locator('//*[@id="address_0"]')
        self.district = page.locator('//*[@id="city_0Div_input"]')
        self.thana = page.locator('//*[@id="thana_0Div_input"]')
        self.zipcode = page.locator('//*[@id="zipCode_0"]')
        self.permanent = page.locator('//*[@id="isSameAsPresentAddress"]')
        self.savingsproduct = page.locator('//*[@id="savingsProductId"]')
        self.target_amount = page.locator('//*[@id="targetAmount"]')
        self.savebtn = page.locator('//*[@id="saveButtonId" and @value="Save"]')
        self.validation= page.locator('//*[@id="layout-body-ajax"]/div[1]/div/div[1]/h1/span')


    def create_member(self,project_code,gender):

        first_digit = random.randint(1, 9)
        remaining_digits = random.randint(10 ** 15, (10 ** 16) - 1)
        num = int(str(first_digit) + str(remaining_digits))
        print(num)
        fake = Faker()
        self.page.wait_for_timeout(3000)

        self.input_in_element(self.nationalid,str(num))
        self.select_from_list_by_value( self.projectname, project_code)

        self.select_from_list_by_value(self.assigned_po, "[00144880] Md Imdadul Haque")
        self.select_from_list_by_value(self.category, "General Member")

        self.input_in_element(self.firstname, fake.name())
        self.select_from_list_by_value(self.gender, gender)

        self.select_from_list_by_value(self.Marital_Status,"Single")
        self.input_in_element(self.dateofbirth, "01-02-1991")
        self.page.locator("body").click()
        self.select_from_list_by_value(self.occupation,"Service")
        self.input_in_element(self.fathername, fake.name())
        self.input_in_element(self.mothername, fake.name())
        self.input_in_element(self.mobilenumbe, "01689493234")
        self.input_in_element(self.address, "Dhanmondi")
        self.input_in_element(self.district,"Dhaka" )
        self.page.keyboard.press("Enter")
        self.page.keyboard.press("Enter")
        self.input_in_element(self.thana, "Dhanmondi")
        self.page.keyboard.press("Enter")
        self.page.keyboard.press("Enter")

        self.input_in_element(self.zipcode, "1207")
        self.click_on_btn(self.permanent)
        self.select_from_list_by_value(self.savingsproduct, "General Savings")
        self.input_in_element(self.target_amount,"9000")
        self.click_on_btn(self.savebtn)
        self.page.wait_for_timeout(3000)

        v= self.validation.inner_text()
        print(v)

        return v






