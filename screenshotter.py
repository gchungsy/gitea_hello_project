"""
python screenshotter.py --input urls.txt --output shots_folder --headless
"""
import os
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


async def take_screenshots(input_file, output_dir, headless):
    output_dir = create_output_dir(output_dir)

    # Read URLs
    with open(input_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})

        for i, url in enumerate(urls, start=1):
            try:
                print(f"[{i}/{len(urls)}] Visiting: {url}")
                page = await context.new_page()
                await page.goto(url, timeout=15000)
                await page.wait_for_load_state("networkidle")
                filename = f"{i:02d}_{get_domain_name(url)}.png"
                filepath = os.path.join(output_dir, filename)
                await page.screenshot(path=filepath, full_page=True)
                print(f"✅ Saved: {filepath}")
                await page.close()
            except Exception as e:
                print(f"❌ Error with {url}: {e}")

        await browser.close()
    print(f"\n📂 All screenshots saved in: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Take screenshots of URLs using Playwright.")
    parser.add_argument(
        "--input",
        type=str,
        default="urls.txt",
        help="Path to input file containing URLs (default: urls.txt)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output folder name (default: screenshots_<timestamp>)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False)"
    )

    args = parser.parse_args()

    asyncio.run(take_screenshots(
        input_file=args.input,
        output_dir=args.output,
        headless=args.headless
    ))


if __name__ == "__main__":
    main()
