"""
DAY 2 - PYAUTOGUI BASIC: NETWEB STOCK PRICE TO EXCEL
====================================================

BEGINNER STEP-BY-STEP PROCEDURE
--------------------------------
STEP 1 - Open PowerShell in the Day2_PyAutoGUIBasic project folder.

STEP 2 - Create a separate virtual environment:
    python -m venv venv

STEP 3 - Activate the environment:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\venv\Scripts\Activate.ps1

STEP 4 - Install dependencies:
    python -m pip install --upgrade pip
    python -m pip install pyautogui pyperclip pillow pyscreeze

STEP 5 - Run the automation:
    python daily_report_bot.py

STEP 6 - Do not touch the mouse or keyboard while the script runs.
    PyAutoGUI sends keyboard and mouse actions to the active desktop window.
    To trigger the emergency stop, move the mouse to the top-left screen corner.

STEP 7 - Follow the five runtime stages shown in the terminal:
    [1/5] Open Chrome Guest, navigate to the Upstox quote page and wait
          until copied page text contains NETWEB and a rupee-denominated price.
    [2/5] Extract the stock name, symbol, exchange, price, percentage change
          and quote update text from the copied page.
    [3/5] Open Microsoft Excel and create a blank workbook.
    [4/5] Paste the column headings and stock data into Excel; verify cells
          A1 and A2 before continuing.
    [5/5] Save the .xlsx workbook, verify that the file exists and is non-empty,
          then capture one final screenshot of the populated worksheet.

STEP 8 - Check the outputs:
    Get-ChildItem .\outputs

    Expected successful files:
      netweb_stock_report_YYYY-MM-DD.xlsx
      netweb_stock_report_YYYY-MM-DD.png

WHAT THE PROGRAM DOES
---------------------
- Reads a public stock quote only; it does not log in or place trades.
- Uses Chrome Guest, clipboard text and regular expressions to extract data.
- Uses PyAutoGUI to control Excel through keyboard/mouse automation.
- Verifies Excel cells A1 and A2 so an empty workbook is not reported as success.
- Attempts to close Chrome Guest and Excel in the final cleanup block.

IMPORTANT
---------
- Keep the desktop undisturbed while the automation runs.
- The Upstox page text and layout can change; inspect diagnostic text/screenshots
  if stock extraction fails.
- Successful runs should create one final worksheet screenshot. Diagnostic
  screenshots may be created only when an error occurs.
- These instructions are intentionally inside this .py file; no separate
  Markdown procedure is required to understand or run the program.
"""

from __future__ import annotations

# datetime creates capture timestamps and date-based output filenames.
from datetime import datetime
# Path builds file locations without manually joining backslashes.
from pathlib import Path
import os
import re
import shutil
# subprocess launches Chrome as a separate Windows process.
import subprocess
import time

# PyAutoGUI controls the desktop; pyperclip reads/writes clipboard contents.
import pyautogui
import pyperclip


# STEP 1 - CONFIGURATION: stock identity, website, folders and wait limits.

STOCK_NAME = "Netweb Technologies India Ltd"
STOCK_SYMBOL = "NETWEB"
STOCK_EXCHANGE = "NSE"

# Public Upstox quote page; no account login is required.
STOCK_URL = os.environ.get(
    "STOCK_URL",
    "https://upstox.com/stocks/netweb-tech-india-ltd-share-price/",
)

# __file__ is this script; resolve() makes its path absolute; parent is project root.
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

BROWSER_START_WAIT = 8
PAGE_RENDER_WAIT = 12
CLIPBOARD_WAIT_TIMEOUT = 45
EXCEL_START_WAIT = 12
SAVE_DIALOG_WAIT = 6

# Emergency stop: move mouse to the top-left corner. PAUSE slows each action slightly.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


# --------------------------- Reusable helpers ---------------------------

