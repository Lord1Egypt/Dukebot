# Dukebot Vercel Deployment — Fix Log

## Goal
Make `Lord1Egypt/Dukebot` (Python/Flask Telegram AI bot) deployable to Vercel via the "Deploy to Vercel" button in README, so any user can click it and get a working deployment.

## Deployed URL
https://duke-bot-tau.vercel.app/

## Repo
- Public (template): https://github.com/Lord1Egypt/Dukebot
- Original source: https://github.com/winniesi/tg-gemini-bot

---

## Fixes Applied (in order)

### 1. `requirements.txt` — Remove git dependency
**Problem:** `md2tgmd` was installed via git URL, which fails on Vercel (no `git` in build env).
**Fix:** Replaced with PyPI version.
```
# Before
md2tgmd @ git+https://github.com/yym68686/md2tgmd.git@e3c23501a21d2ab07d2f63e1d3a63cc9571b44ac

# After
md2tgmd>=0.3.10
```

### 2. `runtime.txt` — Pin Python version
**Added:** `python-3.11` to explicitly set Python version for Vercel.

### 3. `api/index.py` — Export Flask app as `handler`
**Added** at end of file:
```python
handler = app
```

### 4. `vercel.json` — Switch from `functions` to `builds`
**Root cause of "doesn't match any Serverless Functions" error:**
- `api/__init__.py` marks the `api/` directory as a Python package
- Vercel's `functions` config skips Python packages when scanning for serverless functions
- All files in `api/` use relative imports (`from .handle import ...`) so removing `__init__.py` wasn't viable

**Fix:** Replaced `functions` with `builds` using `@vercel/python` builder, which explicitly handles Flask apps with package-style imports.

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

---

## Current Status
- Deployment: **SUCCESS** at https://duke-bot-tau.vercel.app/
- Status page layout: **FIXED** (see Fix #5 below)
- Remaining issues to investigate (via Vercel CLI logs):
  - Runtime errors in bot logic

## Next Steps
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel logs https://duke-bot-tau.vercel.app/` to see runtime errors
3. Fix any import errors or missing env vars shown in logs
4. Check static files — `templates/` may need to be included in the build

### 5. `api/templates/status.html` — Fix layout, add icons
**Problem:** The setup page at `/` showed plain text links with no styling or icons for the three webhook actions.
**Fix:** Rewrote the template with:
- Dark card layout (GitHub-inspired dark theme)
- Font Awesome 6 icons via CDN for each button
- Three styled action buttons (green = set webhook, blue = info, red = delete)
- Proper token input with label and placeholder
- Responsive layout

**Icons used:**
- `fa-plug-circle-bolt` — Set Webhook (start bot)
- `fa-circle-info` — Get Webhook Info
- `fa-plug-circle-xmark` — Delete Webhook (stop bot)

---

## Key Files
| File | Purpose |
|------|---------|
| `api/index.py` | Flask app entry point, Vercel serverless function |
| `api/handle.py` | Message routing |
| `api/config.py` | Reads env vars (BOT_TOKEN, GOOGLE_API_KEY, etc.) |
| `api/gemini.py` | Gemini AI integration |
| `vercel.json` | Vercel build config |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version pin |

## Required Env Vars on Vercel
- `BOT_TOKEN` — Telegram bot token
- `GOOGLE_API_KEY` — Google Gemini API key (comma-delimited for multiple)
- `OPENAI_API_KEY` — (optional) OpenAI key
- `ALLOWED_USERS` — comma-delimited Telegram user IDs
- `ALLOWED_GROUPS` — comma-delimited group IDs
- `ADMIN_ID` — Telegram admin user ID
