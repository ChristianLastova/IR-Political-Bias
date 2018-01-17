from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from random import shuffle
import numpy as np
from sklearn.externals import joblib

#read in data
print("Reading articles")
data = []
#kaggle - all the news
for i in range(1,4):
    for line in open("all-the-news/articles_format" + str(i) + ".csv"):
        fields = line.strip().split("\t",1)
        if len(fields) < 2:
            continue
        data.append((fields[0], fields[1]))

# webhose - english news
for line in open("webhose_news_formatted.csv"):
    fields = line.strip().split("\t",1)
    if len(fields) < 2:
        continue
    data.append((fields[0], fields[1]))

shuffle(data)

split_index = 2000
grid_data = data[:split_index]
data_test = data[split_index:]


(target, articles) = zip(*grid_data)
(target_test, articles_test) = zip(*data_test)


clf = joblib.load('political_bias_classifier.pkl')
parameters = {
              'clf__penalty': ['l2', 'l1', 'elasticnet'],
              'clf__alpha': (1e-3, 1e-4, 1e-5, 1e-6),
              'clf__loss': ['squared_hinge', 'hinge', 'perceptron'],
              'vect__stop_words': ['english', None],
              'vect__max_df': [0.7, 0.8, 0.9, 1.0],
}
print("Tuning parameters")
gs_clf = GridSearchCV(clf, parameters, n_jobs=-1)

gs_clf = gs_clf.fit(articles, target)
print(gs_clf.best_score_)


for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))

print("Testing data")
predicted = gs_clf.predict(articles_test)
print(np.mean(predicted == target_test))

joblib.dump(gs_clf, 'political_bias_classifier_optimized.pkl')
