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

# Fixture is handled as a part of conftest.py
# The below code is added for reference, in case browser and page fixture 
# has to be setup without the usage of conftest.py
# Pytest fixture for browser setup
# @pytest.fixture(scope='function')
# async def browser():
#     if exec_platform == 'local':
#         browser = await launch(headless = False, args=['--start-maximized'])
#     yield browser
#     await asyncio.sleep(1)    
#     await browser.close()

# # Pytest fixture for page setup
# @pytest.fixture(scope='function')
# async def page(browser):
#     page = await browser.newPage()
#     yield page
#     await page.close()

# Documentation Link
# https://miyakogi.github.io/pyppeteer/reference.html#dialog-class

# Interesting reference question
# https://stackoverflow.com/questions/75622322/why-dialog-popup-alert-doesnt-dismiss-as-they-claim-by-using-pyppeteer-class

# Scenario Handling Alerts
dialog_test_url = 'https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo'

# Locators for different elements
# 0 - JS Alert
# 1 - Confirm Box
# 2 - Prompt Box

loc_alert_arr =  ['.my-30',
                '.py-20.ml-10 .btn',
                'section:nth-of-type(2) div:nth-of-type(3) .btn']

test_message = 'LambdaTest is a great platform!'

# Event event listener for handling JS alert dialog box
def handle_js_dialog_box(dialog):
    asyncio.ensure_future(dialog.accept())
    print(f"Dialog message: {dialog.message}")

# Event event listener for handling confirm dialog box
def handle_confirm_accept_dialog_box(dialog):
    asyncio.ensure_future(dialog.accept())
    print(f"Dialog message: {dialog.message}")

# Event event listener for handling confirm dialog box
def handle_confirm_dismiss_dialog_box(dialog):
    asyncio.ensure_future(dialog.dismiss())
    print(f"Dialog message: {dialog.message}")

# Event event listener for handling prompt dialog box
def handle_confirm_prompt_dialog_box(dialog):
    asyncio.ensure_future(dialog.accept(test_message))
    print(f"Dialog message: {dialog.message}")

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_handling_js_alerts(page):
    await page.goto(dialog_test_url)

    # Can be changed with non-blocking sleep
    await asyncio.sleep(1)

    page.on('dialog', handle_js_dialog_box)

    elem_alert = await page.querySelector(loc_alert_arr[0])

    # Click on the located element
    await elem_alert.click()

    # Wait for the event loop to process events
    await asyncio.sleep(2)

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_handling_confirm_accept_alerts(page):
    await page.goto(dialog_test_url)

    # Can be changed with non-blocking sleep
    await asyncio.sleep(1)

    page.on('dialog', handle_confirm_accept_dialog_box)

    # Confirm Alert
    elem_alert = await page.querySelector(loc_alert_arr[1])

    # Click on the located element
    await elem_alert.click()

    # Wait for the event loop to process events
    await asyncio.sleep(2)

@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_handling_confirm_dismiss_alerts(page):
    await page.goto(dialog_test_url)

    # Can be changed with non-blocking sleep
    await asyncio.sleep(1)

    page.on('dialog', handle_confirm_dismiss_dialog_box)

    await asyncio.sleep(2)

    # Dismiss Alert
    elem_alert = await page.querySelector(loc_alert_arr[1])

    # Click on the located element
    await elem_alert.click()

    # Wait for the event loop to process events
    await asyncio.sleep(2)

@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_handling_prompt_alerts(page):
    await page.goto(dialog_test_url)

    # Can be changed with non-blocking sleep
    await asyncio.sleep(1)

    page.on('dialog', handle_confirm_prompt_dialog_box)

    # Prompt Alert
    elem_alert = await page.querySelector(loc_alert_arr[2])

    # Click on the located element
    await elem_alert.click()

    page.on('dialog', handle_confirm_dismiss_dialog_box)

    await asyncio.sleep(2)