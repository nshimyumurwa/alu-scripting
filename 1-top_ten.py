#!/usr/bin/python3
"""
Module that queries the Reddit API and prints top 10 hot posts.
"""
import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print titles of first 10 hot posts.

    Args:
        subreddit: name of the subreddit

    Returns:
        None
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'python:subreddit.topten:v1.0'}
    params = {'limit': 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            children = data.get('data', {}).get('children', [])
            if not children:
                print(None)
                return
            for post in children:
                title = post.get('data', {}).get('title')
                if title:
                    print(title)
        else:
            print(None)
    except Exception:
        print(None)
