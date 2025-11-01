#!/usr/bin/python3
"""
Module that queries the Reddit API and returns subscriber count.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Query the Reddit API and return the number of subscribers.

    Args:
        subreddit: name of the subreddit

    Returns:
        Number of subscribers or 0 if invalid subreddit
    """
    if subreddit is None or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'python:subreddit.counter:v1.0'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False,
                                timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        return 0
    except Exception:
        return 0
