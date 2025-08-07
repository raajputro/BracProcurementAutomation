from utils.basic_actionsdm import BasicActionsDM


class DashboardPage(BasicActionsDM):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.myDashboardItem_modal = page.locator('id=modal')        
        self.myDashboardItem_HRM= page.locator('xpath=//*[contains(text(),"HRM")]')
        self.myDashboardItem_ePMS = page.locator('xpath=//*[contains(text(),"ePMS")]')
        self.myDashboardItem_EDMS = page.locator('xpath=//*[contains(text(),"EDMS")]')
        # self.myDashboardItem_procurement = page.locator('xpath=//*[contains(text(),"PROCUREMENT")]')
        self.myDashboardItem_procurement = page.locator('//a[contains(@class, "moreInfoBoxShow") and text()="PROCUREMENT"]')
        self.myDashboardItem_eTender = page.locator('xpath=//*[contains(text(),"E-Tender")]')
        self.myDashboardItem_Marketplace = page.locator('xpath=//*[contains(text(),"Marketplace")]')
        self.myDashboardItem_FIXEDASSET = page.locator('xpath=//*[contains(text(),"FIXED ASSET")]')
        self.myDashboardItem_MICROFINANCE = page.locator('xpath=//*[contains(text(),"MICROFINANCE")]')
        self.myDashboardItem_ACCOUNTING = page.locator('xpath=//*[contains(text(),"ACCOUNTING")]')
        self.myDashboardItem_Budget = page.locator('xpath=//*[contains(text(),"Budget")]')
        self.myDashboardItem_FINANCIALCONSOLIDATION = page.locator('xpath=//*[contains(text(),"FINANCIAL CONSOLIDATION")]')
        self.myDashboardItem_MyBRAC = page.locator('xpath=//*[contains(text(),"My BRAC")]')
        self.myDashboardItem_MyDesk = page.locator('xpath=//*[contains(text(),"My Desk")]')
        self.myDashboardItem_CareersPortal = page.locator('xpath=//*[contains(text(),"Careers Portal")]')
        self.myDashboardItem_eRecruitment = page.locator('xpath=//*[contains(text(),"eRecruitment")]')
        self.myDashboardItem_PERFORMANCEDASHBOARD = page.locator('xpath=//*[contains(text(),"PERFORMANCE DASHBOARD")]')
        self.myDashboardItem_HRAnalyticsDASHBOARD = page.locator('xpath=//*[contains(text(),"HR Analytics ")]')
        self.myDashboardItem_HOFAMS = page.locator('xpath=//*[contains(text(),"HO FAMS")]')
        self.myDashboardItem_MonthlyMFReportingTool = page.locator('xpath=//*[contains(text(),"Monthly MF Reporting Tool")]')
        self.myDashboardItem_BracInventory = page.locator('xpath=//*[contains(text(),"Brac Inventory")]')
        self.add_bannar = page.locator('#modals')

        self.click_procurement_hyperlink = page.locator('a[href="/procurementDashboard/myDashboard"]:has-text("Procurement")')


    def closing_add(self) -> None:
        self.wait_to_load_element(self.add_bannar)
        self.get_full_page_screenshot('add_bannar')   
        self.page.keyboard.press('Enter')
        self.get_full_page_screenshot('add_bannar2')

    def goto_procurement(self) -> None:
        self.click_on_btn(self.myDashboardItem_procurement)

    def menu_click_procurement_hyperlink(self):
        self.click_on_btn(self.click_procurement_hyperlink)