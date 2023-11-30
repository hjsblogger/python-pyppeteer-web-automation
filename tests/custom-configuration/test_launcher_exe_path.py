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

# Can take values - headless and non-headless
chromium_version = os.getenv('CHROMIUM_VERSION')

# Pytest fixture for browser setup
@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'local':
        if chromium_version == '121':
            custom_chrome_path = "mac-chrome/Chromium_121.app/Contents/MacOS/Chromium"
        elif chromium_version == '113':
            custom_chrome_path = "mac-chrome/Chromium_113.app/Contents/MacOS/Chromium"
        else:
            custom_chrome_path = "mac-chrome/Chromium.app/Contents/MacOS/Chromium"
    
    browser = await launch(headless = False,
                executablePath = custom_chrome_path, args=['--start-maximized']) 
    yield browser
    await asyncio.sleep(1)    
    await browser.close()

# Pytest fixture for page setup
@pytest.fixture(scope='function')
async def page(browser):
    page = await browser.newPage()
    yield page
    await page.close()

# Ported code from https://github.com/LambdaTest/puppeteer-sample/blob/main/puppeteer-parallel.js

@pytest.mark.asyncio
async def test_exe_path(page):
    await page.goto('https://www.duckduckgo.com')
    await page.setViewport({'width': 1920, 'height': 1080})

    element = await page.querySelector('[name="q"]')
    await element.click()
    await element.type('LambdaTest')
    await asyncio.gather(
        page.keyboard.press('Enter'),
        page.waitForNavigation()
    )

    page_title = await page.title()

    try:
        assert page_title == 'LambdaTest at DuckDuckGo', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')