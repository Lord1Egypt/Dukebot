# Dukebot Vercel Deployment — Fix Log

## Goal
Make `Lord1Egypt/Dukebot` (Python/Flask Telegram AI bot) deployable to Vercel via the "Deploy to Vercel" button in README, so any user can click it and get a working deployment.

## Repos
- **Original (public template):** https://github.com/Lord1Egypt/Dukebot — cloned at `/home/lordegypt/Dukebot`
- **Private working clone:** https://github.com/Lord1Egypt/dragonduke — cloned at `/home/lordegypt/dragonduke`
- **Live deployment:** https://dragonduke.vercel.app

## Strategy
Fix errors in the **private clone** (dragonduke) until 100% working, then sync all fixes back to the **original** (Dukebot) in one shot.

---

## Fixes Applied (in order)

### Fix 1 — `requirements.txt`: Remove git dependency
**Problem:** `md2tgmd` was installed via a git URL, which fails on Vercel (no `git` in build env).
**Fix:** Replaced with PyPI version.
```
# Before
md2tgmd @ git+https://github.com/yym68686/md2tgmd.git@e3c23501a21d2ab07d2f63e1d3a63cc9571b44ac

# After
md2tgmd>=0.3.10
```
**Commit:** `f95ffa6` on Dukebot

---

### Fix 2 — `runtime.txt`: Pin Python version
**Problem:** No Python version specified; Vercel behaviour was inconsistent.
**Fix:** Created `runtime.txt` with `python-3.11`
**Commit:** `f95ffa6` on Dukebot

---

### Fix 3 — `api/index.py`: Export Flask app as `handler`
**Problem:** Vercel's `@vercel/python` builder expects the WSGI app to be exported as `handler`.
**Fix:** Added `handler = app` at the bottom of `api/index.py`.
**Commit:** `eef8ecf` on Dukebot

---

### Fix 4 — `vercel.json`: Switch from `functions` to `builds`
**Root cause:** `api/__init__.py` marks `api/` as a Python package. Vercel's `functions` config skips Python packages when scanning for serverless functions, causing a "doesn't match any Serverless Functions" error.
**Fix:** Replaced `functions` with `builds` using `@vercel/python` builder.
```json
// Before (broken)
{
  "version": 2,
  "routes": [{ "src": "/(.*)", "dest": "/api/index.py" }],
  "functions": {
    "api/index.py": { "maxDuration": 30 }
  }
}

// After (working)
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": { "maxDuration": 30 }
    }
  ],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```
**Commit:** `c4d76aa` on Dukebot

---

### Fix 5 — `api/templates/status.html`: Redesign setup page
**Problem:** The `/` page showed plain text links with no styling.
**Fix:** Rewrote template with dark GitHub-inspired theme, Font Awesome icons, and three styled action buttons (Set Webhook, Get Webhook Info, Delete Webhook).
**Commit:** `01ac992` on Dukebot

---

### Fix 6 — `api/index.py`: Explicit Flask template path
**Problem:** `Flask(__name__)` resolves the `templates/` directory using the Python module name. Inside Vercel's serverless runtime, the module path can resolve differently, causing Flask to look in the wrong directory and fail to find `status.html`.
**Fix:** Used `os.path.abspath(__file__)` to pin the template folder to the actual file location.
```python
# Before
app = Flask(__name__)

# After
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
```
**Commit:** `cf6f67b` on Dukebot

---

