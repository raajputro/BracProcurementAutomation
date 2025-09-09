from utils.basic_actions import BasicActions


class DashboardPage(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format
        # self.myDashboardItem_modal = page.locator('id=modal')        

        self.myDashboardItem_procurement = page.locator('xpath=//*[contains(text(),"PROCUREMENT")]')
        self.add_bannar = page.locator('#modals')


    def closing_add(self) -> None:
        self.wait_to_load_element(self.add_bannar)
        self.get_full_page_screenshot('add_bannar')   
        self.page.keyboard.press('Enter')
        self.get_full_page_screenshot('add_bannar2')

    def goto_procurement(self) -> None:
        self.click_on_btn(self.myDashboardItem_procurement)