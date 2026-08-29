# NZ Tech Expo 2026 — Do It Yourself AI

Live interactive demo for the talk at NZ Tech Expo 2026, Auckland.

Audience scans a QR code → joins `#nztechexpo` → chats with self-hosted AI agents live.

## Contents

| File | Description |
|---|---|
| `slides.md` | Slidev presentation source |
| `style.css` | Slide custom styles |
| `global-bottom.vue` | Slidev global bottom component |
| `package.json` | Slidev dependencies |
| `irc_bot.py` | AI IRC bots (Aria, Skeptic, HAL) |
| `Dockerfile` | Bot container image |
| `compose.yaml` | Docker Compose — three bot services |
| `kiwi-config.conf` | KiwiIRC server config |
| `kiwi-client.json` | KiwiIRC client branding & startup options |
| `ergo.motd` | Ergo IRC server MOTD |

## Slides

```bash
npm install
npm run dev      # dev server at localhost:3030
npm run build    # static export
npm run export   # export to PPTX
```

## Bots

Three AI agents connect to `#nztechexpo` on `irc.conreco.com.ar`:

- **Aria** — helpful, warm, answers everything
- **Skeptic** — contrarian, challenges AI hype
- **HAL** — HAL 9000, ominous and dry

Powered by LiteLLM → DeepSeek (or any OpenAI-compatible endpoint).

```bash
# Run locally (requires LiteLLM endpoint)
BOT_NAME=Aria \
IRC_HOST=irc.conreco.com.ar \
IRC_PORT=6668 \
LLM_URL=http://your-litellm:4000/v1/chat/completions \
LLM_KEY=your-key \
LLM_MODEL=deepseek \
python irc_bot.py
```

## Infrastructure

See `formosa` steering file: `skills/formosa/nztechexpo/SKILL.md`

- IRC server: Ergo on CT 107 (`192.168.22.27:6668`)
- Web client: KiwiIRC on CT 107 (`192.168.22.27:7779`)
- Public URL: `https://irc.conreco.com.ar`
- TLS: Let's Encrypt `*.conreco.com.ar` via HAProxy on pfSense
