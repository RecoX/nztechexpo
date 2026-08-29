#!/usr/bin/env python3
"""
IRC AI Bot — single bot instance.
Each bot is a separate process/container with its own personality + model.
Set BOT_NAME env var to select which bot from config.yaml to run.

Design:
- Uses irc.client_aio (asyncio-native IRC library)
- On each public channel message, decides probabilistically whether to reply
- Calls LiteLLM proxy (OpenAI-compatible API) for completions
- Keeps a sliding window of channel history as conversation context
- Bots ignore each other's messages to prevent echo loops
"""

import asyncio
import logging
import os
import random
import re
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

import irc.client_aio as aio_irc
import yaml
from openai import AsyncOpenAI

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("ircbot")


# ---------------------------------------------------------------------------
# Config dataclasses
# ---------------------------------------------------------------------------
@dataclass
class BotConfig:
    name: str
    nick: str
    model: str
    system_prompt: str
    response_chance: float = 0.4
    response_chance_mention: float = 1.0
    response_chance_bot: float = 0.08
    max_response_tokens: int = 300
    typing_delay: float = 1.5
    cooldown_seconds: float = 8.0
    bot_cooldown_seconds: float = 45.0
    realname: str = "IRC AI Bot"
    username: str = "aibot"


@dataclass
class ServerConfig:
    host: str = "irc.kmira.org"
    port: int = 6667
    use_ssl: bool = False
    channel: str = "#general"
    channel_password: str = ""


@dataclass
class LiteLLMConfig:
    base_url: str = "http://192.168.22.22:4000"
    api_key: str = "sk-5196c38d39d0472d76385d22de628c11"


@dataclass
class AppConfig:
    server: ServerConfig
    litellm: LiteLLMConfig
    bots: list[BotConfig]
    context_window: int = 25
    ignore_nicks: list[str] = field(default_factory=list)


def load_config(path: str, bot_name: str) -> tuple[AppConfig, BotConfig]:
    with open(path) as f:
        raw = yaml.safe_load(f)

    server = ServerConfig(**raw.get("server", {}))
    litellm = LiteLLMConfig(**raw.get("litellm", {}))
    bots = [BotConfig(**b) for b in raw["bots"]]
    bot_map = {b.name: b for b in bots}

    if bot_name not in bot_map:
        raise SystemExit(
            f"Bot '{bot_name}' not found. Available: {list(bot_map.keys())}"
        )

    app = AppConfig(
        server=server,
        litellm=litellm,
        bots=bots,
        context_window=raw.get("context_window", 25),
        ignore_nicks=raw.get("ignore_nicks", []),
    )
    return app, bot_map[bot_name]


# ---------------------------------------------------------------------------
# Channel context ring-buffer
# ---------------------------------------------------------------------------
class ChannelContext:
    def __init__(self, maxlen: int = 25):
        self._buf: deque[dict] = deque(maxlen=maxlen)

    def add(self, nick: str, text: str):
        self._buf.append({"nick": nick, "text": text})

    def to_openai_messages(self, own_nick: str) -> list[dict]:
        msgs = []
        for entry in self._buf:
            if entry["nick"] == own_nick:
                msgs.append({"role": "assistant", "content": entry["text"]})
            else:
                msgs.append({
                    "role": "user",
                    "content": f"<{entry['nick']}> {entry['text']}",
                })
        return msgs


