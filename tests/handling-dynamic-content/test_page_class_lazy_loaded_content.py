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

# Get username and access key of the LambdaTest Platform
username = environ.get('LT_USERNAME', None)
access_key = environ.get('LT_ACCESS_KEY', None)

test1_url = 'https://ecommerce-playground.lambdatest.io/'
test2_url = 'https://scrapingclub.com/exercise/list_infinite_scroll/'

# Usecase - 1
loc_ecomm_1 = ".order-1.col-lg-6 div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) div:nth-of-type(1) > img:nth-of-type(1)"
target_url_1 = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=63"

# Usecase - 2 (Click on e-commerce sliding banner)
loc_ecomm_2 = "[alt='Canon DSLR camera']"
target_url_2 = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=30"

# Usecase - 3 Automating interactions on https://scrapingclub.com/exercise/list_infinite_scroll/
loc_infinite_src_prod1 = ".grid .p-4 [href='/exercise/list_basic_detail/93926-C/']"
target_url_3 = "https://scrapingclub.com/exercise/list_basic_detail/93926-C/"

# Usecase - 4 Automating interactions on https://scrapingclub.com/exercise/list_infinite_scroll/
# when the images are lazy loaded
loc_infinite_src_prod2 = "div:nth-of-type(31) > .p-4 [href='/exercise/list_basic_detail/94967-A/']"
target_url_4 = "https://scrapingclub.com/exercise/list_basic_detail/94967-A/"

# Set timeout in ms
timeOut = 60000

# @pytest.fixture(scope='function')
# async def browser():
#     if exec_platform == 'local':
#         browser = await launch(headless = False, args=['--start-maximized'])
#     yield browser
#     await asyncio.sleep(1)    
#     await browser.close()

# # Pytest fixture for page setup
# @pytest.fixture(scope='function')
# async def page(browser):
#     page = await browser.newPage()
#     yield page
#     await page.close()

async def scroll_to_element(page, selector):
    # Scroll until the element is detected
    await page.evaluateHandle(
        '''async (selector) => {
            const element = document.querySelector(selector);
            if (element) {
                element.scrollIntoView();
            }
        }''',
        selector
    )

    return selector

async def scroll_carousel(page, scr_count):
    for scr in range(2, scr_count):
        elem_next_button = "#mz-carousel-213240 > ul li:nth-child(" + str(scr) + ")"
        await asyncio.sleep(1)
        elem_next_button = await page.querySelector(elem_next_button)
        await elem_next_button.click()

# Replica of https://github.com/hjsblogger/web-scraping-with-python/blob/
# main/tests/beautiful-soup/test_infinite_scraping.py#L67C5-L80C18

async def scroll_end_of_page(page):
    start_height = await page.evaluate('document.documentElement.scrollHeight')

    while True:
        # Scroll to the bottom of the page
        await page.evaluate(f'window.scrollTo(0, {start_height})')

        # Wait for the content to load
        await asyncio.sleep(1)

        # Get the new scroll height
        scroll_height = await page.evaluate('document.documentElement.scrollHeight')

        if scroll_height == start_height:
            # If heights are the same, we reached the end of the page
            break

        # Add an additional wait
        await asyncio.sleep(2)

        start_height = scroll_height

    # Additional wait after scrolling
    await asyncio.sleep(2)

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_lazy_load_ecomm_1(page):

    # The time out can be set using the setDefaultNavigationTimeout
    # It is primarily used for overriding the default page timeout of 30 seconds
    page.setDefaultNavigationTimeout(timeOut)
    await page.goto(test1_url,
        {'waitUntil': 'load', 'timeout': timeOut})
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    await asyncio.sleep(2)
    
    # elem_button = await page.waitForXPath(loc_xpath, {'timeout': timeOut})
    # Scroll until the element is detected
    elem_button = await scroll_to_element(page, loc_ecomm_1)

    # await page.click(elem_button)

    # Wait until the page is loaded
    # https://miyakogi.github.io/pyppeteer/reference.html#pyppeteer.page.Page.waitForNavigation
    navigationPromise = asyncio.ensure_future(page.waitForNavigation())
    await page.click(elem_button)  # indirectly cause a navigation
    await navigationPromise  # wait until navigation finishes
    
    # Assert if required, since the test is a simple one; we leave as is :D
    current_url = page.url
    print('Current URL is: ' + current_url)

    try:
        assert current_url == target_url_1
        print("Test Success: Product checkout successful")
    except PageError as e:
        print("Test Failure: Could not checkout Product")
        print("Error Code" + str(e))

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_lazy_load_ecomm_2(page):
    carousel_len = 4

    # The time out can be set using the setDefaultNavigationTimeout
    # It is primarily used for overriding the default page timeout of 30 seconds
    page.setDefaultNavigationTimeout(timeOut)
    await page.goto(test1_url,
        {'waitUntil': 'load', 'timeout': timeOut})
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    await asyncio.sleep(2)

    # Approach 1: Directly click on the third button on the carousel
    # elem_carousel_banner = await page.querySelector("#mz-carousel-213240 > ul li:nth-child(3)")
    # await asyncio.sleep(1)
    # await elem_carousel_banner.click()

    # Approach 2 (Only for demo): Serially click on every button on carousel
    await scroll_carousel(page, carousel_len)
    
    await asyncio.sleep(1)

    # elem_prod_1 = await page.querySelector(loc_ecomm_2)
    elem_prod_1 = await page.waitForSelector(loc_ecomm_2, {'visible': True})
    await asyncio.gather(
        elem_prod_1.click(),
        page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 60000}),
    )
    
    # Assert if required, since the test is a simple one; we leave as is :D
    current_url = page.url
    print('Current URL is: ' + current_url)

    try:
        assert current_url == target_url_2
        print("Test Success: Product checkout successful")
    except PageError as e:
        print("Test Failure: Could not checkout Product")
        print("Error Code" + str(e))


