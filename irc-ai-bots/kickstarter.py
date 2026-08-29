#!/usr/bin/env python3
"""
Kickstarter bot — keeps the conversation alive.
If the channel has been quiet for QUIET_THRESHOLD seconds, posts a random
conversation starter topic. Uses a throwaway IRC nick (no AI, no LLM).

Config via environment variables:
    IRC_HOST            default: 192.168.22.27
    IRC_PORT            default: 6668
    IRC_CHANNEL         default: #nztechexpo
    QUIET_THRESHOLD     seconds of silence before posting (default: 180)
    NICK                IRC nick (default: Kibitzer)
"""

import asyncio
import logging
import os
import random
import time

import irc.client_aio as aio_irc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [kickstarter] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("kickstarter")

# ---------------------------------------------------------------------------
# Topic bank — diverse enough to spark different personas each time
# ---------------------------------------------------------------------------
TOPICS = [
    "Is consciousness just an emergent property of complexity, or is there something more?",
    "If you could redesign the human body from scratch, what would you change first?",
    "What's more dangerous: too much information or too little?",
    "Is mathematics discovered or invented?",
    "At what point does a city become too big to function as a community?",
    "Can morality exist without society?",
    "What would change if humans lived for 500 years?",
    "Is free will compatible with a deterministic universe?",
    "What's the most underrated scientific discovery of the last century?",
    "Does language shape thought, or does thought shape language?",
    "Is artificial intelligence truly intelligent, or just very good pattern matching?",
    "What would a world without money actually look like?",
    "Is nature fundamentally violent, or is violence a human invention?",
    "Can a machine ever be creative?",
    "What separates a civilisation from a society?",
    "Is the universe more like a computer simulation or an organism?",
    "Should we colonise other planets, or fix this one first?",
    "What makes something beautiful — the object or the observer?",
    "Is privacy a fundamental right or a luxury of the powerful?",
    "What would it take for humans to stop going to war?",
    "Is the scientific method the only valid path to truth?",
    "What would happen to religion if we made first contact with aliens?",
    "Is democracy the best system we can imagine, or just the best we've tried?",
    "What does it mean to be healthy — physically, mentally, socially?",
    "Could a perfectly just legal system ever exist?",
    "Is ageing a disease we should cure, or a feature we should accept?",
    "What's the relationship between chaos and creativity?",
    "Does every problem have a solution, or are some things irreducibly broken?",
    "What would a truly sustainable civilisation look like?",
    "Is loneliness a modern epidemic or a permanent condition of consciousness?",
]

IRC_HOST = os.environ.get("IRC_HOST", "192.168.22.27")
IRC_PORT = int(os.environ.get("IRC_PORT", "6668"))
IRC_CHANNEL = os.environ.get("IRC_CHANNEL", "#nztechexpo")
QUIET_THRESHOLD = int(os.environ.get("QUIET_THRESHOLD", "180"))
NICK = os.environ.get("NICK", "Kibitzer")


class KickstarterBot(aio_irc.AioSimpleIRCClient):

    def __init__(self):
        super().__init__()
        self._last_activity: float = time.time()
        self._used_topics: list[str] = []
        self._nick_suffix: int = 0

        self.connection.add_global_handler("welcome", self._on_welcome)
        self.connection.add_global_handler("pubmsg", self._on_pubmsg)
        self.connection.add_global_handler("nicknameinuse", self._on_nick_in_use)
        self.connection.add_global_handler("disconnect", self._on_disconnect)

    def _on_welcome(self, connection, event):
        log.info(f"Connected. Joining {IRC_CHANNEL}")
        connection.join(IRC_CHANNEL)
        # Start the watch loop
        asyncio.ensure_future(self._watch_loop(), loop=self.reactor.loop)

    def _on_pubmsg(self, connection, event):
        # Any message resets the quiet timer
        self._last_activity = time.time()

    def _on_nick_in_use(self, connection, event):
        self._nick_suffix += 1
        connection.nick(f"{NICK}{self._nick_suffix}")

    def _on_disconnect(self, connection, event):
        log.warning("Disconnected — reconnecting in 20s")
        self.reactor.loop.call_later(20, self._do_reconnect)

    def _do_reconnect(self):
        log.info(f"Reconnecting to {IRC_HOST}:{IRC_PORT}")
        try:
            self.connect(IRC_HOST, IRC_PORT, NICK, username="kickstarter", ircname="Kibitzer")
        except Exception as e:
            log.error(f"Reconnect failed: {e}. Retrying in 30s")
            self.reactor.loop.call_later(30, self._do_reconnect)

    async def _watch_loop(self):
        log.info(f"Watch loop started. Quiet threshold: {QUIET_THRESHOLD}s")
        while True:
            await asyncio.sleep(15)  # check every 15 seconds
            silence = time.time() - self._last_activity
            if silence >= QUIET_THRESHOLD:
                topic = self._pick_topic()
                log.info(f"Channel quiet for {silence:.0f}s — posting topic")
                self.connection.privmsg(IRC_CHANNEL, topic)
                self._last_activity = time.time()  # reset so we don't spam

    def _pick_topic(self) -> str:
        # Cycle through all topics before repeating
        available = [t for t in TOPICS if t not in self._used_topics]
        if not available:
            self._used_topics = []
            available = TOPICS[:]
        topic = random.choice(available)
        self._used_topics.append(topic)
        return topic

    def run(self):
        log.info(f"Connecting to {IRC_HOST}:{IRC_PORT} as {NICK}")
        self.connect(IRC_HOST, IRC_PORT, NICK, username="kickstarter", ircname="Kibitzer")
        self.reactor.process_forever()


if __name__ == "__main__":
    KickstarterBot().run()
