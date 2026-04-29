# Oglas Tracker

Automated tracker for Croatian classified-ad sites. Monitors ad counts every 5 minutes via GitHub Actions and sends a Telegram notification when new ads appear.

Currently supported: **Njuškalo** (server-side HTML).
Planned: **Index Oglasi** (JavaScript rendering via Playwright).

---

## How it works

1. Scrape the configured search URLs and extract the total ad count.
2. Compare with the previously saved count in `state.json`.
3. If any count **increased**, send a single consolidated Telegram message.
4. Persist the new counts back to `state.json`.

On the very first run (no `state.json`), counts are saved without sending a notification.

---

## Local setup

```bash
# Clone
git clone https://github.com/<your-user>/oglas_tracker.git
cd oglas_tracker

# Virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

# Dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env and fill in your values

# Run
python app.py
```

---

## Creating a Telegram Bot

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the prompts to pick a name and username.
3. BotFather replies with an **API token** (e.g. `7123456789:AAH...`) — this is your `TELEGRAM_BOT_TOKEN`.

### Finding your Chat ID

1. Open a chat with your new bot in Telegram and send any message (e.g. "hello").
2. Open this URL in your browser (replace `<TOKEN>` with your actual token):

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. In the JSON response, find the `"chat": {"id": NUMBER}` — that number is your `TELEGRAM_CHAT_ID`.

---

## GitHub Secrets

Go to **Settings → Secrets and variables → Actions** in your repository and add:

| Secret               | Description                          |
|----------------------|--------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather            |
| `TELEGRAM_CHAT_ID`   | Your personal or group chat ID       |

---

## Deploy (GitHub Actions)

The workflow is already configured in `.github/workflows/check.yml`.

- **Schedule:** runs every 5 minutes (`*/5 * * * *`).
- **Manual trigger:** you can also run it via *Actions → Check Ads → Run workflow*.
- After each run the workflow commits updated `state.json` back to the repo.

> **Note:** GitHub Actions cron is best-effort and may have delays of up to a few minutes.

---

## Project structure

```
app.py              # Entry point
config.py           # URLs, category names
state.py            # Read / write state.json
notifier.py         # Telegram notification builder + sender
providers/
  base.py           # Abstract base provider
  njuskalo.py       # Njuškalo HTML scraper
  (index.py)        # Future – Index Oglasi (Playwright)
.github/workflows/
  check.yml         # Cron workflow
```

---

## Adding a new provider

1. Create `providers/your_provider.py`.
2. Subclass `BaseProvider` and implement `fetch_count(url) -> int`.
3. Instantiate and call `provider.scrape(categories)` in `app.py`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Selector 'strong.entities-count' not found` | Njuškalo may have changed their HTML. Inspect the page and update `_SELECTOR` in `providers/njuskalo.py`. |
| Telegram message not arriving | Verify the bot token and chat ID. Make sure you sent at least one message to the bot first. Check `https://api.telegram.org/bot<TOKEN>/getUpdates`. |
| Telegram API returns 403 | The bot was blocked by the user. Unblock it in Telegram. |
| Workflow never runs | GitHub disables scheduled workflows after 60 days of repo inactivity. Push a commit or trigger manually. |
| `state.json` merge conflict | Delete the file and let the next run reinitialise it. |
