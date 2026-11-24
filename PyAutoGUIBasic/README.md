# Day 2 – PyAutoGUIBasic: NETWEB Stock Price Report

A beginner-friendly Windows desktop automation project. It opens the public Upstox quote page for NETWEB in Chrome Guest mode, copies the rendered page text, extracts the displayed quote, enters a report into Microsoft Excel, saves the workbook, captures screenshots, and closes the browser and Excel windows.

This is read-only automation. It does not sign in to a trading account or place orders.

## Requirements
- Windows 10/11 desktop
- Python 3.12
- Google Chrome
- Microsoft Excel desktop
- Internet connection
- Unlocked desktop session while the bot runs

## Quick start

Open PowerShell in the project folder:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

Then run:

```powershell
.\venv\Scripts\Activate.ps1
python daily_report_bot.py
```

Do not use the mouse or keyboard while the bot is running. PyAutoGUI's fail-safe is enabled: move the pointer to the top-left corner to abort.

## Documentation

- `docs/Project_Documentation.md` – full beginner walkthrough
- `docs/Project_Documentation.pdf` – printable project documentation
- `docs/Beginner_Command_Reference.md` – setup and execution commands

## Project structure

```text
Day2_PyAutoGUIBasic/
├── daily_report_bot.py
├── requirements.txt
├── setup.ps1
├── README.md
├── .gitignore
├── docs/
│   ├── Project_Documentation.md
│   ├── Project_Documentation.pdf
│   └── Beginner_Command_Reference.md
└── outputs/
```

## Generated outputs

The script writes date-based files to `outputs/`:
- `netweb_stock_report_YYYY-MM-DD.xlsx` – Excel report
- `netweb_sheet_load_check_YYYY-MM-DD.png` – populated worksheet screenshot before saving
- `netweb_stock_report_YYYY-MM-DD.png` – final screenshot after saving
- `excel_workbook_ready.png` – screenshot after opening the blank workbook
- `netweb_copied_page.txt` – copied page text used for extraction
- Diagnostic screenshots/text if a stage fails

If a report already exists for the same date, the script adds a time suffix instead of overwriting it.

## Important notes
- The captured quote is whatever the public page displays when the automation runs.
- UI automation depends on screen resolution, display scaling, focus and application dialogs.
- Save unrelated work before running: the cleanup shortcuts close the current Chrome Guest and Excel windows.
