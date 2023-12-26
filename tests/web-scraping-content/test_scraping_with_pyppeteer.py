import asyncio
import pytest
from pyppeteer.errors import PageError
from urllib.parse import quote
import json
import os
import sys
from os import environ
from pyppeteer import connect, launch

test_url = 'https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=57'

@pytest.mark.asyncio
async def test_ecommerce_scraping(page):
    for iteration in range(1,6):
        meta_data_arr = []

        curr_test_url = test_url + "&page=" + str(iteration)
        meta_data_arr = await scrap_ecommerce(page, curr_test_url)
        print('\n')
        print("Product Page = " + curr_test_url)
        print("*********************************************************************************************************\n")
        await print_scrapped_content(meta_data_arr)

async def scrap_ecommerce(page, curr_test_url) -> list:
    await page.goto(curr_test_url, {'waitUntil': 'domcontentloaded'})

    rows = await page.querySelectorAll('.product-layout.product-grid.no-desc.col-xl-4.col-lg-4.col-md-4.col-sm-6.col-6')

    meta_data_arr = []
    # Extract information from the selected elements
    for row in rows:
        link = await row.querySelector('a.carousel.d-block.slide')
        name = await row.querySelector('h4.title')
        price = await row.querySelector('span.price-new')

        link_href = await page.evaluate('(element) => element.getAttribute("href")', link)
        product_name = await page.evaluate('(element) => element.textContent', name)
        product_price = await page.evaluate('(element) => element.textContent', price)

        # Create a dictionary of the meta-data of the items on e-commerce store
        meta_data_dict = {
            'product link': link_href,
            'product name': product_name,
            'product price': product_price
        }

        meta_data_arr.append(meta_data_dict)  
    
    return meta_data_arr

# # Pagination - 1:5
# # Page 1: https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=57&page=1
# # Page 5: https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=57&page=5

# Replica of https://github.com/hjsblogger/web-scraping-with-python/blob/main/pageobject/helpers.py#L146
async def print_scrapped_content(meta_data):
    for elem_info in meta_data:
        print(elem_info)