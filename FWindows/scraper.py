import praw

reddit = praw.Reddit(client_id='VZu2jnSdaSnzEA', client_secret='YD-aEHSx6sWKGwnkqJJYvg90k2Dl9A', user_agent='Sander S')


import pandas as pd
posts = []
ml_subreddit = reddit.subreddit('AmItheAsshole')
for post in ml_subreddit.hot(limit=10000):
    if post.link_flair_text == "Asshole" or post.link_flair_text == "Not the A-hole":
        posts.append([post.title, post.selftext, post.link_flair_text])
posts = pd.DataFrame(posts,columns=['title', 'body', 'link_flair_text'])
posts.to_csv("data_test.csv", index=False)
print(posts)