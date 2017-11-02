from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from random import shuffle
import numpy as np
from sklearn.externals import joblib

FULL_TRAINING = True

categories = ['liberal', 'conservative']
data = [] # list of tuples (target, article)

weird = 0
for i in range(1,4):
    for line in open("all-the-news/articles_format" + str(i) + ".csv"):
        fields = line.strip().split("\t",1)
        if len(fields) < 2:
            weird += 1
            continue
        data.append((fields[0], fields[1]))
shuffle(data)

split_index = len(data)*4//5
data_train = data[:split_index]
data_test = data[split_index:]

if FULL_TRAINING:
    (target_train, articles_train) = zip(*data)
else:
    (target_train, articles_train) = zip(*data_train)
(target_test, articles_test) = zip(*data_test)

print(weird)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(articles_train)
print(X_train_counts.shape)

tf_transformer = TfidfTransformer().fit_transform(X_train_counts)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidif', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                           max_iter=5, tol=None)),
])
text_clf.fit(articles_train, target_train)

joblib.dump(text_clf, 'political_bias_classifier.pkl')

predicted = text_clf.predict(articles_test)
print(np.mean(predicted == target_test))