### Fix 7 — Setup page: 3-step flow + env var table (dragonduke only so far)
**Problem:** Users deploying via the README button had no idea they needed to add `BOT_TOKEN` and `GOOGLE_API_KEY` to Vercel env vars. The token field on the setup page is ONLY for registering the Telegram webhook — it is NOT saved to the server. This caused silent failures (bot received messages but couldn't reply).
**Also:** No mention of OpenAI-compatible API setup on the page.
**Fix:** Rewrote setup page with 3 clear steps:
- Step 1: Set env vars in Vercel (with table showing all vars, REQUIRED/optional labels, direct link to Vercel dashboard, and orange warning box)
- Step 2: Register the webhook (existing buttons, now clearly labeled as step 2)
- Step 3: Test the bot (instructions + BotFather link)
**Commit:** `b6064c3` on dragonduke

---

### Fix 8 — `README.md`: Deploy button prompts for env vars (dragonduke only so far)
**Problem:** The "Deploy to Vercel" button URL didn't use Vercel's `env` parameter, so users were never prompted for `BOT_TOKEN` or `GOOGLE_API_KEY` during the deploy flow. Bot deployed, looked fine, silently failed.
**Fix:** Updated deploy button URL to include `env=BOT_TOKEN,GOOGLE_API_KEY` so Vercel shows an input form for both keys before the first deploy.
```
# Before
https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/Dukebot

# After
https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/Dukebot&env=BOT_TOKEN,GOOGLE_API_KEY&envDescription=...&envLink=...
```
**Commit:** `b6064c3` on dragonduke

---

## Current Status

| Item | Status |
|------|--------|
| Build on Vercel | ✅ Succeeds |
| `GET /` setup page | ✅ 200 OK |
| `POST /` webhook receives messages | ✅ 200 OK |
| Bot replies to Telegram | ❌ Needs `BOT_TOKEN` env var set |
| AI responses | ❌ Needs `GOOGLE_API_KEY` env var set |
| Setup page shows steps clearly | ✅ Fixed (dragonduke only) |
| Deploy button prompts for env vars | ✅ Fixed (dragonduke only) |
| SyntaxWarnings from md2tgmd | ⚠️ Cosmetic only, not our code, app still works |

---

## Remaining Tasks

1. **Set env vars on dragonduke Vercel project:**
   - `BOT_TOKEN` — Telegram bot token
   - `GOOGLE_API_KEY` — Google Gemini API key
   - `AUCH_ENABLE=0` OR `ALLOWED_USERS=<your telegram ID>` — to allow yourself in
   - Optional: `OPENAI_API_KEY` + `OPENAI_BASE_URL` for OpenAI-compatible models

2. **Redeploy dragonduke** after setting env vars (Vercel dashboard → Deployments → Redeploy, or `vercel --prod` from `/home/lordegypt/dragonduke`)

3. **Test end-to-end:**
   - Send `/start` to the bot in Telegram → should reply
   - Send a regular message → should get AI response
   - Try `/model` → should show model selector
   - Test with OpenAI key if applicable

4. **After all tests pass:** sync fixes 7 and 8 (setup page + README) from dragonduke → Dukebot original repo

---

## Key Files

| File | Purpose |
|------|---------|
| `api/index.py` | Flask app entry point, Vercel serverless function |
| `api/handle.py` | Message routing and auth check |
| `api/command.py` | Bot commands (/start, /model, /prompt, etc.) |
| `api/config.py` | Reads all env vars with safe defaults |
| `api/auth.py` | Access control (ALLOWED_USERS, AUCH_ENABLE) |
| `api/gemini.py` | Google Gemini AI integration |
| `api/openai_compat.py` | OpenAI-compatible API integration |
| `api/telegram.py` | Telegram API calls (send_message, etc.) |
| `api/templates/status.html` | Setup page at `/` |
| `vercel.json` | Vercel build config |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version pin (python-3.11) |

## Required Env Vars on Vercel

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | YES | Telegram bot token from @BotFather |
| `GOOGLE_API_KEY` | YES | Google Gemini API key from AI Studio |
| `OPENAI_API_KEY` | no | For OpenAI / OpenRouter / Groq / etc. |
| `OPENAI_BASE_URL` | no | Provider base URL (default: OpenAI) |
| `AUCH_ENABLE` | no | `0` = open, `1` = restricted (default is `1`) |
| `ALLOWED_USERS` | no | Comma-separated Telegram IDs or usernames |
| `ADMIN_ID` | no | Your Telegram user ID for admin commands |

## Auth Logic (important)
- `AUCH_ENABLE=1` (default) + `ALLOWED_USERS` empty → **nobody** can send regular messages
- `/start`, `/help`, `/get_my_info` bypass auth — always work
- Set `AUCH_ENABLE=0` to open the bot to everyone
- Send `/get_my_info` to the bot to find your Telegram user ID, then add it to `ALLOWED_USERS`

## Vercel CLI Commands Reference
```bash
# Check logs
vercel logs https://dragonduke.vercel.app --expand --since 1h

# Check error logs only
vercel logs --level error --since 24h --expand

# List env vars
vercel env ls

# Add env var
vercel env add BOT_TOKEN

# Deploy to production
vercel --prod
```
