import re
from playwright.sync_api import Playwright, sync_playwright, expect
from resources.resource_file import TestResources


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    rf = TestResources()
    print("Starting the test... with RF value:", rf.practice_value)
    # Perform Login
    page.goto("https://env28.erp.bracits.net/idp/realms/brac/protocol/openid-connect/auth?client_id=erp&redirect_uri=https%3A%2F%2Fenv28.erp.bracits.net&state=dGltZToxNzUxMjg1NDUyOTMwfHVybDpudWxs&response_type=code&scope=openid&kc_idp_hint=")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("197363")
    page.get_by_role("textbox", name="Password").click()    
    page.get_by_role("textbox", name="Password").fill("abc123$")
    page.get_by_role("button", name="Sign In").click()
    # Closing the popup if it appears
    page.locator("//*[@class='close-button']").click()
    # Navigate to Procurement Home Page
    page.get_by_role("link", name="PROCUREMENT", exact=True).click()
    # Navigate to Create Requisition Page
    page.get_by_text("Requisition", exact=True).first.click()
    page.get_by_role("link", name="Create Requisition").click()
    # Actions performed on Create Requisition Page    
    page.locator("#self").check()
    page.locator("#projectInfoDiv_arrow").click()
    page.get_by_text("[H04] - Procurement-BRAC").click()
    page.locator("#sourceOfFundDiv_arrow").click()
    rf.practice_value = "112BRAC"
    print("RF value set to:", rf.practice_value)
    page.get_by_text("112BRAC").click()
    page.get_by_role("textbox", name="Max size of requisition remarks 300 characters").click()
    page.get_by_role("textbox", name="Max size of requisition remarks 300 characters").fill("Some text")
    rf.print_practice_value()
    page.get_by_role("textbox", name="Min 3 characters").click()
    page.get_by_role("textbox", name="Min 3 characters").fill("Glue")
    page.get_by_text("[19190]-Glue-(Supplies and Stationeries->Supplies and Stationeries->Stationery)").click()
    page.locator("#mUnitDiv_arrow").click()
    page.get_by_text("17Pcs").click()
    page.get_by_role("textbox", name="Max size of requisition specification/TOR 2000 characters").click()
    page.get_by_role("textbox", name="Max size of requisition specification/TOR 2000 characters").fill("Glue (any type of glue) some more glue")
    page.locator("#quantity").click()
    page.locator("#quantity").fill("100")
    page.locator("#unitPrice").click()
    page.locator("#unitPrice").fill("25")
    page.locator("#singleProjectRadio").check()
    page.locator("#itemCostQuantity").check()
    page.locator("#itemCostAmount").check()
    page.locator("#glInfo_0Div_arrow").click()
    page.get_by_text("[5102010107-05] Remuneration").click()
    page.get_by_role("textbox", name="Max size of item remarks 500").click()
    page.get_by_role("textbox", name="Max size of item remarks 500").fill("Some remarks")
    page.get_by_role("checkbox", name="Same schedule").check()
    page.get_by_role("img", name="Select date").click()
    page.get_by_role("combobox").nth(1).select_option("6")
    page.locator("#defaultDeliveryDate").select_option("6")
    page.get_by_role("link", name="16").click()    
    page.locator("#defaultDeliveryStoreId").select_option("2")
    page.get_by_role("textbox", name="Note: 1. Address 2. Contact").click()
    page.get_by_role("textbox", name="Note: 1. Address 2. Contact").fill("Dhaka, Bangladesh")
    page.get_by_role("button", name="Add to Grid").click()
    page.get_by_role("button", name="Save").click()
    page.get_by_text("Procurement Requisition", exact=True).click()
    page.get_by_text("Requisition Saved As Draft").click()
    page.get_by_text("×Procurement").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
