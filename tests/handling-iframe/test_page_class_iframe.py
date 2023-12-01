import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import os
import sys
from os import environ
from pyppeteer import connect, launch

exec_platform = os.getenv('EXEC_PLATFORM')

test_url = 'https://www.lambdatest.com/selenium-playground/iframe-demo/'

# Selectors of the page

# Simple iFrame containing Editor
loc_iframe_1 = "#iFrame1"
# Use class name to select an element
loc_iframe_inside_con = ".rsw-ce"
test_message = "LambdaTest is an awesome platform!"
loc_bold_button = "#__next > div > div.rsw-toolbar > button:nth-child(1)"
loc_underline_button = "//span[.='𝐔']"

# Simple iFrame containing webpage
loc_iframe_2 = "//*[@id='iFrame2']"
loc_playwright_testing = "//a[.='Playwright Testing']"

async def scroll_to_element(page, element):
    # Scroll until the element is detected
    await page.evaluateHandle(
        '''async (element) => {
            if (element) {
                element.scrollIntoView();
            }
        }'''
    )

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
async def test_handling_iframe_1(page):
    await page.goto(test_url)
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    asyncio.sleep(2)

    # Get the iframe element handle
    iframe_handle = await page.querySelector(loc_iframe_1)

    # Switch to the iframe
    iframe = await iframe_handle.contentFrame()
    
    # Locate the Search button in the iFrame
    # Perform actions inside the iframe
    elem_text_box = await iframe.querySelector(loc_iframe_inside_con)

    # Get the element inside the view
    await elem_text_box.click()

    await asyncio.sleep(1)

    await elem_text_box.click(clickCount=3)
    await page.keyboard.press('Backspace')

    # Wait for 2000 ms
    await iframe.waitFor(2000)

    await elem_text_box.type(test_message)
    await asyncio.sleep(2)
    await elem_text_box.click(clickCount=3)

    elem_underline_button = await iframe.waitForXPath(loc_underline_button)
    elem_bold_button = await iframe.querySelector(loc_bold_button)
    await asyncio.sleep(1)
    await elem_underline_button.click()
    await asyncio.sleep(1)
    await elem_bold_button.click()
    await asyncio.sleep(1)

    await elem_text_box.click()

    # Switch back to the main frame if needed
    await page.bringToFront()

    await asyncio.sleep(2)

    # Take a screenshot
    await page.screenshot({'path': 'iFrame1-screenshot.png'})

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_handling_iframe_2(page):
    await page.goto(test_url)
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    asyncio.sleep(2)

    # Get the iframe element handle
    iframe_handle = await page.waitForXPath(loc_iframe_2)

    # Switch to the iframe
    iframe = await iframe_handle.contentFrame()
    
    # Locate the Search button in the iFrame
    # Perform actions inside the iframe
    elem_search = await iframe.waitForXPath(loc_playwright_testing)

    # Get the element inside the view
    await scroll_to_element(iframe, elem_search)
    await elem_search.click()

    await asyncio.sleep(2)

    # Take a screenshot
    await page.screenshot({'path': 'iFrame2-screenshot.png'})