def create_output_folder() -> None:
    """STEP 2 - Create outputs/ for generated workbooks and screenshots."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_capture_timestamp() -> str:
    """Return the local time when this script captured the stock quote."""
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def get_filename_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def find_chrome_executable() -> str:
    """STEP 3 - Find the Chrome executable in PATH or common install folders."""
    """Find Chrome from PATH or common Windows installation folders."""
    chrome = shutil.which("chrome") or shutil.which("chrome.exe")
    if chrome:
        return chrome

    candidates = [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Google/Chrome/Application/chrome.exe",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    raise FileNotFoundError(
        "Google Chrome was not found. Check that Chrome is installed."
    )


def launch_stock_page_and_copy_text() -> str:
    """STEP 4 - Launch Chrome Guest, open Upstox and copy rendered page text.

    The retry loop checks for both the NETWEB identity and a rupee price. It
    avoids assuming that one fixed delay guarantees JavaScript content is ready.
    """
    """
    Open the public NETWEB quote page in Chrome Guest and wait for its content.

    The page is JavaScript-rendered, so this uses repeated clipboard checks
    rather than assuming a fixed delay means the quote is ready.
    """
    print("[1/5] Opening NETWEB stock quote in Chrome Guest mode...")
    pyperclip.copy("")

    chrome_path = find_chrome_executable()
    guest_profile_dir = OUTPUT_DIR / "chrome_guest_profile"
    guest_profile_dir.mkdir(parents=True, exist_ok=True)

    # Popen starts Chrome without making Python wait for Chrome to exit.
    subprocess.Popen(
        [
            chrome_path,
            "--guest",
            "--no-first-run",
            "--no-default-browser-check",
            "--new-window",
            f"--user-data-dir={guest_profile_dir}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Allow Chrome itself to start before navigating.
    time.sleep(BROWSER_START_WAIT)

    # Navigate after the window exists. This avoids racing Chrome's startup.
    pyautogui.hotkey("ctrl", "l")
    pyperclip.copy(STOCK_URL)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    print("[1/5] Waiting for the NETWEB quote page to render...")
    # Use monotonic time to create a 90-second retry deadline.
    deadline = time.monotonic() + 90
    last_copied_text = ""

    while time.monotonic() < deadline:
        # Re-focus the page content on each attempt. Avoid Ctrl+A while the
        # address bar is focused, otherwise it selects the URL instead.
        time.sleep(3)
        pyautogui.click(800, 450)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        copied_text = pyperclip.paste()
        if copied_text:
            last_copied_text = copied_text
            normalized = copied_text.casefold()

            # A successful copy must contain the intended ticker/company and
            # a rupee price, not merely navigation text or an empty page.
            has_stock_identity = (
                "netweb" in normalized or "netweb technologies" in normalized
            )
            has_rupee_price = bool(
                re.search(r"₹\s*[0-9][0-9,]*(?:\.\d{1,2})?", copied_text)
            )

            if has_stock_identity and has_rupee_price:
                debug_path = OUTPUT_DIR / "netweb_copied_page.txt"
                debug_path.write_text(copied_text, encoding="utf-8")
                return copied_text

        print("[1/5] Quote not ready yet; retrying page capture...")

    # Save whatever text was available to help diagnose the actual page state.
    if last_copied_text:
        (OUTPUT_DIR / "netweb_copied_page.txt").write_text(
            last_copied_text, encoding="utf-8"
        )

    diagnostic_path = OUTPUT_DIR / "netweb_browser_diagnostic.png"
    pyautogui.screenshot().save(str(diagnostic_path))
    raise TimeoutError(
        "NETWEB quote did not become available within 90 seconds. The script "
        "waited and retried, but did not find both the NETWEB name and a rupee "
        "price. Check the browser screenshot: "
        f"{diagnostic_path}. If present, inspect "
        f"{OUTPUT_DIR / 'netweb_copied_page.txt'} too."
    )


def extract_stock_price(page_text: str) -> dict[str, str]:
    """STEP 5 - Parse copied text and return stock fields in a dictionary.

    Regular expressions find the rupee-denominated price and percentage change.
    """
    """
    Extract NETWEB's displayed price from the copied Upstox page text.

    The parser looks near the NETWEB stock heading and does not simply take
    the first rupee amount on the entire page (which could be unrelated data).
    """
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in page_text.splitlines()
    ]
    lines = [line for line in lines if line]

    # Confirm the copied content belongs to the intended stock.
    joined_text = "\n".join(lines)
    if not re.search(r"\bNETWEB\b|Netweb Tech", joined_text, re.IGNORECASE):
        debug_path = OUTPUT_DIR / "netweb_copied_page.txt"
        debug_path.write_text(page_text, encoding="utf-8")
        raise ValueError(
            "The copied page does not appear to contain NETWEB stock details. "
            f"Inspect: {debug_path}"
        )

    heading_index = next(
        (
            i for i, line in enumerate(lines)
            if re.search(r"Netweb.*Share Price|NETWEB", line, re.IGNORECASE)
        ),
        0,
    )

    # Search around the stock heading for the first rupee-denominated quote.
    context = lines[heading_index: min(heading_index + 20, len(lines))]
    # Match ₹ followed by a number, optional thousands separators and decimals.
    price_pattern = re.compile(r"₹\s*([0-9][0-9,]*(?:\.\d{1,2})?)")

    price = None
    price_line = None
    for line in context:
        match = price_pattern.search(line)
        if match:
            price = match.group(1).replace(",", "")
            price_line = line
            break

    if not price:
        debug_path = OUTPUT_DIR / "netweb_copied_page.txt"
        debug_path.write_text(page_text, encoding="utf-8")
        raise ValueError(
            "NETWEB was found, but a rupee-denominated share price was not "
            f"found near its heading. Inspect: {debug_path}"
        )

    # Capture a percentage movement if shown close to the price.
    change = "Not displayed"
    change_pattern = re.compile(
        r"([+-]?\s*\d+(?:\.\d+)?\s*%)"
    )
    for line in context[:8]:
        match = change_pattern.search(line)
        if match:
            change = match.group(1).replace(" ", "")
            break

    # Capture the page's quote update time if present.
    quote_time = "Not displayed"
    for line in lines:
        if re.search(r"last updated|as on|updated", line, re.IGNORECASE):
            quote_time = line
            break

    return {
        "stock_name": STOCK_NAME,
        "symbol": STOCK_SYMBOL,
        "exchange": STOCK_EXCHANGE,
        "share_price": price,
        "price_change": change,
        "quote_time": quote_time,
        "source": "Upstox public quote page",
        "price_source_line": price_line or "",
    }


def open_excel_and_create_workbook() -> None:
    """STEP 6 - Open Excel and select a new blank workbook."""
    """Launch Excel and explicitly open a blank workbook from its Home screen."""
    print("[3/5] Opening Microsoft Excel...")
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.write("excel", interval=0.08)
    pyautogui.press("enter")
    time.sleep(EXCEL_START_WAIT)

    # Excel may start on its Home screen. Ctrl+N is not reliable there,
    # so explicitly select the Blank workbook tile. Its position is
    # proportional to the screen size to support common display resolutions.
    screen_width, screen_height = pyautogui.size()
    blank_workbook_x = int(screen_width * 0.16)
    blank_workbook_y = int(screen_height * 0.28)
    pyautogui.click(blank_workbook_x, blank_workbook_y)
    time.sleep(6)

    # Move to A1 only after the blank workbook has had time to open.
    pyautogui.hotkey("ctrl", "home")
    time.sleep(1)

    # Keep a diagnostic screenshot if Excel is still showing its Home screen.
    # The worksheet should show the cell grid and the A1 selection.
    diagnostic_path = OUTPUT_DIR / "excel_workbook_ready.png"
    pyautogui.screenshot().save(str(diagnostic_path))


def enter_report_row(stock_data: dict[str, str]) -> None:
    """STEP 7 - Paste a header row and data row, then verify cells A1 and A2.

    Tabs separate columns and a newline separates the two rows. The read-back
    check prevents an empty worksheet from being treated as a successful run.
    """
    """Paste the report, verify Excel cell contents, then capture the loaded sheet."""
    print("[4/5] Entering NETWEB price details in Excel...")

    captured_at = get_capture_timestamp()
    comment = "NETWEB share price captured from the Upstox public quote page."

    headers = [
        "Captured Date & Time",
        "Stock Name",
        "Symbol",
        "Exchange",
        "Share Price (INR)",
        "Price Change",
        "Quote Update Time",
        "Source",
        "Comment",
    ]
    values = [
        captured_at,
        stock_data["stock_name"],
        stock_data["symbol"],
        stock_data["exchange"],
        stock_data["share_price"],
        stock_data["price_change"],
        stock_data["quote_time"],
        stock_data["source"],
        comment,
    ]

    # Paste into the first cell of the worksheet. A short retry loop handles
    # occasional clipboard/focus timing issues in desktop Excel.
    # Excel interprets tabs as columns and the newline as the next row.
    payload = "\t".join(headers) + "\n" + "\t".join(values)
    expected_header = headers[0]
    expected_first_value = captured_at

    verified = False
    for attempt in range(1, 4):
        print(f"[4/5] Pasting report into Excel (attempt {attempt}/3)...")
        pyautogui.press("esc")
        pyautogui.hotkey("ctrl", "home")
        time.sleep(0.4)

        pyperclip.copy(payload)
        time.sleep(0.4)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)

        # Verify A1 by copying the single active cell, not the entire range.
        pyautogui.press("esc")
        pyautogui.hotkey("ctrl", "home")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.8)
        actual_header = pyperclip.paste().strip()

        # Verify A2 (the capture timestamp) independently.
        pyautogui.press("down")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.8)
        actual_first_value = pyperclip.paste().strip()

        if actual_header == expected_header and actual_first_value == expected_first_value:
            verified = True
            break

    pyautogui.press("esc")
    pyautogui.hotkey("ctrl", "home")

    if not verified:
        diagnostic_path = OUTPUT_DIR / "excel_paste_verification_failed.png"
        pyautogui.screenshot().save(str(diagnostic_path))
        raise RuntimeError(
            "Excel paste verification failed. The expected header and first "
            "data value could not be read back from cells A1 and A2. "
            f"Screenshot: {diagnostic_path}. The workbook will not be reported "
            "as successfully populated."
        )

    print("[4/5] Verified Excel cells A1 and A2. Adjusting column widths...")
    # Select only the used range before AutoFit; then return to A1 so the
    # evidence screenshot does not show the entire worksheet selected.
    pyautogui.hotkey("ctrl", "shift", "end")
    pyautogui.hotkey("alt", "h")
    pyautogui.press("o")
    pyautogui.press("i")
    time.sleep(1)
    pyautogui.press("esc")
    pyautogui.hotkey("ctrl", "home")
    time.sleep(0.5)

    # The final saved-workbook screenshot is the only success screenshot.
    return None


def close_chrome_guest() -> None:
    """Close the automation's current Chrome Guest window, if it is open."""
    try:
        print("[Cleanup] Closing Chrome Guest window...")
        pyautogui.hotkey("ctrl", "shift", "w")
        time.sleep(2)
    except Exception as error:
        print(f"[Cleanup] Could not close Chrome Guest cleanly: {error}")


