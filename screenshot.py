import asyncio
from playwright.async_api import async_playwright
import os

pages_to_capture = {
    'home': 'http://127.0.0.1:8000/',
    'about': 'http://127.0.0.1:8000/about/',
    'services': 'http://127.0.0.1:8000/services/',
    'blog': 'http://127.0.0.1:8000/blog/',
    'events': 'http://127.0.0.1:8000/events/',
    'feedback': 'http://127.0.0.1:8000/feedback/',
    'gallery': 'http://127.0.0.1:8000/gallery/',
    'contact': 'http://127.0.0.1:8000/contact/',
    'login': 'http://127.0.0.1:8000/dashboard/login/'
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1200, 'height': 1200})
        
        # Go to homepage
        print("Opening homepage...")
        await page.goto('http://127.0.0.1:8000/')
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.7);")
        await asyncio.sleep(1)
        
        # Click the first photo to open the lightbox
        print("Opening lightbox...")
        items = await page.query_selector_all('#gallery-grid .gallery-item')
        if items:
            await items[0].click()
            await asyncio.sleep(1)
            
            # Save screenshot of opened lightbox
            print("Capturing open lightbox...")
            await page.screenshot(path='C:/Users/DELL/.gemini/antigravity/brain/92af82e7-55d1-423b-bf43-18002f560ad7/screenshot_lightbox_open.png')
            
            # Click next arrow
            print("Navigating next...")
            await page.click('#lightbox-next')
            await asyncio.sleep(1)
            await page.screenshot(path='C:/Users/DELL/.gemini/antigravity/brain/92af82e7-55d1-423b-bf43-18002f560ad7/screenshot_lightbox_next.png')
            
            # Click close button
            print("Closing lightbox...")
            await page.click('#lightbox-close')
            await asyncio.sleep(1)
            await page.screenshot(path='C:/Users/DELL/.gemini/antigravity/brain/92af82e7-55d1-423b-bf43-18002f560ad7/screenshot_lightbox_closed.png')
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

