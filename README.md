# Actuary — Insurance Risk Calculator

> A command-line tool that calculates auto and life insurance risk scores using public government data.

Built as a learning project to explore **Antigravity** and **Claude Code** features: slash commands, hooks, MCP integrations, and GitHub Actions automation.

---

## Features

- **Auto insurance quotes** — pulls vehicle complaint data from NHTSA
- **Life insurance estimates** — uses CDC mortality statistics
- **Side-by-side vehicle comparison** — compare two cars on safety metrics
- **Visual risk diagrams** — auto-generated Excalidraw charts for every quote ( Version 2)
- **Notion sync** — every quote saved to a searchable Notion database ( Version 2)
- **Protected secrets** — hooks block Claude from reading `.env` or `data/` files
- **Auto-archived reports** — timestamped reports saved to `reports/` automatically

---

## Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage — Slash Commands](#-usage--slash-commands)
- [Data Sources](#-data-sources)
- [Claude Code Features](#-claude-code-features)
- [GitHub Actions Workflows](#-github-actions-workflows)
- [Configuration](#-configuration)
- [How It Was Built](#-how-it-was-built)
- [Contributing](#-contributing)

---

## Quick Start

### Prerequisites

- Python 3.9+
- `pip install requests pandas`
- [Claude Code](https://docs.claude.com/en/docs/claude-code) (for development)

### Install

```bash
git clone https://github.com/YOUR_USERNAME/actuary.git
cd actuary
pip install -r requirements.txt
```

### Run your first quote

```bash
python main.py --type auto --age 35 --vehicle-make Honda --vehicle-model Civic
```

Or inside Claude Code:

```
/quote-auto 35 Ontario sedan
```

---

## Project Structure

```
actuary/
├── .claude/
│   └── commands/
│       ├── quote-auto.md        # /quote-auto [age] [province] [vehicle-type]
│       ├── quote-life.md        # /quote-life [age] [sex] [smoker/nonsmoker]
│       ├── compare-vehicle.md   # /compare-vehicle [make1-model1] [make2-model2]
│       ├── compare-visual.md    # /compare-visual [make1-model1] [make2-model2]
│       ├── history.md           # /history — last 10 quotes from Notion
│       └── help.md              # /help — list all commands
├── .github/
│   └── workflows/
│       ├── ci.yml               # Run tests on every push/PR
│       ├── claude-pr-review.yml # Auto PR review with @claude
│       └── claude-issue.yml     # Auto-implement issues labeled 'claude-implement'
├── actuary/
│   ├── fetchers/
│   │   ├── nhtsa.py             # Vehicle complaint data (NHTSA API)
│   │   ├── cdc.py               # Mortality statistics (CDC WONDER)
│   │   └── census.py            # Demographic risk data (US Census)
│   ├── engine/
│   │   ├── risk_scorer.py       # Combines data into 0-100 risk score
│   │   └── premium_estimator.py # Converts score to premium range (CAD)
│   ├── diagram.py               # Generates Excalidraw diagrams via MCP
│   └── notion_sync.py           # Saves quotes to Notion via MCP
├── reports/                     # Auto-archived quote reports (gitignored)
├── data/                        # Local cache (gitignored, hook-protected)
├── CLAUDE.md                    # Claude Code project memory & rules
├── requirements.txt
└── main.py                      # CLI entry point
```

---

##  Usage — Slash Commands

All commands are available inside **Claude Code** (`claude` in your terminal).

### `/quote-auto [age] [province/state] [vehicle-type]`

Generate an auto insurance risk quote.

```
/quote-auto 35 Ontario sedan
/quote-auto 28 British-Columbia SUV
/quote-auto 52 Alberta truck
```

**Output:**
```
──────────────────────────────────────
ACTUARY RISK REPORT — Auto Insurance
──────────────────────────────────────
Age Risk:         58/100
Vehicle Risk:     71/100
Location Risk:    45/100

OVERALL RISK SCORE:   65/100
EST. ANNUAL PREMIUM:  CAD $1,840 — $2,210

Top Risk Factors:
  1. Vehicle complaint rate (sedan category)
  2. Age bracket (35-40 moderate risk)
  3. Ontario collision frequency

✓  Report archived:   reports/2026-03-22-14-30-quote.md
```

---

### `/quote-life [age] [sex] [smoker/nonsmoker]`

Generate a life insurance risk estimate.

```
/quote-life 40 male nonsmoker
/quote-life 55 female smoker
/quote-life 30 female nonsmoker
```

---

### `/compare-vehicle [make1-model1] [make2-model2]`

Side-by-side vehicle safety comparison using NHTSA data.

```
/compare-vehicle Honda-Civic Toyota-Corolla
/compare-vehicle Ford-F150 Chevrolet-Silverado
```

---

### `/compare-visual [make1-model1] [make2-model2]`

Same as `/compare-vehicle` but generates an Excalidraw visual comparison diagram.

```
/compare-visual Honda-Civic Toyota-Corolla
```

---

### `/history`

Pulls the last 10 quotes from your Notion database and displays them as a table.

```
/history
```

---

### `/help`

Lists all available commands with argument formats.

```
/help
```

---

## Data Sources

| Source | Data Used | URL |
|--------|-----------|-----|
| **NHTSA** | Vehicle complaints & safety ratings | `api.nhtsa.gov` |
| **CDC WONDER** | Mortality rates by age/sex | `wonder.cdc.gov` |
| **US Census** | Demographic & location risk factors | `census.gov/data` |
| **IIHS** | Public vehicle safety ratings | `iihs.org` |

---

## Claude Code Features

This project was built using Claude Code and demonstrates four core features:

### 1. Basic Workflow (`CLAUDE.md`)

`CLAUDE.md` at the project root acts as Claude's memory. It documents:
- Project structure and conventions
- Coding standards (Python, type hints, `requests` + `pandas` only)
- Data source base URLs
- Risk score normalization rules (0–100 scale)

Claude reads this file at the start of every session automatically.

### 2. Custom Slash Commands (`.claude/commands/`)

Each `.md` file in `.claude/commands/` becomes a `/command` in Claude Code.
The `$ARGUMENTS` placeholder captures everything you type after the command name.

**Example — `.claude/commands/quote-auto.md`:**
```markdown
---
description: Generate an auto insurance risk quote
argument-hint: [age] [province/state] [vehicle-type]
allowed-tools: Read, Bash, Write
---

You are an insurance risk analyst using the Actuary tool.
Parse these arguments: $ARGUMENTS
Format: [age] [province/state] [vehicle-type]

1. Run the NHTSA fetcher for the vehicle type
2. Run the CDC fetcher for the age provided
3. Calculate the combined risk score
4. Output a formatted report with Excalidraw diagram URL
```

### 3. Hooks (`~/.claude/settings.json`)

Three hooks run automatically:

| Hook | Type | What it does |
|------|------|-------------|
| **Report archiver** | PostToolUse (Write) | Copies every `.md` output to `reports/` with timestamp |
| **Secret protector** | PreToolUse (Read\|Grep) | Blocks reads of `.env`, `data/`, `secrets` paths |
| **Completion notifier** | PostToolUse (Bash) | Prints `✓ Done` after slow fetches |

**Key difference:** PreToolUse *blocks* actions before they happen. PostToolUse *reacts* after. Always use PreToolUse for security.

### 4. MCP Integrations

| MCP Server | Used for |
|------------|----------|
| **Excalidraw** | Auto-generate risk diagrams after every quote |
| **Notion** | Save quotes to a structured database with full report pages |
| **Gmail** *(optional)* | Parse insurance renewal emails for data |
| **Google Calendar** *(optional)* | Schedule renewal reminders after quotes |

---

##  GitHub Actions Workflows

Three workflows are included in `.github/workflows/`.

---

### Workflow 1 — CI (`ci.yml`)

Runs automatically on every push and pull request.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/ --cov=actuary --cov-report=term-missing

      - name: Check code style
        run: |
          pip install flake8
          flake8 actuary/ --max-line-length=100
```

**What it does:**
- Installs Python 3.11 and all dependencies
- Runs the full test suite with coverage reporting
- Checks code style with flake8
- Fails the PR if tests break or style violations exist

---

### Workflow 2 — Claude PR Review (`claude-pr-review.yml`)

Automatically reviews every pull request using Claude Code. No manual trigger needed.

```yaml
# .github/workflows/claude-pr-review.yml
name: Claude PR Review

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Claude Code PR Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            Review this pull request for the Actuary insurance risk calculator.
            Check for:
            - Python type hints on all functions
            - Error handling for HTTP failures in fetchers
            - Risk scores normalized to 0-100 range
            - No hardcoded API keys or secrets
            - Tests for any new fetcher or engine logic
            Post your review as inline comments on the diff.
```

**What it does:**
- Triggers on every new PR and every new commit to an open PR
- Claude reads the full diff with project context from `CLAUDE.md`
- Posts inline code review comments directly on the PR
- Checks for project-specific conventions (type hints, error handling, no secrets)

**Setup required:**
1. Add `ANTHROPIC_API_KEY` to your repository secrets (Settings → Secrets → Actions)
2. Install the [Claude GitHub App](https://github.com/apps/claude) on your repo
   — or run `/install-github-app` inside Claude Code for automatic setup

---

### Workflow 3 — Claude Issue Implementer (`claude-issue.yml`)

When you label a GitHub issue with `claude-implement`, Claude automatically creates a branch, writes the code, and opens a pull request.

```yaml
# .github/workflows/claude-issue.yml
name: Claude Implement Issue

on:
  issues:
    types: [labeled]

permissions:
  contents: write
  pull-requests: write
  issues: read

jobs:
  implement:
    if: contains(github.event.label.name, 'claude-implement')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Claude Code Implement Issue
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            Implement the feature or fix described in issue #${{ github.event.issue.number }}.
            Follow the conventions in CLAUDE.md:
            - Python with type hints
            - requests + pandas only
            - Risk scores normalized 0-100
            - Add tests in tests/ for any new logic
            - Do not read or modify .env or data/ files
            Create a branch named feature/issue-${{ github.event.issue.number }},
            commit the changes, and open a pull request linking to this issue.

      - name: Comment on Issue
        if: success()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: ${{ github.event.issue.number }},
              body: '🤖 Implementation PR created by Claude. Please review before merging.'
            })
```

**What it does:**
- Watches for the `claude-implement` label on any issue
- Claude reads the issue description and `CLAUDE.md` for context
- Creates a feature branch, writes the code, adds tests
- Opens a pull request linked to the original issue
- Posts a comment on the issue with a link to the PR

**How to use it:**
1. Open a GitHub issue describing the feature or bug
2. Add the label `claude-implement`
3. Wait ~2 minutes — a PR will appear automatically

---

## Security

- **`.env` files** are protected by a PreToolUse hook — Claude cannot read them even if asked
- **`data/` folder** is gitignored and hook-protected — CSV files never leave your machine
- **GitHub Actions** — `ANTHROPIC_API_KEY` must be stored as a repository secret, never committed
- **Workflow permissions** — each workflow uses the minimum permissions required (`contents: read` for reviews, `contents: write` only for issue implementation)
---

## Configuration

### Environment variables (`.env`)

```bash
# Optional — only needed if extending with paid data sources
OPENWEATHER_API_KEY=your_key_here   # Not used by default
NOTION_TOKEN=auto_configured_by_mcp # Set automatically by Notion MCP
```

### Notion setup

Run this once inside Claude Code to initialize your Notion workspace:

```
Ask Claude: Run actuary/notion_sync.py setup_workspace()
```

This creates:
- `Actuary` parent page
- `Quote History` database (Date, Type, Risk Score, Premium, Excalidraw URL)
- `Reports` subpage for full report pages

### GitHub Actions setup

1. Add `ANTHROPIC_API_KEY` to repository secrets
2. Install Claude GitHub App: run `/install-github-app` in Claude Code
3. Create the `claude-implement` label in your repo (Issues → Labels → New label)

---

## How It Was Built

This project was built in 5 stages using Claude Code as the primary development tool:

| Stage | Feature | What Was Built |
|-------|---------|----------------|
| 1 | Basic workflow | CLAUDE.md, project structure, NHTSA + CDC fetchers, main.py |
| 2 | Slash commands | 6 command files in `.claude/commands/` using `$ARGUMENTS` |
| 3 | Hooks | PreToolUse secret protection, PostToolUse report archiver |
| 4 | Excalidraw MCP | `diagram.py` — auto-generates visual risk charts |
| 5 | Notion MCP | `notion_sync.py` — saves every quote to a structured database |


---