def close_excel() -> None:
    """Close Excel after the report has been saved and the final screenshot captured."""
    try:
        print("[Cleanup] Closing Excel...")
        pyautogui.hotkey("alt", "f4")
        time.sleep(2)
    except Exception as error:
        print(f"[Cleanup] Could not close Excel cleanly: {error}")


def save_workbook_and_screenshot() -> tuple[Path, Path]:
    """STEP 8 - Save the workbook, confirm the file exists, and take one screenshot."""
    """Save the Excel workbook and capture a screenshot after file verification."""
    date_part = get_filename_date()
    workbook_path = OUTPUT_DIR / f"netweb_stock_report_{date_part}.xlsx"
    screenshot_path = OUTPUT_DIR / f"netweb_stock_report_{date_part}.png"

    if workbook_path.exists():
        suffix = datetime.now().strftime("%H%M%S")
        workbook_path = OUTPUT_DIR / f"netweb_stock_report_{date_part}_{suffix}.xlsx"
        screenshot_path = OUTPUT_DIR / f"netweb_stock_report_{date_part}_{suffix}.png"

    print("[5/5] Saving the workbook...")
    pyautogui.press("f12")
    time.sleep(SAVE_DIALOG_WAIT)

    # In the Windows Save As dialog, Alt+N focuses the File name field.
    # Select its contents before pasting the complete destination path.
    pyautogui.hotkey("alt", "n")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "a")
    pyperclip.copy(str(workbook_path))
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(2)
    # Handle the Excel format confirmation if it appears.
    pyautogui.press("enter")

    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if workbook_path.exists() and workbook_path.stat().st_size > 0:
            break
        time.sleep(1)

    if not (workbook_path.exists() and workbook_path.stat().st_size > 0):
        diagnostic_path = OUTPUT_DIR / "save_as_diagnostic.png"
        pyautogui.screenshot().save(str(diagnostic_path))
        raise RuntimeError(
            "Excel did not create the expected workbook. Inspect the Save As "
            f"screen capture: {diagnostic_path}. Expected: {workbook_path}"
        )

    pyautogui.screenshot().save(str(screenshot_path))
    return workbook_path, screenshot_path


