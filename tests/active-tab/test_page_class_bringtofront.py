import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import json
import os
import sys
from os import environ
from pyppeteer import connect, launch

exec_platform = os.getenv('EXEC_PLATFORM')

# # Pytest fixture for browser setup
@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'local':
        browser = await launch(headless = False, args=['--start-maximized'])
    yield browser
    await asyncio.sleep(1)    
    await browser.close()

# Pytest fixture for page setup
@pytest.fixture(scope='function')
async def page(browser):
    page = await browser.newPage()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_bring_to_front(browser, page):
    await page.goto('https://www.duckduckgo.com', {'waitUntil' : 'networkidle2'})
    # Maximize the page
    await page.setViewport({'width': 1920, 'height': 1080})

    element = await page.querySelector('[name="q"]')
    await element.click()
    await element.type('LambdaTest')
    await asyncio.gather(
        page.keyboard.press('Enter'),
        page.waitForNavigation()
    )

    # Use asyncio.sleep within the async test function
    # await asyncio.sleep(1)

    page_title = await page.title()

    try:
        assert page_title == 'LambdaTest at DuckDuckGo', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    
    page_1 = await browser.newPage()
    await page_1.goto('https://www.lambdatest.com', {'waitUntil' : 'networkidle2'})

    await page.bringToFront()
    await asyncio.sleep(2)
