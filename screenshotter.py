"""
python screenshotter.py --input urls.txt --output shots_folder --headless
"""
import os
import json
import asyncio
import argparse
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright


def create_output_dir(output_arg=None):
    if output_arg:
        output_dir = output_arg
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = f"screenshots_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def get_domain_name(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc.replace('.', '_')
    except Exception:
        return "invalid_url"


def load_cookies(cookie_file):
    if not cookie_file:
        return []
    try:
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)
        print(f"🍪 Loaded {len(cookies)} cookies from {cookie_file}")
        return cookies
    except Exception as e:
        print(f"❌ Failed to load cookies: {e}")
        return []


async def take_screenshots(input_file, output_dir, headless, cookie_file):
    output_dir = create_output_dir(output_dir)
    cookies = load_cookies(cookie_file)

    # Read URLs
    with open(input_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)

        for i, url in enumerate(urls, start=1):
            try:
                print(f"[{i}/{len(urls)}] Visiting: {url}")
                parsed_url = urlparse(url)
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080}
                )

                # Set cookies if applicable
                if cookies:
                    # Filter cookies matching the current domain
                    domain_cookies = [
                        cookie for cookie in cookies
                        if parsed_url.hostname and cookie.get("domain") in parsed_url.hostname
                    ]
                    if domain_cookies:
                        await context.add_cookies(domain_cookies)

                page = await context.new_page()
                await page.goto(url, timeout=15000)
                await page.wait_for_load_state("networkidle")
                filename = f"{i:02d}_{get_domain_name(url)}.png"
                filepath = os.path.join(output_dir, filename)
                await page.screenshot(path=filepath, full_page=True)
                print(f"✅ Saved: {filepath}")
                await context.close()
            except Exception as e:
                print(f"❌ Error with {url}: {e}")

        await browser.close()
    print(f"\n📂 All screenshots saved in: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Take screenshots of URLs using Playwright.")
    parser.add_argument("--input", type=str, default="urls.txt", help="Input file with URLs (default: urls.txt)")
    parser.add_argument("--output", type=str, default=None, help="Output folder (default: screenshots_<timestamp>)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--cookies", type=str, default=None, help="Path to JSON file containing cookies")

    args = parser.parse_args()

    asyncio.run(take_screenshots(
        input_file=args.input,
        output_dir=args.output,
        headless=args.headless,
        cookie_file=args.cookies
    ))


if __name__ == "__main__":
    main()
