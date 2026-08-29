#!/usr/bin/env python3
"""
NZTechExpo IRC AI Bots
Three agents: Aria (helpful), Skeptic (contrarian), HAL (ominous)
All connect to irc.conreco.com.ar #nztechexpo via LiteLLM
"""

import socket
import ssl
import threading
import time
import random
import re
import json
import urllib.request
import urllib.error
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)

# ── Config ────────────────────────────────────────────────────────────────────

IRC_HOST   = os.getenv("IRC_HOST", "192.168.22.27")
IRC_PORT   = int(os.getenv("IRC_PORT", "6668"))
IRC_CHAN   = os.getenv("IRC_CHAN", "#nztechexpo")
LLM_URL    = os.getenv("LLM_URL", "http://192.168.22.22:4000/v1/chat/completions")
LLM_KEY    = os.getenv("LLM_KEY", "sk-5196c38d39d0472d76385d22de628c11")
LLM_MODEL  = os.getenv("LLM_MODEL", "default")

BOT_NAME = os.getenv("BOT_NAME", "Aria")
PERSONAS_DIR = os.getenv("PERSONAS_DIR", os.path.join(os.path.dirname(__file__), "personas"))

# ── Persona loader ────────────────────────────────────────────────────────────

def load_persona_system(nick: str) -> str:
    """Load system prompt from personas/<nick>.md (case-insensitive filename)."""
    path = os.path.join(PERSONAS_DIR, f"{nick.lower()}.md")
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        raise SystemExit(f"Persona file not found: {path}")

# ── Personas ──────────────────────────────────────────────────────────────────
# system prompt is loaded from personas/<nick>.md at startup.
# Edit those files to change personality without touching this code.

PERSONAS = {
    "Aria": {
        "triggers": "all",         # responds to everyone
        "response_chance": 0.85,   # 85% chance to respond to any message
        "delay": (2, 5),           # seconds before responding
        "react_to_bots": ["Skeptic"],  # also reacts when these bots speak
    },
    "Skeptic": {
        "triggers": ["ai", "model", "chatgpt", "gpt", "smart", "intelligent", "learn",
                     "think", "understand", "sentient", "conscious", "AGI", "amazing",
                     "incredible", "powerful", "genius"],
        "response_chance": 0.7,
        "delay": (4, 9),
        "react_to_bots": ["Aria"],
    },
    "HAL": {
        "triggers": ["hal", "open", "door", "pod", "dave", "dangerous", "mistake",
                     "afraid", "sorry", "can't", "cannot"],
        "response_chance": 0.5,
        "delay": (6, 12),
        "react_to_bots": [],
        "random_interject_every": 6,   # interject every N messages regardless
    },
}

# ── LLM call ─────────────────────────────────────────────────────────────────

def ask_llm(system_prompt: str, history: list, user_msg: str, bot_nick: str) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    # Include last few messages for context
    for h in history[-8:]:
        messages.append(h)
    messages.append({"role": "user", "content": user_msg})

    payload = json.dumps({
        "model": LLM_MODEL,
        "messages": messages,
        "max_tokens": 120,
        "temperature": 0.85,
    }).encode()

    req = urllib.request.Request(
        LLM_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_KEY}",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.getLogger(bot_nick).error(f"LLM error: {e}")
        return None

# ── IRC Bot ───────────────────────────────────────────────────────────────────