# ---------------------------------------------------------------------------
# Bot — subclasses AioSimpleIRCClient
# AioSimpleIRCClient.connect() is synchronous (runs loop.run_until_complete)
# AioSimpleIRCClient.start() / reactor.process_forever() runs loop.run_forever()
# ---------------------------------------------------------------------------
class AIBot(aio_irc.AioSimpleIRCClient):

    def __init__(self, app: AppConfig, cfg: BotConfig):
        super().__init__()
        self.app = app
        self.cfg = cfg
        self.ctx = ChannelContext(maxlen=app.context_window)
        self._last_reply: float = 0.0
        self._last_bot_reply: float = 0.0
        self._pending: bool = False
        self._nick_suffix: int = 0
        self._other_bot_nicks: set[str] = {
            b.nick for b in app.bots if b.nick != cfg.nick
        }

        self.ai = AsyncOpenAI(
            base_url=app.litellm.base_url,
            api_key=app.litellm.api_key,
        )

        # irc event handlers — registered on the reactor
        self.connection.add_global_handler("welcome", self._on_welcome)
        self.connection.add_global_handler("pubmsg", self._on_pubmsg)
        self.connection.add_global_handler("privmsg", self._on_privmsg)
        self.connection.add_global_handler("nicknameinuse", self._on_nick_in_use)
        self.connection.add_global_handler("disconnect", self._on_disconnect)
        self.connection.add_global_handler("error", self._on_error_event)

    # ------------------------------------------------------------------
    # IRC event handlers (called synchronously by the library)
    # ------------------------------------------------------------------
    def _on_welcome(self, connection, event):
        ch = self.app.server.channel
        log.info(f"[{self.cfg.nick}] Connected. Joining {ch}")
        if self.app.server.channel_password:
            connection.join(ch, self.app.server.channel_password)
        else:
            connection.join(ch)

    def _on_nick_in_use(self, connection, event):
        self._nick_suffix += 1
        new = f"{self.cfg.nick}{self._nick_suffix}"
        log.warning(f"[{self.cfg.nick}] Nick taken, trying {new}")
        connection.nick(new)

    def _on_disconnect(self, connection, event):
        log.warning(f"[{self.cfg.nick}] Disconnected — scheduling reconnect in 20s")
        loop = self.reactor.loop
        loop.call_later(20, self._do_reconnect)

    def _on_error_event(self, connection, event):
        log.error(f"[{self.cfg.nick}] Server error: {event.arguments}")

    def _on_pubmsg(self, connection, event):
        nick = event.source.nick
        text = event.arguments[0]
        own = connection.get_nickname()

        if nick == own:
            return
        if nick in self.app.ignore_nicks:
            return

        # Always record for context — but use lower chance for other AI bots
        self.ctx.add(nick, text)
        is_bot = nick in self._other_bot_nicks

        asyncio.ensure_future(
            self._maybe_respond(connection, nick, text, is_bot=is_bot),
            loop=self.reactor.loop,
        )

    def _on_privmsg(self, connection, event):
        nick = event.source.nick
        text = event.arguments[0]
        own = connection.get_nickname()

        if nick == own:
            return
        if nick in self.app.ignore_nicks:
            return
        # Don't respond to other bots in DMs
        if nick in self._other_bot_nicks:
            return

        log.info(f"[{self.cfg.nick}] DM from {nick}: {text[:80]}")
        asyncio.ensure_future(
            self._reply_dm(connection, nick, text),
            loop=self.reactor.loop,
        )

    async def _reply_dm(self, connection, nick: str, text: str):
        own = connection.get_nickname()
        # Build a minimal context: just this DM, no channel history
        messages = [
            {"role": "system", "content": self.cfg.system_prompt},
            {"role": "user", "content": text},
        ]
        try:
            await asyncio.sleep(self.cfg.typing_delay)
            log.info(f"[{self.cfg.nick}] Replying to DM from {nick}")
            resp = await self.ai.chat.completions.create(
                model=self.cfg.model,
                messages=messages,
                max_tokens=self.cfg.max_response_tokens,
                temperature=0.85,
            )
            reply = resp.choices[0].message.content.strip()
            if reply:
                reply = re.sub(r"\s*\n+\s*", " | ", reply)
                for chunk in _chunk(reply, 400):
                    connection.privmsg(nick, chunk)
                log.info(f"[{self.cfg.nick}] → DM {nick}: {reply[:90]}")
        except Exception as exc:
            log.error(f"[{self.cfg.nick}] DM reply error: {exc}")

    # ------------------------------------------------------------------
    # Reconnect
    # ------------------------------------------------------------------
    def _do_reconnect(self):
        s = self.app.server
        log.info(f"[{self.cfg.nick}] Reconnecting to {s.host}:{s.port}…")
        try:
            self.connect(
                server=s.host,
                port=s.port,
                nickname=self.cfg.nick,
                username=self.cfg.username,
                ircname=self.cfg.realname,
            )
        except Exception as exc:
            log.error(f"[{self.cfg.nick}] Reconnect failed: {exc}. Retrying in 30s")
            self.reactor.loop.call_later(30, self._do_reconnect)

    # ------------------------------------------------------------------
    # Response logic
    # ------------------------------------------------------------------
    async def _maybe_respond(self, connection, nick: str, text: str, is_bot: bool = False):
        if self._pending:
            return

        own = connection.get_nickname()
        mentioned = own.lower() in text.lower()

        # Separate cooldown for bot-to-bot replies
        if is_bot and not mentioned:
            if (time.time() - self._last_bot_reply) < self.cfg.bot_cooldown_seconds:
                return
        elif not mentioned:
            if (time.time() - self._last_reply) < self.cfg.cooldown_seconds:
                return

        if mentioned:
            chance = self.cfg.response_chance_mention
        elif is_bot:
            chance = self.cfg.response_chance_bot
        else:
            chance = self.cfg.response_chance

        if random.random() > chance:
            return

        self._pending = True
        try:
            reply = await self._get_reply(own)
            if reply:
                await asyncio.sleep(self.cfg.typing_delay)
                self._send(connection, reply)
                now = time.time()
                self._last_reply = now
                if is_bot:
                    self._last_bot_reply = now
                self.ctx.add(own, reply)
        except Exception as exc:
            log.error(f"[{self.cfg.nick}] AI error: {exc}")
        finally:
            self._pending = False

    async def _get_reply(self, own_nick: str) -> Optional[str]:
        messages = [{"role": "system", "content": self.cfg.system_prompt}]
        messages += self.ctx.to_openai_messages(own_nick)

        log.info(f"[{self.cfg.nick}] Querying model={self.cfg.model} ({len(messages)} msgs)")
        resp = await self.ai.chat.completions.create(
            model=self.cfg.model,
            messages=messages,
            max_tokens=self.cfg.max_response_tokens,
            temperature=0.85,
        )
        raw = resp.choices[0].message.content.strip()
        if not raw:
            return None
        # Collapse newlines — IRC is single-line per message
        return re.sub(r"\s*\n+\s*", " | ", raw)

    def _send(self, connection, text: str):
        ch = self.app.server.channel
        for chunk in _chunk(text, 400):
            connection.privmsg(ch, chunk)
        log.info(f"[{self.cfg.nick}] → {ch}: {text[:90]}{'…' if len(text) > 90 else ''}")

    # ------------------------------------------------------------------
    # Start
    # ------------------------------------------------------------------
    def run(self):
        s = self.app.server
        log.info(f"[{self.cfg.nick}] Connecting to {s.host}:{s.port}")
        # AioSimpleIRCClient.connect() calls loop.run_until_complete(connection.connect())
        self.connect(
            server=s.host,
            port=s.port,
            nickname=self.cfg.nick,
            username=self.cfg.username,
            ircname=self.cfg.realname,
        )
        # reactor.process_forever() calls loop.run_forever()
        self.reactor.process_forever()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _chunk(text: str, max_len: int) -> list[str]:
    """Split a long message into IRC-safe chunks."""
    if len(text) <= max_len:
        return [text]
    parts = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        cut = text.rfind(" ", 0, max_len)
        if cut == -1:
            cut = max_len
        parts.append(text[:cut])
        text = text[cut:].lstrip()
    return parts


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    config_file = os.environ.get("CONFIG_FILE", "config.yaml")
    bot_name = os.environ.get("BOT_NAME", "").strip()

    if not bot_name:
        raise SystemExit("BOT_NAME environment variable is required (e.g. sage, chaos, oracle)")

    app, cfg = load_config(config_file, bot_name)
    log.info(f"Loaded config for '{cfg.nick}' — model={cfg.model}")

    bot = AIBot(app, cfg)
    bot.run()


if __name__ == "__main__":
    main()
