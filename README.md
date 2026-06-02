<div align="center">

<h1>🤖 Duke Bot</h1>

<p><strong>A self-hosted Telegram AI bot with Google Gemini & OpenAI-compatible APIs.<br>Deploy in 60 seconds with one click — no coding required.</strong></p>

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/Dukebot&env=BOT_TOKEN,GOOGLE_API_KEY,ALLOWED_USERS,OPENAI_API_KEY,OPENAI_BASE_URL&envDescription=BOT_TOKEN%20and%20GOOGLE_API_KEY%20are%20required.%20ALLOWED_USERS%3A%20your%20Telegram%20ID%20to%20protect%20your%20API%20keys%20from%20abuse.%20OPENAI_API_KEY%20and%20OPENAI_BASE_URL%20are%20optional.&envLink=https%3A%2F%2Fgithub.com%2FLord1Egypt%2FDukebot%23environment-variables)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Serverless-000000?style=flat&logo=vercel&logoColor=white)](https://vercel.com)
[![License](https://img.shields.io/github/license/Lord1Egypt/Dukebot?style=flat&color=green)](LICENSE.txt)
[![Stars](https://img.shields.io/github/stars/Lord1Egypt/Dukebot?style=flat&color=yellow)](https://github.com/Lord1Egypt/Dukebot/stargazers)
[![Forks](https://img.shields.io/github/forks/Lord1Egypt/Dukebot?style=flat&color=blue)](https://github.com/Lord1Egypt/Dukebot/network/members)

</div>

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🧠 **Multi-model AI** | Google Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash + any OpenAI-compatible provider |
| 🔄 **Model switching** | `/model` — swap between AI models instantly via inline keyboard |
| 🎭 **System prompts** | `/prompt` — Default, Professional, Creative presets or write your own |
| 🖼️ **Image understanding** | Send photos — the bot analyzes and describes them |
| 💬 **Conversation history** | Remembers context within each session |
| 👥 **Group chat support** | Works in groups and supergroups; shared or per-user history |
| 🔒 **Access control** | Restrict to specific users or groups to protect your API keys |
| 🌐 **Any OpenAI-compatible API** | OpenRouter, Groq, Together AI, Mistral, self-hosted LLMs |
| ⚡ **One-click deploy** | Vercel, Railway, or Render — no server required |

---

## 🚀 Quick Deploy (Vercel)

**3 steps — under 60 seconds:**

1. Click **Deploy with Vercel** above → fill in your API keys when prompted
2. Visit your deployment URL → click **Set Webhook** on the setup page
3. Open your bot in Telegram → send `/start`

> ⚠️ **Set `ALLOWED_USERS` to your Telegram ID** during deploy to protect your API keys from abuse. Send `/get_my_info` to the bot to find your ID.

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and quick help |
| `/new` | Start a fresh conversation |
| `/model` | Switch AI model via inline keyboard |
| `/prompt` | Change system prompt (presets + custom) |
| `/get_my_info` | Get your Telegram user ID |
| `/get_group_info` | Get the group chat ID (groups only) |
| `/help` | Show full help message |

**Admin-only** (requires `ADMIN_ID` + `IS_DEBUG_MODE=1`):

| Command | Description |
|---------|-------------|
| `/get_allowed_users` | List authorized users |
| `/get_allowed_groups` | List authorized groups |
| `/get_api_keys` | Show API key status |
| `/list_models` | List configured models |

---

## 🤖 System Prompts

| Preset | Description |
|--------|-------------|
| 🤖 Default | Friendly, concise AI assistant |
| 💼 Professional | Expert consultant with structured answers |
| ✨ Creative | Imaginative partner with vivid storytelling |
| ✏️ Custom | Type your own system prompt |

---

## 🌐 Supported AI Providers

| Provider | Type | Base URL |
|----------|------|----------|
| [Google Gemini](https://aistudio.google.com/app/apikey) | Gemini API | *(built-in)* |
| [OpenAI](https://platform.openai.com) | OpenAI-compatible | `https://api.openai.com/v1` |
| [OpenRouter](https://openrouter.ai) | OpenAI-compatible | `https://openrouter.ai/api/v1` |
| [Groq](https://console.groq.com) | OpenAI-compatible | `https://api.groq.com/openai/v1` |
| [Together AI](https://www.together.ai) | OpenAI-compatible | `https://api.together.xyz/v1` |
| [Mistral](https://console.mistral.ai) | OpenAI-compatible | `https://api.mistral.ai/v1` |
| Self-hosted (Ollama, LM Studio, etc.) | OpenAI-compatible | Your server URL |

---

## ⚙️ Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `GOOGLE_API_KEY` | Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) |

### Security (Strongly Recommended)

| Variable | Description |
|----------|-------------|
| `ALLOWED_USERS` | Comma-separated Telegram user IDs or `@usernames`. **Set this to prevent strangers from draining your API quota.** |
| `AUCH_ENABLE` | `1` = only allowed users can chat (default), `0` = open to everyone |

### OpenAI-Compatible API (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for any OpenAI-compatible provider | — |
| `OPENAI_BASE_URL` | Provider base URL | `https://api.openai.com/v1` |

### Models (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_MODEL` | Model used for new conversations | `gemini-2.0-flash` |
| `GEMINI_MODELS` | Comma-separated Gemini models | `gemini-2.0-flash,gemini-1.5-pro,gemini-1.5-flash` |
| `OPENAI_MODELS` | Comma-separated OpenAI-compat models | `gpt-4o,gpt-4o-mini` |

### Admin & Debug (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_ID` | Your Telegram user ID — enables admin commands | — |
| `IS_DEBUG_MODE` | `1` = send debug logs to admin | `0` |
| `GROUP_MODE` | `1` = shared group history, `2` = per-user history in groups | `1` |

---

## 🆔 How to Find Your Telegram ID

**Method 1 — Use this bot:**
Send `/get_my_info` to your bot after deploying — it replies with your user ID.

**Method 2 — Use [@userinfobot](https://t.me/userinfobot):**
Open it on Telegram and send any message — it replies instantly with your ID.

**For group chat IDs:**
Add your bot to the group and send `/get_group_info` — the bot replies with the group ID (a negative number like `-1001234567890`). Add it to `ALLOWED_GROUPS`.

---

## 🔧 Other Deployment Options

### Railway

1. Fork this repository
2. Create a new Railway project → **Deploy from GitHub repo**
3. Add environment variables in the Railway dashboard
4. Set start command: `flask --app api.index run --host 0.0.0.0 --port $PORT`
5. Set your webhook URL to the Railway domain

### Render

1. Fork this repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `flask --app api.index run --host 0.0.0.0 --port $PORT`
5. Add environment variables and set your webhook to the Render domain

---

## 🏗️ Architecture

```
Telegram  ──webhook──►  Flask on Vercel / Railway / Render
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             handle_message        handle_callback
                    │                     │
          ┌─────────┴──────┐        user_settings
          ▼                ▼        (model + prompt)
       text/photo     commands
          │
    ChatManager
    (per-session history)
          │
    ┌─────┴──────┐
    ▼            ▼
Gemini API   OpenAI-compatible API
```

> Chat history is in-memory and resets on cold start (expected on serverless). Use `/new` to clear history manually.

---

## 📝 Register Commands with BotFather (Recommended)

Send this to [@BotFather](https://t.me/BotFather) using `/setcommands`:

```
start - Start the bot
new - Start a fresh conversation
model - Switch AI model
prompt - Change system prompt
get_my_info - Get your Telegram ID
get_group_info - Get group ID
help - Show help
```

---

## ⭐ Support

If this project helped you, please **star the repo** — it helps others find it!

[![Star History](https://img.shields.io/github/stars/Lord1Egypt/Dukebot?style=social)](https://github.com/Lord1Egypt/Dukebot/stargazers)

---

## 📄 License

MIT — free to use, modify, and deploy.
