#!/usr/bin/python3
"""
Module that recursively queries the Reddit API for all hot posts.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively query the Reddit API and return all hot post titles.

    Args:
        subreddit: name of the subreddit
        hot_list: list to accumulate titles
        after: pagination token

    Returns:
        List of all hot post titles or None if invalid
    """
    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'python:subreddit.recurse:v1.0'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            after = data.get('data', {}).get('after')

            for post in posts:
                hot_list.append(post.get('data', {}).get('title'))

            if after is not None:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return None
    except Exception:
        return None
