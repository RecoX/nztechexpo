FROM python:3.12-slim
WORKDIR /app
COPY irc_bot.py .
COPY personas/ ./personas/
CMD ["python", "-u", "irc_bot.py"]
