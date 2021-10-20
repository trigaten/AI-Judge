#!/usr/bin/env python
"""Link AITA posts with their highest rated top-level comments"""
import json

__author__ = "Avik Rao"
__email__ = "avik.rao@gmail.com"

# Minimum post/comment scores, higher = smaller but better quality sample
POST_SCORE_THRESHOLD = 50 
COMMENT_SCORE_THRESHOLD = 50 

# Input/output filenames
COMMENTS_FILE = 'parsedcomments.json'
POSTS_FILE = 'parsedposts.json'
OUTPUT_FILE = 'linked.json'

# AITA tags
TAGS = ('YTA', 'NTA', 'NAH', 'ESH')


def main() :

    # Load posts as json
    posts = []
    with open(POSTS_FILE, "r") as f :
        posts = json.load(f)
    print("Done loading posts.")
    
    # Load comments as json
    comments = []
    with open(COMMENTS_FILE, "r") as f :
        comments = json.load(f)
    print("Done loading comments.")

    end_list = []

    # Create dict of post ID: post
    posts_dict = {}
    for post in posts :
        # Check if post score meets minimum threshold
        if post['score'] < POST_SCORE_THRESHOLD :
            continue
        posts_dict[post['id']] = post
    
    # Create dict of post ID: top comment
    comments_dict = {}
    for comment in comments :

        score = comment['score']
        # Check if comment score meets minimum threshold
        if score < COMMENT_SCORE_THRESHOLD :
            continue

        # Get comment judgement (YTA, NTA, ESH, NAH)
        judgement = comment['body'][0:3].upper()
        if judgement not in TAGS :
            continue

        # Set as top comment if higher than previously found
        post_id = comment['post_id'][3:]
        if post_id in comments_dict :
            if score > comments_dict[post_id]['score'] :
                comments_dict[post_id] = comment 
        else :
            comments_dict[post_id] = comment 
    
    # Link posts with top comment 
    for post_id in posts_dict :
        if post_id not in comments_dict :
            continue
        post = posts_dict[post_id]
        comment = comments_dict[post_id]
        judgement = comment['body'][0:3].upper()
        end_list.append({'title': post['title'], 'post_body': post['body'], 'judgement': judgement, 'comment_body': comment['body']})

    print(f"Done linking. (Found {len(end_list)} matches)")

    # Output result json to file
    with open(OUTPUT_FILE, "w") as f :
        json.dump(end_list, f, indent=4)

if __name__ == '__main__' :
    main()