

class NavigationMenu(BaseException):
    def __init__(self, page):
        super().__init__(page)
        self.menu_item_manage = page.locator('css=#manage_menu')