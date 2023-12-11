import asyncio
from pyppeteer import connect, launch
from pyppeteer.errors import PageError
from urllib.parse import quote
import json
import os
from os import environ

exec_platform = os.getenv('EXEC_PLATFORM')

# Get username and access key of the LambdaTest Platform
username = environ.get('LT_USERNAME', None)
access_key = environ.get('LT_ACCESS_KEY', None)

async def test_lambdatest_search(capability):
    if exec_platform == 'cloud':
        print('Initializing test:: ', capability['LT:Options']['name'])

        browser = await connect(
            browserWSEndpoint=f'wss://cdp.lambdatest.com/puppeteer?capabilities={quote(json.dumps(capability))}'
        )
    elif exec_platform == 'local':
        print('Initializing test:: ', capability['browserName'])
        browser = await launch(headless=False, args=['--start-maximized'])

    page = await browser.newPage()

    await page.goto('https://search.brave.com/')
    title = await page.title()
    print(title)

    try:
        assert title == 'Private Search Engine - Brave Search', 'Expected page title is incorrect!'
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "passed", "remark": "Title matched" } })}')
        await teardown(page, browser)
    except PageError as e:
        await page.evaluate('_ => {}', f'lambdatest_action: {json.dumps({ "action": "setTestStatus", "arguments": { "status": "failed", "remark": str(e) } })}')
        await teardown(page, browser)

async def teardown(page, browser):
    await page.close()
    await browser.close()

# Capabilities array with the respective configuration for parallel tests
cloud_capabilities = [
    {
        'browserName': 'Chrome',
        'browserVersion': 'latest',
        'LT:Options': {
            'platform': 'Windows 10',
            'build': '[Build] Launching browser session with Pyppeteer (with unittest)',
            'name': 'Launching browser session with Pyppeteer (with unittest)',
            'user': username,
            'accessKey': access_key,
            'resolution': '1920x1080',
            'network': True,
            'video': True,
            'console': True,
            'headless': False
        }
    }
]

local_capabilities = [
    {
        'browserName': 'Chrome'
    }
]

if exec_platform == 'cloud':
    # Run parallel tests for each capability
    for capability in cloud_capabilities:
        asyncio.run(test_lambdatest_search(capability))
elif exec_platform == 'local':
    # Run parallel tests for each capability
    for capability in local_capabilities:
        asyncio.run(test_lambdatest_search(capability))