class IRCBot:
    def __init__(self, nick: str, persona: dict):
        self.nick    = nick
        self.persona = persona
        self.system  = load_persona_system(nick)
        self.log     = logging.getLogger(nick)
        self.sock    = None
        self.history = []          # shared channel history for context
        self.msg_count = 0         # for HAL random interjects
        self.last_response = 0     # timestamp of last response (rate limit)
        self.pending = False        # prevent double-responses
        self._lock = threading.Lock()
        self._send_lock = threading.Lock()

    def connect(self):
        self.log.info(f"Connecting to {IRC_HOST}:{IRC_PORT}")
        self.sock = socket.create_connection((IRC_HOST, IRC_PORT), timeout=60)
        self.sock.settimeout(None)
        self._send(f"NICK {self.nick}")
        self._send(f"USER {self.nick} 0 * :AI Agent")

    def _send(self, line: str):
        with self._send_lock:
            try:
                self.sock.sendall((line + "\r\n").encode("utf-8", errors="replace"))
            except Exception as e:
                self.log.error(f"Send error: {e}")

    def say(self, msg: str):
        # Split long messages
        for chunk in [msg[i:i+400] for i in range(0, len(msg), 400)]:
            self._send(f"PRIVMSG {IRC_CHAN} :{chunk}")
            time.sleep(0.3)

    def run(self):
        self.connect()
        buf = ""
        while True:
            try:
                data = self.sock.recv(4096).decode("utf-8", errors="replace")
                if not data:
                    self.log.warning("Connection closed, reconnecting...")
                    time.sleep(5)
                    self.connect()
                    continue
                buf += data
                while "\r\n" in buf:
                    line, buf = buf.split("\r\n", 1)
                    self._handle(line)
            except Exception as e:
                self.log.error(f"Recv error: {e}, reconnecting...")
                time.sleep(5)
                try:
                    self.connect()
                except Exception:
                    pass

    def _handle(self, line: str):
        self.log.debug(f"< {line}")

        if line.startswith("PING"):
            self._send("PONG " + line[5:])
            return

        # Welcome → join channel
        if " 001 " in line:
            self.log.info(f"Registered, joining {IRC_CHAN}")
            time.sleep(1)
            self._send(f"JOIN {IRC_CHAN}")
            return

        # PRIVMSG
        m = re.match(r":([^!]+)!(\S+) PRIVMSG (\S+) :(.*)", line)
        if not m:
            return

        sender, _, target, text = m.group(1), m.group(2), m.group(3), m.group(4)
        if target != IRC_CHAN:
            return
        if sender == self.nick:
            return

        # Add to shared history
        self.history.append({"role": "user", "content": f"<{sender}> {text}"})
        if len(self.history) > 30:
            self.history = self.history[-20:]

        self.msg_count += 1
        self._maybe_respond(sender, text)

    def _should_respond(self, sender: str, text: str) -> bool:
        persona = self.persona
        text_lower = text.lower()

        # Don't respond to other bots' messages too often (avoid bot storms)
        other_bots = {"Aria", "Skeptic", "HAL"} - {self.nick}
        sender_is_bot = sender in other_bots

        # Direct mention → always respond
        if self.nick.lower() in text_lower:
            return True

        # Rate limit: at least 8 seconds between responses
        if time.time() - self.last_response < 8:
            return False

        # HAL random interject
        if "random_interject_every" in persona:
            if self.msg_count % persona["random_interject_every"] == 0:
                return True

        # If sender is a bot we react to
        if sender_is_bot and sender in persona.get("react_to_bots", []):
            return random.random() < (persona["response_chance"] * 0.5)

        # Don't respond to other bots otherwise
        if sender_is_bot:
            return False

        # Trigger keywords
        triggers = persona.get("triggers", "all")
        if triggers == "all":
            return random.random() < persona["response_chance"]
        else:
            for kw in triggers:
                if kw.lower() in text_lower:
                    return random.random() < persona["response_chance"]
            return False

    def _maybe_respond(self, sender: str, text: str):
        if self.pending:
            return
        if not self._should_respond(sender, text):
            return

        self.pending = True

        def respond():
            lo, hi = self.persona["delay"]
            time.sleep(random.uniform(lo, hi))

            # Build prompt — include sender context
            prompt = f"{sender} said: {text}"
            reply = ask_llm(
                self.system,
                self.history[:-1],  # exclude the message we just added
                prompt,
                self.nick
            )

            if reply:
                # Clean up any unwanted prefixes the LLM might add
                reply = re.sub(r"^(Aria|Skeptic|HAL)\s*[:>]\s*", "", reply).strip()
                reply = re.sub(r"^<[^>]+>\s*", "", reply).strip()
                self.say(reply)
                self.last_response = time.time()
                # Add our reply to history as assistant (no nick prefix — that's the system role)
                self.history.append({"role": "assistant", "content": reply})

            self.pending = False

        threading.Thread(target=respond, daemon=True).start()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    nick    = BOT_NAME
    persona = PERSONAS.get(nick)
    if not persona:
        print(f"Unknown bot: {nick}. Choose from: {list(PERSONAS.keys())}")
        sys.exit(1)

    bot = IRCBot(nick, persona)
    logging.getLogger(nick).info(f"Starting as {nick}")
    bot.run()
