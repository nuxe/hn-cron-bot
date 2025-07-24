# HN Cron Bot

A simple bot that searches Hacker News for posts about "serverless" and posts them to Slack.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up Modal secrets:
   ```bash
   modal secret create slack-secret SLACK_BOT_TOKEN=your_token_here
   ```

3. Deploy and run:
   ```bash
   modal run main.py::search_hackernews
   ```

## How it works

- Searches HN Algolia API for posts containing "serverless" from the last 24 hours
- Posts found URLs to the selected Slack channel
- Runs on Modal's serverless platform (https://modal.com)
