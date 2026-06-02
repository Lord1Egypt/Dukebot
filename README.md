# Duke Bot 🤖

A powerful Telegram AI bot that supports **Google Gemini** and any **OpenAI-compatible API** (OpenRouter, OpenCode, Groq, Together AI, Mistral, and more). Switch models and system prompts on the fly — right inside Telegram.

---

## Features

- **Multi-model support** — Google Gemini (2.0 Flash, 1.5 Pro, 1.5 Flash) and any OpenAI-compatible provider
- **`/model`** — Switch AI models with a tap via inline keyboard
- **`/prompt`** — Choose from preset system prompts or write your own custom prompt
- **Image understanding** — Send photos and the bot will analyze them
- **Conversation history** — Maintains chat context per user/group
- **Group support** — Works in Telegram groups and supergroups; shared or per-user history
- **Access control** — Restrict usage to specific users or groups
- **Admin commands** — Debug logging and admin-only management tools
- **One-click deploy** — Works on Vercel, Railway, Render, and other platforms

---

## Commands

| Command | Description |
|---------|-------------|
| `/new` | Start a fresh conversation |
| `/model` | Switch AI model (inline keyboard) |
| `/prompt` | Change system prompt (presets + custom) |
| `/get_my_info` | Get your Telegram user ID |
| `/get_group_info` | Get the group ID (group chats only) |
| `/help` | Show help message |

**Admin-only** (requires `ADMIN_ID` + `IS_DEBUG_MODE=1`):

| Command | Description |
|---------|-------------|
| `/get_allowed_users` | List authorized users |
| `/get_allowed_groups` | List authorized groups |
| `/get_api_keys` | Show API key status |
| `/list_models` | List configured models |

---

## System Prompts

The `/prompt` command gives you three built-in presets plus a custom option:

| Preset | Description |
|--------|-------------|
| 🤖 Default | Friendly, concise AI assistant |
| 💼 Professional | Expert consultant with structured answers |
| ✨ Creative | Imaginative partner with vivid storytelling |
| ✏️ Custom | Type your own system prompt |

---

## Deployment

### Vercel (Recommended - One Click Deploy)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/Dukebot)

**Fastest way to deploy:**

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Authorize Vercel to access your repos
4. Click "Import Repository"
5. Add environment variables in Vercel dashboard:
   - `BOT_TOKEN` — Your Telegram bot token
   - `GOOGLE_API_KEY` — Your Google Gemini API key
   - Other optional vars (see Environment Variables section below)
6. Click "Deploy"
7. After deployment completes, set your Telegram webhook:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<YOUR_VERCEL_URL>
   ```
   Or visit your Vercel deployment URL in a browser and use the setup page.

### Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Fork this repository
2. Create a new Railway project → **Deploy from GitHub repo**
3. Add environment variables in the Railway dashboard
4. Set start command: `flask --app api.index run --host 0.0.0.0 --port $PORT`
5. Set your webhook URL to the Railway domain

### Render

1. Fork this repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `flask --app api.index run --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Set your webhook to the Render domain

---

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `GOOGLE_API_KEY` | Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) |

### OpenAI-Compatible API (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for OpenAI-compatible provider | — |
| `OPENAI_BASE_URL` | Base URL of the provider | `https://api.openai.com/v1` |

**Popular providers and their base URLs:**

| Provider | Base URL |
|----------|----------|
| OpenAI | `https://api.openai.com/v1` |
| OpenRouter | `https://openrouter.ai/api/v1` |
| Groq | `https://api.groq.com/openai/v1` |
| Together AI | `https://api.together.xyz/v1` |
| Mistral | `https://api.mistral.ai/v1` |
| OpenCode | Your self-hosted URL |

### Models (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_MODEL` | Model used for new conversations | `gemini-2.0-flash` |
| `GEMINI_MODELS` | Comma-separated list of Gemini models to offer | `gemini-2.0-flash,gemini-1.5-pro,gemini-1.5-flash` |
| `OPENAI_MODELS` | Comma-separated list of OpenAI-compat models to offer | `gpt-4o,gpt-4o-mini` |

### Access Control (Optional)

| Variable | Description |
|----------|-------------|
| `AUCH_ENABLE` | `1` = restricted (default), `0` = open to everyone |
| `ALLOWED_USERS` | Comma-separated Telegram usernames or user IDs |
| `ALLOWED_GROUPS` | Comma-separated group names or group IDs |

### Admin & Debug (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_ID` | Your 10-digit Telegram user ID | — |
| `IS_DEBUG_MODE` | `1` = enable debug logs to admin, `0` = off | `0` |
| `GROUP_MODE` | `1` = shared group history, `2` = per-user history in groups | `1` |

---

## Quick Start

1. **Create a bot** — Message [@BotFather](https://t.me/BotFather) on Telegram, use `/newbot`, and save the token.

2. **Get a Gemini API key** — Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free key.

3. **Deploy** — Click one of the deploy buttons above or follow the manual steps.

4. **Set environment variables** — Add `BOT_TOKEN` and `GOOGLE_API_KEY` at minimum.

5. **Register the webhook** — Set the webhook URL to your deployment domain.

6. **Register commands with BotFather** (optional but recommended):
   ```
   new - Start a fresh conversation
   model - Switch AI model
   prompt - Change system prompt
   get_my_info - Get your Telegram ID
   get_group_info - Get group ID
   help - Show help
   ```

---

## Architecture

```
Telegram webhook → Flask (Vercel / Railway / Render)
                       ↓
               handle_message / handle_callback
                  ↓              ↓
            text / photo     inline keyboard
                  ↓              ↓
          ChatManager      user_settings
          (per-session)   (model + prompt)
                  ↓
        Gemini API  ←→  OpenAI-compatible API
```

Chat history is in-memory and resets on server restart (expected on serverless platforms). Use `/new` to manually clear history at any time.

---

## License

MIT
