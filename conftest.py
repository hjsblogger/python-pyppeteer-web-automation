import sys
import os
from os import environ
import json
import asyncio
import time
import pytest

sys.path.append(sys.path[0] + "/../..")
from pyppeteer import connect, launch
from urllib.parse import quote

exec_platform = os.getenv('EXEC_PLATFORM')

# Get username and access key of the LambdaTest Platform
username = environ.get('LT_USERNAME', None)
access_key = environ.get('LT_ACCESS_KEY', None)

cloud_capabilities = {
    'browserName': 'chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 11',
        'build': '[Build] Pytest + Pyppeteer testing on LambdaTest',
        'name': 'Pytest + Pyppeteer testing on LambdaTest',
        'resolution': '1920x1200',
        'user': username,
        'accessKey': access_key,
        'network': True,
        'video': True,
        'console': True,
        'headless': False
    }
}

local_capabilities = {
    'browserName': 'chrome'
}

# Fixture for launching a browser
@pytest.fixture(scope='function')
async def browser(request):
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

# Fixture for creating a new page
@pytest.fixture(scope='function')
async def page(browser):
    page = await browser.newPage()
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    if exec_platform == 'local':
        await page.setViewport({'width': 1440, 'height': 900})
    elif exec_platform == 'cloud':
        await page.setViewport({'width': 1920, 'height': 1200})
    yield page

    await page.close()
    await asyncio.sleep(1)
    await browser.close()