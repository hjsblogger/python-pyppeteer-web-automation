import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import json
import os
from os import environ
from pyppeteer import connect, launch

exec_platform = os.getenv('EXEC_PLATFORM')

# Get username and access key of the LambdaTest Platform
username = environ.get('LT_USERNAME', None)
access_key = environ.get('LT_ACCESS_KEY', None)

cloud_capabilities = {
    'browserName': 'chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 11',
        'build': '[Build] Duckduckgo Search using Pyppeteer',
        'name': 'Duckduckgo Search using Pyppeteer',
        'resolution': '1920x1080',
        'user': username,  # Replace with your LT_USERNAME
        'accessKey': access_key,  # Replace with your LT_ACCESS_KEY
        'network': True,
        'video': True,
        'console': True,
        'headless': False
    }
}

@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'local':
        browser = await launch(headless = False, args=['--start-maximized'])
    elif exec_platform == 'cloud':
        capability = quote(json.dumps(cloud_capabilities))
        print('Initializing test:: ', cloud_capabilities['LT:Options']['name'])

        browser = await connect(
            browserWSEndpoint=f'wss://cdp.lambdatest.com/puppeteer?capabilities={capability}'
        )
    yield browser
    await asyncio.sleep(1)    

# Pytest fixture for page setup
@pytest.fixture(scope='function')
async def page(browser):
    page = await browser.newPage()
    yield page
    
    await page.close()
    await asyncio.sleep(1)
    await browser.close()

@pytest.mark.usefixtures('page')
                         
@pytest.mark.asyncio
async def test_search_1(page):
    # asyncio.set_event_loop(asyncio.new_event_loop())
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

    await asyncio.sleep(1)

    title = await page.title()

    try:
        assert title == 'LambdaTest at DuckDuckGo', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')

    await asyncio.sleep(1)

    return title