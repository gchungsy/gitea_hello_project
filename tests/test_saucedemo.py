import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://saucedemo.com/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Swag Labs"))

def test_get_started_link(page: Page):
    page.goto("https://saucedemo.com/")

    # Click the get started link.
    page.locator('input[name="user-name"]').fill("standard_user")
    page.locator('input[name="password"]').fill("secret_sauce")
    page.locator('input[name="login-button"]').click()
    page.screenshot(path="save_home_screen.png")
    # Expects page to have a heading with the name of Installation.
    # expect(page.get_by_role("heading", name="Installation")).to_be_visible()
    page.locator('button[name="add-to-cart-sauce-labs-backpack"]').click()
    page.screenshot(path="save_click_backpack.png")