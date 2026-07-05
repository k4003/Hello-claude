# HN Daily Digest

A small Python tool that pulls the top Hacker News stories, reads the linked
articles, summarizes them with Claude, and writes a Markdown digest — meant to
run automatically once a day.

Built as **Phase 2** of a self-directed AI-engineering learning project (the
longer-term goal is a personal information assistant that feeds summaries into
an Obsidian vault).

## What it does

1. Fetches the top N stories from the Hacker News API.
2. For each story with a link, downloads the page and extracts the main
   article text (via `trafilatura`).
3. Sends the titles + article text to the Claude API and asks for a
   Chinese-language summary.
4. Writes the summary plus a linked source list to `hn_summary.md`.

Data flows through the script in memory — there are no intermediate files.

## Requirements

- Python 3.13 (developed on Windows / PowerShell)
- An Anthropic API key (paid, pay-per-token)

## Setup

```bash
git clone https://github.com/k4003/Hello-claude.git
cd Hello-claude

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (never commit this):

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

## Usage

```bash
python helloclaude.py
```

Generates `hn_summary.md` in the project root. Open it in any Markdown viewer
(in VS Code: `Ctrl+Shift+V`).

## Run it daily (Windows)

`run_digest.bat` wraps the run so a scheduler can call it:

```bat
@echo off
cd /d C:\Users\14303\dev\CC
.venv\Scripts\python.exe helloclaude.py >> run.log 2>&1
```

Schedule with **Task Scheduler → Create Basic Task → Daily → Start a program**,
pointing at `run_digest.bat`. The machine must be on and logged in at the
scheduled time. Output and errors are appended to `run.log`.

## Project structure

```
helloclaude.py    main pipeline: fetch → scrape → summarize → write
run_digest.bat    wrapper for scheduled runs
requirements.txt  pinned dependencies
.env              API key (gitignored, not in repo)
hn_summary.md     generated digest (output)
run.log           scheduled-run log (gitignored)
```

## Notes

- Each run makes one Claude call (uses the Haiku model to keep cost low — a few
  cents per run). Set a spend limit in the Anthropic Console as a backstop.
- Ask HN posts have no external link, so they're summarized from the title only.
- Some pages can't be scraped (paywalls, JS-only sites); those are skipped.

## Roadmap

- Deduplicate stories already seen across runs
- Archive one file per day instead of overwriting
- Write output into an Obsidian vault (Phase 3)