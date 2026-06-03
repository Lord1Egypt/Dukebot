# Dukebot Vercel Deployment — Fix Log

## Goal
Make `Lord1Egypt/Dukebot` (Python/Flask Telegram AI bot) deployable to Vercel via the "Deploy to Vercel" button in README, so any user can click it and get a working deployment.

## Repos
- **Original (public template):** https://github.com/Lord1Egypt/Dukebot — local: `/home/lordegypt/Dukebot`
- **Active private clone:** https://github.com/Lord1Egypt/duke-bot — local: `/home/lordegypt/duke-bot`
- **Old clone (deleted):** dragonduke — used during early testing, now gone

---

## Status: ✅ COMPLETE — Bot is fully working

---

## All Fixes Applied (in order)

### Fix 1 — `requirements.txt`: Remove git dependency
**Problem:** `md2tgmd` installed via git URL — Vercel has no `git` in build env.
**Fix:** Replaced with `md2tgmd>=0.3.10` (PyPI version).

### Fix 2 — `runtime.txt`: Pin Python version
**Fix:** Created file with `python-3.11`

### Fix 3 — `api/index.py`: Export Flask app as `handler`
**Fix:** Added `handler = app` at bottom of file.

### Fix 4 — `vercel.json`: Switch from `functions` to `builds`
**Root cause:** `api/__init__.py` makes it a Python package — Vercel's `functions` config silently skips packages.
**Fix:**
```json
{
  "version": 2,
  "builds": [{ "src": "api/index.py", "use": "@vercel/python", "config": { "maxDuration": 30 } }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

### Fix 5 — `api/templates/status.html`: Redesign setup page
**Fix:** Rewrote with dark GitHub-inspired theme, Font Awesome icons, styled buttons.

### Fix 6 — `api/index.py`: Explicit Flask template path
**Problem:** `Flask(__name__)` resolves templates differently in Vercel runtime.
**Fix:**
```python
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
```

### Fix 7 — Setup page: 3-step flow + security warnings
**Problem:** Users had no idea env vars needed to be set separately — the token field on the page is client-side only (not saved to server).
**Fix:** Rewrote page with:
- Step 1: Set env vars in Vercel (with red warning about ALLOWED_USERS for API protection)
- Step 2: Register webhook
- Step 3: Test + how to get Telegram ID (3 methods) + link to @userinfobot

### Fix 8 — README + deploy button: Prompt for env vars
**Fix:** Updated deploy button URL with `&env=BOT_TOKEN,GOOGLE_API_KEY,ALLOWED_USERS,OPENAI_API_KEY,OPENAI_BASE_URL` so Vercel prompts before deploying. Full README overhaul with badges, feature table, providers table, architecture diagram.

### Fix 9 — `api/config.py`: Remove @mention from help text
**Problem:** `@mention me` in help text created a clickable Telegram link.
**Fix:** Changed to `mention me by name or reply to my messages.`

### Fix 10 — GitHub repo polish
- 14 topics added via `gh repo edit --add-topic`
- Description and homepage set
- shields.io badges: Python, Flask, Vercel, License, Stars, Forks
- Star CTA at bottom of README

### Fix 11 — `api/command.py`: Accept both command formats
**Problem:** Help text showed `/get_my_info` but BotFather menu sent `/getmyinfo` (no underscores) → "Unknown command" error.
**Fix:** Added aliases so both formats work:
```python
if cmd in ("get_my_info", "getmyinfo"):
    return cmd_get_my_info(from_id)
if cmd in ("get_group_info", "getgroupinfo"):
    return cmd_get_group_info(from_type, chat_id)
```

---

## Key Things to Know

### Auth trap
`AUCH_ENABLE=1` (default) + empty `ALLOWED_USERS` = nobody can chat (not even owner).
Commands `/start`, `/help`, `/get_my_info` bypass auth always.
**Fix:** Set `ALLOWED_USERS=5814716109` (owner's Telegram ID) or `AUCH_ENABLE=0`.

### Token field on setup page
Client-side only — builds the Telegram webhook URL. NOT saved to server.
`BOT_TOKEN` must be set as a Vercel env var separately.

### `/start` and `/help` are identical
Both call `cmd_help()`. By design for now.

### BotFather `/setcommands` replaces — never adds
Every call replaces the full list. Send ALL commands in one message:
```
start - Start the bot
new - Start a fresh conversation
model - Switch AI model
prompt - Change system prompt
get_my_info - Get your Telegram user ID
get_group_info - Get group chat ID
help - Show help
```

### `@mention` in Telegram messages
If text contains `@word`, Telegram makes it a clickable mention link.
Always write mention instructions without `@`.

---

## Env Vars Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | YES | From @BotFather |
| `GOOGLE_API_KEY` | YES | From Google AI Studio |
| `ALLOWED_USERS` | SECURITY | Telegram ID(s) — protects API quota from abuse |
| `AUCH_ENABLE` | no | `1`=restricted (default), `0`=open |
| `OPENAI_API_KEY` | no | For OpenAI/OpenRouter/Groq/etc |
| `OPENAI_BASE_URL` | no | Provider URL, default OpenAI |
| `ADMIN_ID` | no | Your Telegram ID — enables admin commands |

## Owner Info
- Telegram user ID: `5814716109`
- GitHub: `Lord1Egypt`
- Vercel account: `mkeshitaoutlookcoms-projects`

## Vercel CLI Quick Reference
```bash
vercel link --project <name> --yes        # link local dir to project
vercel logs <url> --expand --since 1h    # view logs
vercel logs --level error --since 24h    # errors only
vercel env ls                            # list env vars
vercel env add VAR_NAME                  # add env var
vercel --prod                            # deploy to production
```

## Local Paths
- `/home/lordegypt/Dukebot` — original public repo
- `/home/lordegypt/duke-bot` — active private clone (deployed on Vercel)
- `/home/lordegypt/MyRepo/dukebot_notes.md` — session notes
