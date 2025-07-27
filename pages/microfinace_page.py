from utils.basic_actions import BasicActions


class MicrofinancePage(BasicActions):
    def __init__(self, page):
        super().__init__(page)

        self.member = page.locator('//*[@id="wrapper"]/ul/li[5]/div')
        self.member1 = page.locator('//*[@id="wrapper"]/ul/li[5]/ul/li[1]/div/span')
        self.membersetup = page.locator('//*[@id="wrapper"]/ul/li[5]/ul/li[1]/ul/li[1]/a/span')

    def goto_membersetup_page(self) -> None:
       self.click_on_btn(self.member)
       self.click_on_btn(self.member1)
       self.click_on_btn(self.membersetup)


