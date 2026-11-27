# Day 3 – Capture a Live Cricket Score with Playwright

## Project Overview

This project is part of the **Week 1 – Day 3 Playwright assignment**. It uses Python and Playwright's synchronous API to open the Cricbuzz live-scores page, locate the target cricket score, print the score in the terminal, and save a screenshot as `score.png`.

## Assignment Objective

- Open the Cricbuzz live-scores page using Playwright.
- Locate the target score element using a CSS selector inspected from the page.
- Wait for the score element to become visible before reading it.
- Print the captured score in the terminal.
- Save a screenshot of the page as `score.png`.
- Run the script in headed mode first and then in headless mode.

## Project Structure

```text
PlaywrightBasic/
├── cricbuzz_score.py       # Playwright automation script
├── score.png               # Screenshot captured by the script
├── Terminal_Screenshot.png # Terminal output evidence
└── README.md               # Project documentation
```

## Tools and Technologies

- **Python 3** – programming language
- **Playwright for Python** – browser automation library
- **Playwright Sync API** – runs browser automation steps sequentially
- **Chromium** – browser launched and controlled by Playwright
- **Cricbuzz** – website from which the live score is captured

## Target Website

[Cricbuzz – Live Cricket Scores](https://www.cricbuzz.com/cricket-match/live-scores)

The assignment target was the India vs New Zealand match. The script uses the CSS classes inspected from the score element and a score-text hint to distinguish the target element from other score elements on the page.

> **Note:** Cricket scores change during a live match. The current value in `SCORE_TEXT_HINT` inside `cricbuzz_score.py` is `246-5`, based on the inspected HTML supplied during development. If the score changes, update `SCORE_TEXT_HINT` to the score currently displayed for the target match before running the script. The selector or page structure may also need updating if Cricbuzz changes its HTML.

## Setup Instructions (Windows PowerShell)

### 1. Open the project folder

```powershell
cd path\to\PythonBasics\PlaywrightBasic
```

Replace the example path with the actual location of your cloned repository.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following command in the current PowerShell window and activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install Playwright

```powershell
python -m pip install playwright
```

### 5. Install the Chromium browser used by Playwright

```powershell
python -m playwright install chromium
```

## Run the Script

### Headed mode (visible browser)

Run this first. Chromium opens in a visible browser window:

```powershell
python cricbuzz_score.py
```

### Headless mode (browser runs in the background)

After headed mode works, run:

```powershell
$env:PLAYWRIGHT_HEADLESS = "true"
python cricbuzz_score.py
```

To return to the default headed mode in the same PowerShell session:

```powershell
Remove-Item Env:PLAYWRIGHT_HEADLESS
```

## How the Script Works

1. Imports `sync_playwright` and `PlaywrightTimeoutError` from `playwright.sync_api`.
2. Opens Playwright and launches its Chromium browser.
3. Creates a new browser page (tab).
4. Navigates to the Cricbuzz live-scores page.
5. Locates the score element using the CSS selector defined in `SCORE_SELECTOR` and filters it using `SCORE_TEXT_HINT`.
6. Uses `locator.wait_for(state="visible")` to wait for the score element, instead of using a fixed `sleep()` delay.
7. Reads the visible score using `inner_text()` and prints it in the terminal.
8. Captures the page using `page.screenshot()` and saves it as `score.png` in the project folder.
9. Handles a timeout or unexpected error and closes the browser in a `finally` block.

## Expected Output and Evidence

When the configured score is found, the terminal displays the captured score and the path where the screenshot was saved. The script creates or replaces `score.png` in the same folder as `cricbuzz_score.py`.

The repository includes:

- `cricbuzz_score.py` – source code for the Playwright automation.
- `score.png` – screenshot captured by the script.
- `Terminal_Screenshot.png` – terminal output evidence.

## Troubleshooting

- **Target score not found:** The score may have changed. Check the current score for the target match and update `SCORE_TEXT_HINT`.
- **Match not listed:** Confirm that the India vs New Zealand match is still available on the Cricbuzz live-scores page.
- **Selector no longer works:** Inspect the score element in browser Developer Tools and update `SCORE_SELECTOR` if Cricbuzz has changed its HTML classes.
- **Chromium is missing:** Run `python -m playwright install chromium` inside the active virtual environment.
- **Playwright module not found:** Activate the virtual environment and run `python -m pip install playwright`.

## Learning Outcomes

By completing this task, I practised:

- Using Playwright's Python synchronous API.
- Launching a browser with Chromium.
- Navigating to a website and working with page locators.
- Using CSS selectors based on inspected HTML.
- Waiting for an element condition rather than relying on a fixed delay.
- Reading page text and capturing a screenshot.
- Running browser automation in headed and headless modes.

---

**Assignment:** Week 1 – Day 3 – Task 1: Capture a Live Cricket Score with Playwright.