# --------------------------- Application entry point ---------------------------

def main() -> int:
    """STEP 9 - Run each stage in order and clean up browser/Excel windows."""
    create_output_folder()

    print("=== Day 2: PyAutoGUIBasic – NETWEB Stock Price Report ===")
    print(f"Stock: {STOCK_NAME} ({STOCK_SYMBOL})")
    print(f"Quote page: {STOCK_URL}")
    print("Read-only automation: no login or trade placement.")
    print("Do not use the mouse or keyboard while the bot is running.")

    # Orchestrate the stages in order. Each helper function has one responsibility.
    try:
        page_text = launch_stock_page_and_copy_text()
        close_chrome_guest()
        print("[2/5] Extracting NETWEB share price...")
        stock_data = extract_stock_price(page_text)

        print("\nCaptured stock information:")
        print(f"Stock:       {stock_data['stock_name']}")
        print(f"Symbol:      {stock_data['symbol']}")
        print(f"Share price: ₹{stock_data['share_price']}")
        print(f"Change:      {stock_data['price_change']}")
        print(f"Quote time:  {stock_data['quote_time']}")

        open_excel_and_create_workbook()
        enter_report_row(stock_data)
        workbook, screenshot = save_workbook_and_screenshot()

        print("\nAutomation completed successfully.")
        print(f"Excel report:       {workbook}")
        print(f"Screenshot:         {screenshot}")
        print("Browser and Excel cleanup completed.")
        return 0

    except pyautogui.FailSafeException:
        print("Automation aborted using the PyAutoGUI fail-safe.")
        return 2
    except Exception as error:
        print(f"Automation failed: {error}")
        return 1
    finally:
        # Always attempt to close the automation windows, including when
        # paste verification or workbook saving fails.
        close_chrome_guest()
        close_excel()


if __name__ == "__main__":
    raise SystemExit(main())
