import os
from datetime import datetime, timedelta

import modal

app = modal.App("example-hn-bot")

slack_sdk_image = modal.Image.debian_slim().pip_install("slack-sdk")

@app.function(
    image=slack_sdk_image,
    secrets=[modal.Secret.from_name("slack-secret", required_keys=["SLACK_BOT_TOKEN"])],
)
async def post_to_slack(message: str):
    import slack_sdk

    client = slack_sdk.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    client.chat_postMessage(channel="all-nuxe", text=message)

QUERY = "serverless"
WINDOW_SIZE_DAYS = 1
requests_image = modal.Image.debian_slim().pip_install("requests")

@app.function(image=requests_image)
def search_hackernews():
    import requests

    url = "http://hn.algolia.com/api/v1/search"

    threshold = datetime.utcnow() - timedelta(days=WINDOW_SIZE_DAYS)

    params = {
        "query": QUERY,
        "numericFilters": f"created_at_i>{threshold.timestamp()}",
    }

    response = requests.get(url, params, timeout=10).json()
    urls = [item["url"] for item in response["hits"] if item.get("url")]

    print(f"Query returned {len(urls)} items.")

    post_to_slack.for_each(urls)
