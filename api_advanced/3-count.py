#!/usr/bin/python3
"""
Module that recursively queries Reddit API and counts keyword occurrences.
"""
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively query Reddit API and print sorted keyword counts.

    Args:
        subreddit: name of the subreddit
        word_list: list of keywords to count
        after: pagination token
        word_count: dictionary to track counts

    Returns:
        None
    """
    if word_count is None:
        word_count = {}

    if subreddit is None or not isinstance(subreddit, str):
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'python:subreddit.wordcount:v1.0'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        after = data.get('data', {}).get('after')

        for post in posts:
            title = post.get('data', {}).get('title', '').lower()
            words = title.split()

            for word in word_list:
                word_lower = word.lower()
                count = sum(1 for w in words if w == word_lower)
                if count > 0:
                    if word_lower in word_count:
                        word_count[word_lower] += count
                    else:
                        word_count[word_lower] = count

        if after is not None:
            return count_words(subreddit, word_list, after, word_count)
        else:
            if word_count:
                sorted_counts = sorted(word_count.items(),
                                       key=lambda x: (-x[1], x[0]))
                for word, count in sorted_counts:
                    print("{}: {}".format(word, count))

    except Exception:
        return
