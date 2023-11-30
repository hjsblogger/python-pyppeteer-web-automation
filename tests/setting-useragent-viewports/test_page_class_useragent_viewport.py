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
browser_mode = os.getenv('BROWSER_MODE')

# Pytest fixture for browser setup
@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'local':
        if browser_mode == 'headless':
            browser = await launch()
        elif browser_mode == 'non-headless':   
            browser = await launch(headless = False, args=['--start-maximized']) 
    yield browser
    await asyncio.sleep(1)    
    await browser.close()

# Pytest fixture for page setup
@pytest.fixture(scope='function')
async def page(browser):
    # Reference - https://miyakogi.github.io/pyppeteer/
    # reference.html#pyppeteer.browser.Browser.createIncognitoBrowserContext
    page = await browser.newPage()
    yield page
    await page.close()

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_mod_viewport(page):
    await page.goto('https://www.lambdatest.com')
    # Maximize the page
    await page.setViewport({'width': 1920, 'height': 1080})
    await asyncio.sleep(2)

    await page.setViewport({'width': 1280, 'height': 720})
    await asyncio.sleep(2)

    print("Viewport test change complete")


@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_get_nonheadless_user_agent(browser, page):
    curr_userAgent = await browser.userAgent()
    print('Current user agent ' + curr_userAgent)

    page_title = await duckduckgo_test(page)

    try:
        assert page_title == 'LambdaTest at DuckDuckGo', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    await asyncio.sleep(1)

@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_get_headless_user_agent(browser, page):
    curr_userAgent = await browser.userAgent()
    print('Current user agent ' + curr_userAgent)

    page_title = await duckduckgo_test(page)

    try:
        assert page_title == 'LambdaTest at DuckDuckGo', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    await asyncio.sleep(1)

async def duckduckgo_test(page):
    # Navigate to a website to see the effect
    await page.goto('https://www.duckduckgo.com')
    # Maximize the page
    await page.setViewport({'width': 1920, 'height': 1080})

    element = await page.querySelector('[name="q"]')
    await element.click()
    await element.type('LambdaTest')
    await asyncio.gather(
        page.keyboard.press('Enter'),
        page.waitForNavigation()
    )

    page_title = await page.title()
    return page_title