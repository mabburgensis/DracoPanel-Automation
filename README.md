# DracoPanel-Automation

## Project Purpose

**DracoPanel-Automation** is a Selenium-based Python automation project designed for comprehensive end-to-end testing of the [https://operator.dracofusion.com](https://operator.dracofusion.com) panel, including its most popular game modules (Mines, Diamonds, Dice, and more).
The goal is to **automate user flows and game mechanics** in a human-like fashion, ensure fast regression cycles after every release, and catch UI/UX or logic bugs early.

---

## Features

* **Simulates real user behavior:** All form entries, clicks, and delays are performed as a human would do.
* **Panel Login:** The script logs in with a username and password.
* **Game Automation:** Each game has a dedicated Python test script (`mines.py`, `diamonds.py`, `dice.py`).
* **Manual/Real Play Flows:** Each test runs through the real gameplay flow, as if using a real (test) account.
* **Win/Loss Assertion:** After every bet, win/loss results are parsed from the DOM and logged with assertions.
* **Centralized Locators:** All Xpath/UI locators are managed in dedicated locator files.
* **Stable, Readable Code:** Test flows are robust and written for clarity and easy extension.
* **Extensible:** Adding a new game or scenario is straightforward.

---

## Project Structure

```
DracoPanel-Automation/
│
├── common/
│   ├── browser_utils.py         # Common browser utils (open, screenshot, etc.)
│   ├── user_data.py             # User login info
│
├── locators/
│   ├── login_locators.py        # Login and panel locators
│   ├── mines_locators.py        # Mines game locators
│   ├── diamonds_locators.py     # Diamonds game locators
│   ├── dice_locators.py         # Dice game locators
│
├── mines.py                     # Mines game automation
├── diamonds.py                  # Diamonds game automation
├── dice.py                      # Dice game automation
├── main.py                      # Run all tests with a single command
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Installation & Setup

### 1. Python Environment

Recommended: **Python 3.8+**

Install dependencies:

```bash
pip install -r requirements.txt
```

*(Usually includes: selenium, webdriver\_manager, pytest, etc.)*

---

### 2. User Credentials

Edit `common/user_data.py` and provide your test user credentials.
**Do NOT use production accounts!**

---

### 3. Running a Single Game Test

To run a test for a specific game, use:

```bash
python mines.py
python diamonds.py
python dice.py
```

Each script will:

* Log in,
* Enter the related game,
* Execute its scenario (bets, assertions, UI checks),
* Print logs/results to the terminal.

---

### 4. Running All Tests Sequentially (main.py)

You can execute all automated tests with a single command using `main.py`:

```bash
python main.py
```

**Example content of `main.py`:**

```python
from diamonds import test_diamonds_flow
from mines import test_mines_flow
from dice import test_dice_flow

if __name__ == "__main__":
    print("== DracoPanel Automation: All Tests Starting ==")
    test_mines_flow()
    test_diamonds_flow()
    test_dice_flow()
    print("== All tests completed successfully! ==")
```

This script runs all tests one after another—ideal for regression or pre-release checks.

---

### 5. Screenshots

Key moments during test runs are automatically captured and stored for debugging and reporting.

---

## How it Works

* **mines.py**:

  * Login → Mines → Real Play → Random integer bet (1–99) → Random picks → Test ends after first win.
* **diamonds.py**:

  * Login → Diamonds → Real Play → Random integer bet (1–99) → Place bet → Log/Assert result → Loop 10 times.
* **dice.py**:

  * Login → Dice → Real Play → Random integer bet (1–99), random “chance to win” → Assert all win/loss results in history → Loop 10 times.

---

## Contribution & Development

* All scripts are PEP8-compliant and commented.
* Each scenario/test runs independently.
* Never commit sensitive data (e.g. real passwords)!
* To add a new game:

  * Create a new Python test (e.g. `plinko.py`)
  * Create its locator file (e.g. `plinko_locators.py`)
  * Add an import to `main.py` if you want to include it in batch runs.

---

## Notes

* Works with Chrome/Chromium via Selenium WebDriver (you may adjust for other browsers).
* For CI/CD integration or advanced reporting, scripts can be extended easily.

---

**This project is ideal for QA engineers and automation developers who need a robust, scalable UI/game regression solution for DracoPanel.**

---

Let me know if you want any section to be reworded or extra detail added!
You can copy and use this as your main README on GitHub. 🚀
