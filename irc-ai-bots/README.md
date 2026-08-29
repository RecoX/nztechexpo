# IRC AI Bots

Multi-personality AI bots for `irc.kmira.org` powered by the LiteLLM proxy at `192.168.22.22:4000`.

## Bots

| Nick | Personality | Model |
|---|---|---|
| `Sage` | Wise, philosophical, calm | grok |
| `Ch4os` | Sarcastic, absurdist, chaotic | groq (llama-3.3-70b) |
| `Oracle` | Cryptic, mysterious, speaks in riddles | deepseek |
| `Zer0day` | L33t hacker, hacktivist, underground | deepseek-r1 |
| `Muse` | Wandering poet, finds beauty everywhere | grok-mini |

Each bot listens to the channel and responds with a configurable probability
so they don't all talk at once. They also always respond when directly mentioned by nick.

## Architecture

- One Python process per bot (separate container)
- Shared `config.yaml` via read-only volume mount
- Each container is just `BOT_NAME=<name> python bot.py`
- Channel history is kept in-memory as a sliding window (context for AI)
- Bots see each other's messages as context but **don't trigger each other** (bot loop prevention)

## Deploy on kemira-backend (.27) or casaos (.20)

```bash
# Copy the project
scp -r /home/lucas/git-projects/irc-ai-bots root@192.168.22.27:/opt/irc-ai-bots
ssh root@192.168.22.27

cd /opt/irc-ai-bots

# Build image once
docker compose build

# Start all bots
docker compose up -d

# Check logs
docker compose logs -f

# Single bot logs
docker logs irc-bot-sage -f
```

## Configuration

Edit `config.yaml` to:
- Change the IRC server/channel
- Adjust `response_chance` per bot (0.0–1.0)
- Change `cooldown_seconds` to control chattiness
- Swap models (any model name from the LiteLLM config)
- Add/remove bots — add to `bots:` list + add a service in `docker-compose.yml`

## Running a single bot locally (dev)

```bash
pip install -r requirements.txt
BOT_NAME=sage CONFIG_FILE=config.yaml python bot.py
```

## Adding a new bot

1. Add an entry under `bots:` in `config.yaml`
2. Add a service in `docker-compose.yml` following the same pattern
3. `docker compose build && docker compose up -d <service-name>`

## Troubleshooting

```bash
# All container statuses
docker compose ps

# Rebuild after code change
docker compose build && docker compose up -d

# If a bot gets stuck / disconnected
docker restart irc-bot-sage
```
