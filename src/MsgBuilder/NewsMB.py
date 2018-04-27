"""
Module where we build a perfect message to the client
"""

# Generate news articles to send.
def generateNewsPosts(data):
    posts = []
    for element in data:
        post = {
            "title": element['title'],
            "image_url": element['urlToImage'],
            "subtitle": element['description'],
            "buttons": [
                {
                    'type': 'web_url',
                    'url': element['url'],
                    'title': 'Read more'
                }
            ]
        }
        posts.append(post)
    return posts    