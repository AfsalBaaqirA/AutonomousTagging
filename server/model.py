import pandas as pd
import numpy as np
import joblib

df = pd.read_csv("D:\\Projects\\AutonomousTagging\\server\\final_data.csv")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier


import ast

df["Tags"] = df["Tags"].apply(lambda s: s.split())

y = df["Tags"]

multilabel = MultiLabelBinarizer()
y = multilabel.fit_transform(y)

pd.DataFrame(y, columns=multilabel.classes_)

tfidf = TfidfVectorizer(
    analyzer="word", max_features=10000, ngram_range=(1, 3), stop_words="english"
)

X = tfidf.fit_transform(df["Body"].values.astype(str))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


sgd = SGDClassifier()
lr = LogisticRegression()
svc = LinearSVC()


def j_score(y_true, y_pred):
    jaccard = np.minimum(y_true, y_pred).sum(axis=1) / np.maximum(y_true, y_pred).sum(
        axis=1
    )
    return jaccard.mean() * 100


def print_score(y_pred, clf):
    print("CLF: ", clf.__class__.__name__)
    print("Jaccard score: {}".format(j_score(y_test, y_pred)))
    print("---------------------------")


for classifier in [sgd, lr, svc]:
    clf = OneVsRestClassifier(classifier)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print_score(y_pred, classifier)

for classifier in [sgd, lr, svc]:
    clf = OneVsRestClassifier(classifier)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print_score(y_pred, classifier)


joblib_file = "tagPredictor.pkl"
joblib.dump(clf, joblib_file)
