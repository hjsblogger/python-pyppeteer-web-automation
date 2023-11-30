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

# Like Puppeteer, Navigation operations mentioned below only work in Headless mode
# goBack: https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goBack
# goForward: https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goForward

# Bug Link
# https://github.com/puppeteer/puppeteer/issues/7739
# https://stackoverflow.com/questions/65540674/how-to-error-check-pyppeteer-page-goback

@pytest.fixture(scope='function')
async def browser():
    if exec_platform == 'local':
        browser = await launch(headless = True)
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
@pytest.mark.order1
async def test_navigate_ops(page):
    # Added the same since goBack & goForward was not working in non-headless mode
    page.setDefaultNavigationTimeout(60000)
    await page.goto('https://ecommerce-playground.lambdatest.io/')
            # {'waitUntil': 'load', 'timeout': 60000})
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    # await asyncio.sleep(2)

    # https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.goBack
    await page.goto('https://www.lambdatest.com/selenium-playground')
    # await asyncio.sleep(2)
    await page.goBack()

    print("goBack: Current page URL is: " + page.url)

    # await asyncio.sleep(2)
    await page.goForward()

    print("goForward: Current page URL is: " + page.url)

    # Assert if required, since the test is a simple one; we leave as is :D