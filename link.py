import json 

COMMENTS_FILE = 'parsedcomments.json'
POSTS_FILE = 'parsedposts.json'

TAGS = ('YTA', 'NTA', 'NAH', 'ESH')

def main() :

    posts = []
    with open(POSTS_FILE, "r") as f :
        posts = json.load(f)

    print("Done loading posts.")
    
    comments = []
    with open(COMMENTS_FILE, "r") as f :
        comments = json.load(f)

    print("Done loading comments.")

    end_list = []
    linked = 0
    for post in posts :

        if post['score'] < 50 :
            continue

        top_comment = {'comment_id': None, 'score': 50}
        for comment in comments :
            post_id = comment['post_id'][3:]
            if post_id == post['id'] :
                judgement = comment['body'][0:3].upper()
                if (comment['score'] > top_comment['score'] and 
                    judgement in TAGS) :
                    post['judgement'] = judgement
                    top_comment = comment
        
        if top_comment['comment_id'] == None :
            continue

        zipped = {'title': post['title'], 'post_body': post['body'], 'judgement': post['judgement'], 'comment_body': top_comment['body']}

        linked += 1
        
        end_list.append(zipped)

    print(f"Done linking. (Found {len(end_list)} matches)")

    with open("linked.json", "w") as f :
        json.dump(end_list, f, indent=4)



if __name__ == '__main__' :
    main()