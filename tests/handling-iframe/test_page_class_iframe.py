import asyncio
from pyppeteer import launch

async def main():
    # Launch a browser
    browser = await launch()

    # Create an incognito browser context
    incognito_context = await browser.createIncognitoBrowserContext()

    # Create a new page in the incognito browser context
    incognito_page = await incognito_context.newPage()

    # Perform actions on the incognito page
    await incognito_page.goto('https://example.com')
    # Add more actions as needed...

    # Close the incognito browser context when done
    await incognito_context.close()

    # Continue working with the original browser and pages

    # Close the browser when done
    await browser.close()

# Run the asyncio event loop
asyncio.get_event_loop().run_until_complete(main())