@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_lazy_load_infinite_scroll_1(page):
    # The time out can be set using the setDefaultNavigationTimeout
    # It is primarily used for overriding the default page timeout of 30 seconds
    page.setDefaultNavigationTimeout(timeOut)
    await page.goto(test2_url,
        {'waitUntil': 'load', 'timeout': timeOut})
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    await asyncio.sleep(1)

    elem_prod1 = await page.querySelector(loc_infinite_src_prod1)

    await asyncio.gather(
        elem_prod1.click(),
        page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 60000}),
    )

    # await asyncio.sleep(1)
    # await elem_carousel_banner.click()

    # elem_button = scroll_to_element(page, loc_infinite_src_prod1)
    # print(elem_button)
    # await asyncio.sleep(2)
    # await elem_button.click()
    
    # Assert if required, since the test is a simple one; we leave as is :D
    current_url = page.url
    print('Current URL is: ' + current_url)

    try:
        assert current_url == target_url_3
        print("Test Success: Product checkout successful")
    except PageError as e:
        print("Test Failure: Could not checkout Product")
        print("Error Code" + str(e))
   
@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_lazy_load_infinite_scroll_2(page):
    # The time out can be set using the setDefaultNavigationTimeout
    # It is primarily used for overriding the default page timeout of 30 seconds
    page.setDefaultNavigationTimeout(timeOut)

    # Tested navigation using LambdaTest YouTube channel

    # await page.goto("https://www.youtube.com/@LambdaTest/videos",
    await page.goto(test2_url, 
        {'waitUntil': 'load', 'timeout': timeOut})
    
    # Set the viewport - Apple MacBook Air 13-inch
    # Reference - https://codekbyte.com/devices-viewport-sizes/
    await page.setViewport({'width': 1440, 'height': 770})

    await asyncio.sleep(1)

    await scroll_end_of_page(page)

    await page.evaluate('window.scrollTo(0, 0)')

    await asyncio.sleep(1)

    # elem_prod = await page.querySelector(loc_infinite_src_prod2)

    # asyncio.sleep(1)

    # await asyncio.gather(
    #     elem_prod.click(),
    #     page.waitForNavigation({'waitUntil': 'load', 'timeout': 60000}),
    # )

    elem_button = await scroll_to_element(page, loc_infinite_src_prod2)

    await asyncio.sleep(1)

    # await page.click(elem_button)

    await asyncio.gather(
        page.click(elem_button),
        page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 60000}),
    )

    # Assert if required, since the test is a simple one; we leave as is :D
    current_url = page.url
    print('Current URL is: ' + current_url)

    try:
        assert current_url == target_url_4
        print("Test Success: Product checkout successful")
    except PageError as e:
        print("Test Failure: Could not checkout Product")
        print("Error Code" + str(e))