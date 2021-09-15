# https://stackabuse.com/text-classification-with-python-and-scikit-learn/
import pandas as pd
import re

data = pd.read_csv('data.csv')  
# make all lowercase
data = data.applymap(lambda s:s.lower())

# Remove all the special characters
data = data.applymap(lambda s:re.sub(r'\W', ' ',s))

print(data.head())
#  # remove all single characters
# data = data.applymap(lambda s:re.sub(r'\s+[a-zA-Z]\s+', ' ',s))

# # Remove single characters from the start
# data = data.applymap(lambda s:re.sub(r'\^[a-zA-Z]\s+', ' ',s))
# # Substituting multiple spaces with single space
# data = data.applymap(lambda s:re.sub(r'\s+', ' ',s,flags=re.I))
# # Removing prefixed 'b'
# data = data.applymap(lambda s:re.sub(r'^b\s+', ' ',s,flags=re.I))
# Lemmatization
# data['title'] = data['title'].apply(lambda s:s.split())
# data['body'] = data['body'].apply(lambda s:s.split())

# import nltk
# nltk.download('wordnet')
# from nltk.stem import WordNetLemmatizer
# stemmer = WordNetLemmatizer()

# data['title'] = data['title'].apply(lambda s: [stemmer.lemmatize(word) for word in s])
# data['body'] = data['body'].apply(lambda s: [stemmer.lemmatize(word) for word in s])

# print(data.head())

# # TODO change
# data['link_flair_text'] = data['link_flair_text'].apply(lambda s: 1 if s == "Asshole" else 0)

# # creating the feature matrix 
# from sklearn.feature_extraction.text import CountVectorizer
# matrix = CountVectorizer(max_features=1000)
# X = matrix.fit_transform(data['body']).toarray()
# y = data.iloc[:, 2]
# print(y)

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y)

# # Naive Bayes 
# from sklearn.naive_bayes import GaussianNB
# classifier = GaussianNB()
# classifier.fit(X_train, y_train)

# # Predict Class
# y_pred = classifier.predict(X_test)

# # Accuracy 
# from sklearn.metrics import accuracy_score
# accuracy = accuracy_score(y_test, y_pred)

# print(accuracy)

# # str1 = """I live with my wife (f39) my two kiddos (f11) . One of my daughters is autistic, the other is adopted and came from quite a difficult background, so they both need a bit more attention and care than most kids their age. I was taking a walk with my two daughters yesterday, and my biological daughter got a little overwhelmed, and did her usual coping mechanism of sitting on the ground sucking her thumb. My adopted daughter always gets stressed out when her sister is upset so she was also sitting on the ground cuddling her. I'm trying to comfort them both while also trying to keep them away from the yellow snow that they're coming dangerously close to lying in, when we run into someone we know. She's the mother of one of the kids my daughter goes to school with- I wouldn't say we're friends, as we have very little in common aside from that, but we have a decent amount of rapport. Seeing the situation, she asks if everything is ok. I told her it was, and just that they don't really handle crowds and noise very well, but that everything's fine. She reaches out, pulls bio daughter to her feet, and asks (very kindly but a bit intensely) if everything is ok. Bio daughter \*really\* doesn't like being touched by strangers, and breaks away to cling on to me. Friend tries to hug adopted daughter, who does the same. I'm having a bit of an issue processing all of this (I have autism too) so I take a few seconds to react, and by the time I've taken everything in, my friend has her hands on both of my daughters (quite tightly) and is saying how rude they're being. I snap, and start shouting at her to get her hands off my children. She starts crying, runs off.

# # Later, she  sends me a Facebook message. She apologises for what she did, and says that her oldest daughter had died a few days ago, and that seeing my kids had triggered a lot of negative emotions in her. I apologised back to her for cursing her out, and said that if she needed any help with anything to message me. She said what would really help was getting my kids to apologise to her. I responded (copying and pasting for full disclosure)

# # ""I'm really sorry but I don't think I can do that. I know your actions were understandable given the circumstances, but at the end of the day (my children) reacted the way they did because there was an adult putting her hands on them without permission, and I don't want to teach them that it's wrong to break away when someone does that. I'm really sorry for all the pain you're going through- my brother passed away a few years ago and I was a wreck- and if there's anything else I can do please let me know.""

# # She responded ""unbelievable"" and blocked me.

# # AITA? At the end of the day my first responsibility is to my children and I did what I thought was best for them, but I maybe should have been more responsive to her pain. 

# # Edit- Sorry for not responding to each comment individually there's a lot! Also, I'm a woman not a man, sorry for not being clear! ",Not the A-hole
# # AITA For refusing to share my son's gift from family with his step brother?,"Hey, I really thought this wouldn't be an issue but I'll explain the situation quickly.
# # """

# # # data
# # # message = [X[0], X[1]]
# # # matrix = CountVectorizer(max_features=1000)
# # # X = matrix.fit_transform(message).toarray()
# # # print(X)
# # # y_pred = classifier.predict(X)
# # # print(classifier.predict(X))
# # # print(X_train)
# # # print(classifier.predict([["Hello"]]))
