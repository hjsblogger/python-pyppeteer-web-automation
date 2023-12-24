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
test_url = 'https://ecommerce-playground.lambdatest.io/'

cookie_dict = {}

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_get_cookie_info(page):
    await page.goto(test_url)

    await asyncio.sleep(1)

    # Output is a list of dictionaries
    # https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.cookies
    cookie_dict = await page.cookies()

    await asyncio.sleep(1)

    # Let's print values of all the cookies
    for cookie in cookie_dict:
        print("Cookie Name:")
        for key, val in cookie.items():
            print(f'  {key}: {val}')
        print()

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_delete_cookies(page):
    before_del_cookies = {}
    after_del_cookies = {}

    await page.goto(test_url)

    await asyncio.sleep(12)

    # https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.cookies
    # Create/Add a new cookie
    await page.setCookie({'name': 'pyppeteer', 'value': 'v1.0.2'})

    before_del_cookies = await page.cookies()
    print("\nBefore deletion\n")

    print_cookie(before_del_cookies)

    # Delete cookies
    await page.deleteCookie({'name': 'pyppeteer'})

    after_del_cookies = await page.cookies()
    print("After deletion\n")

    print_cookie(after_del_cookies)

def print_cookie(cookie_info):
    # Let's print values of all the cookies
    for cookie in cookie_info:
        print("Cookie Name:")
        for key, val in cookie.items():
            print(f'  {key}: {val}')
        print()