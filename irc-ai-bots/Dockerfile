FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY kickstarter.py .
COPY config.yaml .

# BOT_NAME must be set per-container (e.g. sage, chaos, oracle, hacker, poet)
ENV BOT_NAME=""
ENV CONFIG_FILE="/app/config.yaml"

CMD ["python", "-u", "bot.py"]
