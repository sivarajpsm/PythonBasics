

# STEP 1 - IMPORT THE REQUIRED PLAYWRIGHT TOOLS
# os reads the environment variable used to switch headed/headless mode.
# Path builds the screenshot path relative to this Python file.
from pathlib import Path
import os

# sync_playwright is the synchronous Playwright API requested by the task.
# PlaywrightTimeoutError helps us handle an element that does not appear.
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


# STEP 2 - CONFIGURATION
CRICBUZZ_URL = "https://www.cricbuzz.com/cricket-match/live-scores"

# CSS selector based on the HTML classes you supplied.
# Attribute selectors [class~="..."] match one complete class token.
# This avoids escaping the colon (:) and slash (/) in the original classes.
SCORE_SELECTOR = (
    'span.font-medium'
    '[class~="text-cbTxtPrim"]'
    '[class~="w-1/2"]'
    '[class~="truncate"]'
)

# This is the score text in the HTML element you supplied.
# Update this value if the live India vs New Zealand score changes.
SCORE_TEXT_HINT = "246-5"

PROJECT_FOLDER = Path(__file__).resolve().parent
SCREENSHOT_PATH = PROJECT_FOLDER / "score.png"

# Default is headed mode so you can watch the browser.
# Set PLAYWRIGHT_HEADLESS=true in PowerShell to hide the browser window.
HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "false").strip().lower() == "true"

# Maximum time Playwright should wait for the target score.
SCORE_WAIT_TIMEOUT_MS = 30_000


# STEP 3 - MAIN FUNCTION: keep the browser workflow in one place.
def main() -> int:
    print("=" * 60)
    print("WEEK 1 - DAY 3 - PLAYWRIGHT: INDIA vs NEW ZEALAND")
    print("=" * 60)

    print(f"\nBrowser mode: {'HEADLESS' if HEADLESS else 'HEADED'}")
    print(f"Opening: {CRICBUZZ_URL}")
    print(f"Looking for the supplied score text: {SCORE_TEXT_HINT}")

    # The with block starts Playwright and releases its runtime on exit.
    with sync_playwright() as playwright:

        # STEP 4 - LAUNCH CHROMIUM
        # headless=False displays the browser; True hides its window.
        browser = playwright.chromium.launch(headless=HEADLESS)

        try:
            # STEP 5 - CREATE A NEW BROWSER TAB
            # A page object represents one tab in the Chromium browser.
            page = browser.new_page(
                viewport={"width": 1440, "height": 1000}
            )

            # STEP 6 - OPEN THE CRICBUZZ LIVE-SCORES PAGE
            # domcontentloaded waits for the initial HTML to be parsed.
            # JavaScript may render or update live score content afterwards.
            page.goto(
                CRICBUZZ_URL,
                wait_until="domcontentloaded",
                timeout=60_000,
            )

            # STEP 7 - LOCATE THE SCORE ELEMENT
            # First locate elements with the inspected CSS classes.
            # Then filter for the supplied score text to distinguish this
            # score from other match scores shown on the same page.
            score_locator = page.locator(SCORE_SELECTOR).filter(
                has_text=SCORE_TEXT_HINT
            ).first

            # STEP 8 - WAIT FOR THE TARGET SCORE TO BECOME VISIBLE
            # This waits for the condition; it does not use time.sleep().
            score_locator.wait_for(
                state="visible",
                timeout=SCORE_WAIT_TIMEOUT_MS,
            )

            # STEP 9 - READ THE VISIBLE SCORE TEXT
            # inner_text() reads the rendered text from the selected element.
            score_text = score_locator.inner_text().strip()

            if not score_text:
                print("\nThe selected score element is visible but contains no text.")
                return 1

            # STEP 10 - PRINT THE SCORE IN THE TERMINAL
            print("\nIndia vs New Zealand score captured:")
            print("-" * 60)
            print(score_text)
            print("-" * 60)

            # STEP 11 - SAVE THE REQUIRED SCREENSHOT
            # Capture the rendered Cricbuzz page as assignment evidence.
            page.screenshot(
                path=str(SCREENSHOT_PATH),
                full_page=True,
            )
            print(f"\nScreenshot saved: {SCREENSHOT_PATH}")
            print("\nCapture completed.")
            return 0

        except PlaywrightTimeoutError:
            # A timeout means the exact score hint was not visible in time.
            # It does not prove that no match is live: the score may have
            # changed, the match may have left this page, or the site may
            # have changed its HTML classes.
            print("\nThe target score was not found within 30 seconds.")
            print("Check these items:")
            print(f"1. Has the India vs New Zealand score changed from {SCORE_TEXT_HINT}?")
            print("2. If it changed, update SCORE_TEXT_HINT near the top of this file.")
            print("3. Confirm the match is still listed on the Cricbuzz live-scores page.")
            print("4. Reinspect the score element if Cricbuzz changed its HTML classes.")
            return 1

        except Exception as error:
            # Display navigation or unexpected browser errors clearly.
            print(f"\nAn unexpected error occurred: {error}")
            return 1

        finally:
            # STEP 12 - CLOSE THE BROWSER
            # finally runs after success or failure, so Chromium is closed.
            browser.close()
            print("\nChromium browser closed.")


# STEP 13 - PROGRAM ENTRY POINT
# Run main() only when this Python file is executed directly.
if __name__ == "__main__":
    raise SystemExit(main())
