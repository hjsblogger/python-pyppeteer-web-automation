import asyncio
from pyppeteer import launch

async def double_click():
    browser = await launch()
    page = await browser.newPage()

    # Navigate to a webpage
    await page.goto('https://example.com')

    # Locate the element using a selector
    element_selector = 'button#example-button'
    element = await page.waitForSelector(element_selector)

    # Evaluate JavaScript to perform a double-click on the element
    await page.evaluate('''(element) => {
        const doubleClick = new MouseEvent('dblclick', {
            bubbles: true,
            cancelable: true,
            view: window
        });
        element.dispatchEvent(doubleClick);
    }''', element)

    # Wait for some time to observe the result (optional)
    await page.waitForTimeout(2000)

    # Close the browser
    await browser.close()

# Run the asynchronous function
asyncio.run(double_click())
