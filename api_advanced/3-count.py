#!/usr/bin/python3
"""
Module to recursively query Reddit API and count keyword occurrences.
"""
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively queries the Reddit API, parses titles, and prints
    sorted keyword counts.

    Args:
        subreddit (str): The name of the subreddit
        word_list (list): List of keywords to count
        after (str): Pagination token (default: None)
        word_count (dict): Dictionary to track counts (default: None)

    Returns:
        None: Prints sorted keyword counts
    """
    if word_count is None:
        word_count = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'MyRedditApp/0.0.1'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
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
                    word_count[word_lower] = word_count.get(word_lower, 0) + count

        if after is not None:
            return count_words(subreddit, word_list, after, word_count)
        else:
            if word_count:
                sorted_counts = sorted(word_count.items(),
                                       key=lambda x: (-x[1], x[0]))
                for word, count in sorted_counts:
                    print(f"{word}: {count}")

    except Exception:
        return
