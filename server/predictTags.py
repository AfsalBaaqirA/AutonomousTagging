import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("D:\\Projects\\AutonomousTagging\\server\\final_data.csv")


df["Tags"] = df["Tags"].apply(lambda x: x.split())


all_tags = [item for sublist in df["Tags"].values for item in sublist]
my_set = set(all_tags)
unique_tags = list(my_set)

import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import ToktokTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

from scipy.sparse import hstack

flat_list = [item for sublist in df["Tags"].values for item in sublist]

keywords = nltk.FreqDist(flat_list)

keywords = nltk.FreqDist(keywords)

frequencies_words = keywords.most_common(100)
tags_features = [word[0] for word in frequencies_words]


def most_common(tags):
    tags_filtered = []
    for i in range(0, len(tags)):
        if tags[i] in tags_features:
            tags_filtered.append(tags[i])
    return tags_filtered


df["Tags"] = df["Tags"].apply(lambda x: most_common(x))
df["Tags"] = df["Tags"].apply(lambda x: x if len(x) > 0 else None)

df.dropna(subset=["Tags"], inplace=True)

df["Body"] = df["Body"].apply(
    lambda x: BeautifulSoup(x, features="html.parser").get_text()
)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub(r"\'\n", " ", text)
    text = re.sub(r"\'\xa0", " ", text)
    text = re.sub("\s+", " ", text)
    text = text.strip(" ")
    return text


df["Body"] = df["Body"].apply(lambda x: clean_text(x))

token = ToktokTokenizer()

punct = "!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~"


def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, "strip") else item for item in mylist)
    return [item for item in newlist if item != ""]


def clean_punct(text):
    words = token.tokenize(text)
    punctuation_filtered = []
    regex = re.compile("[%s]" % re.escape(punct))
    remove_punctuation = str.maketrans(" ", " ", punct)
    for w in words:
        if w in tags_features:
            punctuation_filtered.append(w)
        else:
            punctuation_filtered.append(regex.sub("", w))

    filtered_list = strip_list_noempty(punctuation_filtered)

    return " ".join(map(str, filtered_list))


df["Body"] = df["Body"].apply(lambda x: clean_punct(x))

nltk.download("stopwords")
nltk.download("wordnet")

lemma = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def lemitizeWords(text):
    words = token.tokenize(text)
    listLemma = []
    for w in words:
        x = lemma.lemmatize(w, pos="v")
        listLemma.append(x)
    return " ".join(map(str, listLemma))


def stopWordsRemove(text):
    stop_words = set(stopwords.words("english"))

    words = token.tokenize(text)

    filtered = [w for w in words if not w in stop_words]

    return " ".join(map(str, filtered))


df["Body"] = df["Body"].apply(lambda x: lemitizeWords(x))
df["Body"] = df["Body"].apply(lambda x: stopWordsRemove(x))

df["Title"] = df["Title"].apply(lambda x: str(x))
df["Title"] = df["Title"].apply(lambda x: clean_text(x))
df["Title"] = df["Title"].apply(lambda x: clean_punct(x))
df["Title"] = df["Title"].apply(lambda x: lemitizeWords(x))
df["Title"] = df["Title"].apply(lambda x: stopWordsRemove(x))


X1 = df["Body"]
X2 = df["Title"]
y = df["Tags"]

multilabel_binarizer = MultiLabelBinarizer()
y_bin = multilabel_binarizer.fit_transform(y)

vectorizer_X1 = TfidfVectorizer(
    analyzer="word",
    min_df=0.0,
    max_df=1.0,
    strip_accents=None,
    encoding="utf-8",
    preprocessor=None,
    token_pattern=r"(?u)\S\S+",
    max_features=1000,
)

vectorizer_X2 = TfidfVectorizer(
    analyzer="word",
    min_df=0.0,
    max_df=1.0,
    strip_accents=None,
    encoding="utf-8",
    preprocessor=None,
    token_pattern=r"(?u)\S\S+",
    max_features=1000,
)

X1_tfidf = vectorizer_X1.fit_transform(X1)
X2_tfidf = vectorizer_X2.fit_transform(X2)


import joblib

model = joblib.load("D:\\Projects\\AutonomousTagging\\server\\tagPredictor.pkl")


def getTags(title, body):
    body = BeautifulSoup(body).get_text()
    body = clean_text(body)
    body = clean_punct(body)
    body = lemitizeWords(body)
    body = stopWordsRemove(body)
    body = vectorizer_X1.transform([body])
    title = clean_text(title)
    title = clean_punct(title)
    title = lemitizeWords(title)
    title = stopWordsRemove(title)
    title = vectorizer_X2.transform([title])
    question = hstack([body, title])
    tags = multilabel_binarizer.inverse_transform(model.predict(question))
    print(tags)
    return tags
