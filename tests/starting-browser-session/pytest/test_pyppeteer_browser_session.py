import asyncio
import pytest
import os
import sys
import json
from os import environ
from urllib.parse import quote
from pyppeteer import connect, launch
from pyppeteer.errors import PageError

test_url = 'https://search.brave.com/'
exec_platform = os.getenv('EXEC_PLATFORM')

# Get username and access key of the LambdaTest Platform
username = environ.get('LT_USERNAME', None)
access_key = environ.get('LT_ACCESS_KEY', None)

# Capabilities array with the respective configuration for parallel tests
cloud_capabilities = {
        'browserName': 'Chrome',
        'browserVersion': 'latest',
        'LT:Options': {
            'platform': 'Windows 11',
            'build': '[Build] Launching browser session with Pyppeteer (with Pytest)',
            'name': 'Launching browser session with Pyppeteer (with Pytest)',
            'user': username,
            'accessKey': access_key,
            'resolution': '1920x1080',
            'network': True,
            'video': True,
            'console': True,
            'headless': False
        }
}

local_capabilities = {
        'browserName': 'Chrome'
}

# Pytest fixture for browser setup
@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'cloud':
        capability = quote(json.dumps(cloud_capabilities))
        print('Initializing test:: ', cloud_capabilities['LT:Options']['name'])

        browser = await connect(
            browserWSEndpoint=f'wss://cdp.lambdatest.com/puppeteer?capabilities={capability}'
        )
    elif exec_platform == 'local':
        print('Initializing test:: ', local_capabilities['browserName'])
        browser = await launch(headless = False, args=['--start-maximized'])
    
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

@pytest.mark.asyncio
async def test_browser_session(page):
    await page.goto('https://search.brave.com/')
    title = await page.title()
    print(title)

    try:
        assert title == 'Private Search Engine - Brave Search', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')