# Beginner Command Reference

Run these commands in PowerShell from the project root.

```powershell
# 1. Check Python and pip
python --version
python -m pip --version

# 2. Allow setup script for this PowerShell session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Run project setup (creates venv and installs dependencies)
.\setup.ps1

# 4. Activate the environment whenever opening a new terminal
.\venv\Scripts\Activate.ps1

# 5. Run the automation
python daily_report_bot.py

# 6. List generated reports and screenshots
Get-ChildItem .\outputs

# 7. Deactivate the virtual environment
deactivate
```

If setup.ps1 cannot be run, execute the setup commands manually:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
