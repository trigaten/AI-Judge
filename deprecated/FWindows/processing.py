"""Set of functions which help parse and clean data and load it into pandas dataframes"""
import pandas as pd
import re
import math
import nltk
# pretrained tokenizer
nltk.download('punkt')
from nltk.tokenize import word_tokenize 

# import stemmer
from nltk.stem import PorterStemmer 

# remove stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords

from types import SimpleNamespace

def read_csv(path = '/Users/sander/Desktop/ML_Learn/AI-Judge/aita_clean.csv', do_preprocess=True, samples=False):
    data = pd.read_csv(path)  

    # remove unnecessary columns
    data.drop(['id', 'timestamp', 'edited', 'score', 'num_comments', 'verdict'], axis=1, inplace=True)

    # remove rows with incomplete data
    data = data.dropna()

    if samples:
        data = data.sample(n=samples)

    if do_preprocess:
        data = preprocess(data)

    return data

def preprocess(data):
    """Perform various preprocessing operations on 
    title and body of data"""
    # Select columns to apply preprocessing to
    pp_cols = ["title", "body"]

    # stemmer
    ps = PorterStemmer() 

    # make all lowercase
    data[pp_cols] = data[pp_cols].applymap(lambda s:s.lower())

    # Remove all the special characters
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'\W', ' ',s))

    # remove all single characters
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'\s+[a-zA-Z]\s+', ' ',s))

    # Remove single characters from the start (no space before them, but space after)
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'^[a-zA-Z]\s+', ' ',s))

    # Removing prefixed 'b'
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'^b\s+', ' ',s,flags=re.I))

    # remove all of: x200b (zero-width space)
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'x200b', ' ',s))

    # Substituting multiple spaces with single space
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'\s+', ' ',s,flags=re.I))

    # Remove single numbers
    data[pp_cols] = data[pp_cols].applymap(lambda s:re.sub(r'\d+', ' ',s,flags=re.I))

    # tokenize data
    data[pp_cols] = data[pp_cols].applymap(lambda s:word_tokenize(s))

    # perform stemming
    data[pp_cols] = data[pp_cols].applymap(lambda s: [ps.stem(word) for word in s])

    # remove stopwords
    data[pp_cols] = data[pp_cols].applymap(lambda s: [word for word in s if word not in stopwords.words('english')])
    
    return data

def freq_map(in_data, labels, laplacian=True):
    words = {}
    
    totalPos = 0
    totalNeg = 0
    
    data = pd.concat([in_data, labels], axis=1)
    # calculate frequencies
    for index, row in data.iterrows():

        words_in_body = len(row['body'])

        if row['is_asshole'] == 1:
            totalPos += words_in_body
        else:
            totalNeg += words_in_body
        
        # iterate through body text of this row
        for word in row['body']:
            if word not in words:
                words[word] = SimpleNamespace(pos_freq=0, neg_freq = 0)
            if row['is_asshole'] == 1:
                words[word].pos_freq += 1.0
            else:
                words[word].neg_freq += 1.0
    if laplacian:
        LaplacianSmoothFrequencies(words, totalPos, totalNeg)

    return words

def LaplacianSmoothFrequencies(dic, totalPos, totalNeg):
    for key in dic:
        freq_data = dic[key]

        freq_data.pos_freq += 1.0
        freq_data.pos_freq/= (totalPos + len(dic))

        freq_data.neg_freq += 1.0
        freq_data.neg_freq /= (totalNeg + len(dic))
        
def test_freqs(dataframe, dic, preprocess = False, prior_ratio = 1):
    if preprocess:
        preprocess(dataframe)
    pred_labels = []
    for index, row in dataframe.iterrows():
        bayes_result = 1
        for word in row['body']:
            if word in dic:
                bayes_result += math.log(dic[word].pos_freq / dic[word].neg_freq)

        bayes_result += math.log(prior_ratio)
        if bayes_result > 0:
            pred_labels.append(1)
        elif bayes_result < 0:
            pred_labels.append(0)
        else:
            pred_labels.append(-1)
    dataframe['pred_label'] = pred_labels

if __name__ == '__main__':
    from data_processing import read_csv
    from data_processing import freq_map
    from data_processing import test_freqs
    from sklearn.model_selection import train_test_split

    data = read_csv(samples=5)

    X_train, X_test, y_train, y_test = train_test_split(data.drop(['is_asshole'], axis=1), data['is_asshole'], test_size=0.20, random_state=42)

    words = freq_map(X_train, y_train)

    test_freqs(data, words)
