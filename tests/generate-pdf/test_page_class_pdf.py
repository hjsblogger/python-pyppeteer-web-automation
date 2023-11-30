import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import os
import sys
from os import environ
from pyppeteer import connect, launch
sys.path.append(sys.path[0] + "/../..")

exec_platform = os.getenv('EXEC_PLATFORM')

test_url = 'https://lambdatest.com/'

# Selectors of the page

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
async def test_print_pdf(page):
    await page.goto(test_url, {'waitUntil' : 'networkidle2'})

    asyncio.sleep(1)

    # Further details - https://miyakogi.github.io/pyppeteer/reference.html
    # #pyppeteer.page.Page.emulateMedia

    page.emulateMedia('screen')

    # Further details
    # https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.pdf

    await page.pdf({'path': 'lambdatest.pdf', 'format': 'A4'})