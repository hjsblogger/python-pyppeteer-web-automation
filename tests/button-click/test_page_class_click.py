import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import json
import os
import sys
from os import environ
from pyppeteer import connect, launch
sys.path.append(sys.path[0] + "/../..")

exec_platform = os.getenv('EXEC_PLATFORM')

test_url = 'https://ecommerce-playground.lambdatest.io/'
product_url = 'https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=57'

# XPath's of the elements that need to be located on the page

shopcategory = "//a[contains(.,'Shop by Category')]"
megamenu = "//a[contains(.,'Mega Menu')]"
# We could have also used XPath for the same
# phonecategory = "//span[contains(.,'Phone, Tablets & Ipod')]"

phonecategorySelector = '#widget-navbar-217841 > ul > li:nth-child(3) > a > div.info > span'
# Macbook Air product
macbook_locator = '#mz-product-grid-image-44-212408'

# Buy Now button
button_buynow = '.btn-buynow'
target_checkout_url = 'https://ecommerce-playground.lambdatest.io/index.php?route=checkout/checkout'
target_page_str = 'Billing Address'

menu_hover_xpath = "//*[@id='__docusaurus']/nav/div[1]/div[2]/div[1]"

# Pytest fixture for browser setup
# @pytest.fixture(scope='function')
# async def browser():
#     if exec_platform == 'local':
#         browser = await launch(headless = False, args=['--start-maximized'])
#     yield browser
#     await asyncio.sleep(1)    
#     # await browser.close()

# # Pytest fixture for page setup
# @pytest.fixture(scope='function')
# async def page(browser):
#     page = await browser.newPage()
#     yield page
#     # await page.close()

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_click_element(page):
    # await page.goto(test_url)
    await page.goto(test_url,
        {'waitUntil': 'load'})

    # Wait for the 'Shop by Category' menu to be available
    menu_element = await page.waitForXPath(shopcategory)

    # Click on the 'Shop by Category' menu
    await menu_element.click()

    # Can be changed with non-blocking sleep
    await asyncio.sleep(2)

    shop_element = await page.waitForSelector(phonecategorySelector, {'visible': True})

    # Click on the 'Shop by Category' menu
    if exec_platform == 'local':
        await shop_element.click()
    elif exec_platform == 'cloud':
        await asyncio.gather(
            shop_element.click(),
            page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 60000}),
        )

    # Can be changed with non-blocking sleep
    await asyncio.sleep(2)

    page_title = await page.title()

    try:
        assert page_title == "Tablets"
        print("Test Success: Reached the target URL")
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        print("Test Failure: Recheck the URL")
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    await asyncio.sleep(2)

    elem_macbook = await page.waitForSelector(macbook_locator, {'visible': True})

    # Click on the 'Shop by Category' menu
    await elem_macbook.click()

    await asyncio.sleep(2)

    # Click on the Buy Now Button
    elem_buynow = await page.waitForSelector(button_buynow, {'visible': True})
    if exec_platform == 'local':
        await elem_buynow.click()
    elif exec_platform == 'cloud':
        await asyncio.gather(
            elem_buynow.click(),
            page.waitForNavigation({'waitUntil': 'networkidle2'}),
        )

    await asyncio.sleep(2)

    current_url = page.url
    print('Current URL is: ' + current_url)

    try:
        assert current_url == target_checkout_url
        print("Test Success: Product checkout successful")
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        print("Test Failure: Could not checkout Product")
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    await asyncio.sleep(2)

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_get_content(page):
    await page.goto('https://ecommerce-playground.lambdatest.io/')

    await asyncio.sleep(2)

    html_content = await page.content()

    await asyncio.sleep(2)

    assert 'Upto 50% Off on Fully Automatic' in html_content, "Expected string not found in page content"