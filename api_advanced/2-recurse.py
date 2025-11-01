#!/usr/bin/python3
"""
Module to recursively query Reddit API for all hot posts.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing
    the titles of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit
        hot_list (list): List to accumulate titles (default: [])
        after (str): Pagination token (default: None)

    Returns:
        list: List of all hot post titles, or None if invalid
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'MyRedditApp/0.0.1'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
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
