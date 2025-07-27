from utils.basic_actions import BasicActions


class DashboardPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.myDashboardItem_modal = page.locator('id=modal')        
        self.myDashboardItem_HRM= page.locator('xpath=//*[contains(text(),"HRM")]')
        self.myDashboardItem_ePMS = page.locator('xpath=//*[contains(text(),"ePMS")]')
        self.myDashboardItem_EDMS = page.locator('xpath=//*[contains(text(),"EDMS")]')
        self.myDashboardItem_procurement = page.locator('xpath=//*[contains(text(),"PROCUREMENT")]')
        self.myDashboardItem_eTender = page.locator('xpath=//*[contains(text(),"E-Tender")]')
        self.myDashboardItem_Marketplace = page.locator('xpath=//*[contains(text(),"Marketplace")]')
        self.myDashboardItem_FIXEDASSET = page.locator('xpath=//*[contains(text(),"FIXED ASSET")]')

        self.myDashboardItem_MICAROFINANCE = page.locator('//*[@id="module-mf"]/a')


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

    def goto_procurement(self) -> None:
        self.page.keyboard.press('Enter')
        self.click_on_btn(self.myDashboardItem_procurement)

    def goto_microfinance(self) -> None:
       self.page.keyboard.press('Enter')
       self.click_on_btn(self.myDashboardItem_MICAROFINANCE)
